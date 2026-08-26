#!/usr/bin/env python3
"""DELTA R60/F3 - W6 group 1: B1a, B1b, B3a, B4, B6. All in J3, then propagated to H29.

B1a  the row leans on the CATEGORY "regression guard", which no registered rule creates -
     SC-8(g) is not landing in v30a. Minimal GATES-TAG fix: state the property inline
     instead of naming a category the registration does not define. Registering SC-8(g)
     would be new normative text needing its own N5 pass, and B1b shows it would not fix
     the row anyway.
B1b  (g)(1) is asymmetric ("not counted as evidence that the phase's gate was MET") while
     the row was symmetric ("not counted toward the PASS/FAIL evidence"). The row now
     states the asymmetric form: these limbs cannot show the gate was met, and remain
     capable of failing it.
B3a  "the only one that is one-to-one" is false - the four-field Phase 6 key already is.
B4   failure mode 4 states a +-0.010 sliced test the deferred-to clause does not create.
B6   s5(b) says the row fails while the same document's table row 1 says NOT LIVE.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
p = D / "J3_C1_REDRAFT.md"
t = p.read_text(encoding="utf-8")
SUBS = []

# ---- B1a + B1b + B3a: the operative row's two limb labels and the uniqueness claim
SUBS.append((
    "> **the reference anchor holds on both limbs**: *(i)* **AGREEMENT \u2014 A REGRESSION GUARD, AND\n"
    "> LABELLED ONE. What it guards against: a substituted, regenerated or corrupted fixture, which\n"
    "> would move the recomputed entry off the figure the originating experiment recorded.** Each\n"
    "> declared reference-anchor entry is compared against that figure **for the same\n"
    "> `(side, instrument, architecture, horizon_s, tier)`** \u2014 the key stated in full because it is\n"
    "> the only one that is one-to-one: `(horizon, side)` alone selects 16 rows spanning\n"
    "> 0.5420\u20130.9662, **42\u00d7 the tolerance below**, and dropping `tier` leaves three rows per\n"
    "> combination whose 30s values are 0.8299 / 0.8564 / 0.8666 \u2014 **two of the three fail \u00b10.010\n"
    "> against the declared entry, so the key decides the outcome.**",

    "> **the reference anchor holds on both limbs**: *(i)* **AGREEMENT \u2014 this limb CANNOT FAIL while\n"
    "> the fixture is unchanged, and FAILS on substitution, regeneration or corruption of it, which\n"
    "> would move the recomputed entry off the figure the originating experiment recorded. It is\n"
    "> therefore NOT evidence that this gate was met, and remains capable of failing it.** Each\n"
    "> declared reference-anchor entry is compared against that figure **for the same\n"
    "> `(side, instrument, architecture, horizon_s, tier)`** \u2014 the key stated in full because it is\n"
    "> **the join key across two artifacts, neither of which carries all five fields**: the\n"
    "> originating record is keyed `(instrument, architecture, horizon_s, tier)` and is one-to-one on\n"
    "> those four, while `side` selects which declared entry is being compared and is not a column\n"
    "> of it. `(horizon, side)` alone selects 16 rows spanning 0.5420\u20130.9662, **42\u00d7 the tolerance\n"
    "> below**, and dropping `tier` leaves three rows per combination whose 30s values are\n"
    "> 0.8299 / 0.8564 / 0.8666 \u2014 **two of the three fail \u00b10.010 against the declared entry, so the\n"
    "> key decides the outcome.**"))

SUBS.append((
    "> ground declared before any Phase 1 measurement, never after one; *(ii)* **INTEGRITY \u2014 ALSO A\n"
    "> REGRESSION GUARD, guarding against byte corruption of the committed fixture or a changed AUC\n"
    "> routine** \u2014 each entry is recomputed",

    "> ground declared before any Phase 1 measurement, never after one; *(ii)* **INTEGRITY \u2014 likewise\n"
    "> incapable of failing on an unchanged fixture, and failing on byte corruption of the committed\n"
    "> fixture or a changed AUC routine; likewise not evidence that this gate was met** \u2014 each entry\n"
    "> is recomputed"))

SUBS.append((
    "> **THE PASS/FAIL EVIDENCE FOR THIS ROW** is carried by the sliced variant, the four\n"
    "> alignment-control cases, the snapshot hashing, and the \u00a710.0 ordering and claims-verified\n"
    "> clauses. Limbs (i) and (ii) are guards and are not counted toward it.",

    "> **WHAT SHOWS THIS ROW WAS MET** is the sliced variant, the four alignment-control cases, the\n"
    "> snapshot hashing, and the \u00a710.0 ordering and claims-verified clauses. **Limbs (i) and (ii)\n"
    "> cannot show it was met \u2014 neither can fail on an unchanged fixture \u2014 but either can still fail\n"
    "> it, and a failure of either denies the row.**"))

# ---- B4: failure mode 4
SUBS.append((
    "| 4 | **The sliced variant misses its declared entry by more than \u00b10.010.**",
    "| 4 | **The sliced variant fails the ex-ante scoring rule \u00a76.2 (v30a) \"Sliced variant \u2014 "
    "operative\" registers for it** \u2014 not a \u00b10.010 comparison, which that clause does not create "
    "*(corrected R60/F3-B4)*."))

for old, new in SUBS:
    n = t.count(old)
    assert n == 1, "match %d for %.60s" % (n, old.replace("\n", " "))
    t = t.replace(old, new, 1)

# ---- B6: §5(b)'s contradiction with its own table row 1
i = t.index("**The consequence, stated plainly because the author is entitled to it before signing.**")
j = t.index("**Interaction with P8, which is not yet settled.**")
NEWB6 = """**The consequence, stated plainly because the author is entitled to it before signing.**
*(Corrected R60/F3-B6. This paragraph previously read that "the Phase 1 gate row fails as things
stand", which contradicted this document's own failure-mode table three sections above. The table
is right and this was stale.)* Limb (i) compares each entry against **the originating experiment's
figure for its own key** \u2014 Phase 6 \u2014 **not** against the retired 0.957/0.675 pair. Against Phase 6
the pre-fix trio agrees to **|\u0394| \u2264 4.4e-5**, and the post-fix trio takes the no-counterpart branch
on the declaration's ex-ante ground. **The row does not fail on today's artifact.** What follows
from the hard fail is narrower and still real: an entry that later drifts off its originating
figure, or a post-fix entry whose ex-ante ground is not registered, denies the row.

"""
t = t[:i] + NEWB6 + t[j:]
p.write_text(t, encoding="utf-8")
print("J3: %d substitutions + \u00a75(b) rewritten" % len(SUBS))

# ---- propagate the row into H29, read out of J3 rather than retyped -----------
L = p.read_text(encoding="utf-8").split("\n")
s = next(i for i, l in enumerate(L) if l.startswith("> \u00a710.0 ordering followed"))
e = next(i for i in range(s, len(L))
         if L[i].rstrip().endswith("and a failure of either denies the row.**"))
row = re.sub(r"\s+", " ", " ".join(re.sub(r"^>\s?", "", x).strip() for x in L[s:e + 1])).strip()
assert "regression guard" not in row.lower(), "the unregistered category survived"
assert "the only one that is one-to-one" not in row, "the false uniqueness claim survived"

hp = D / "_X5_hunks_v2.json"
d = json.loads(hp.read_text(encoding="utf-8"))
tgt = [h for h in d["hunks"] if (h.get("operative_text") or "").startswith("| **1** | Availability model")]
assert len(tgt) == 1, "C1 hunk match %d" % len(tgt)
cells = tgt[0]["operative_text"].split("|")
tgt[0]["operative_text"] = "|".join(cells[:4]) + "| " + row + " |"
json.dump(d, open(hp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("H29 rebuilt from J3 (%d chars); category and uniqueness claim both absent" % len(row))
