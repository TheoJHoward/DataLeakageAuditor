#!/usr/bin/env python3
"""DELTA R47 / P1 + P2 — the narrowest C2.

P1  contaminated limb byte-identical to registered v30; only the corrected limb
    rewritten in SC-3's vocabulary; ambiguity branch byte-exact.
P2  the contaminated-side tightening is DEFERRED ENTIRELY, not carried as a
    second amendment in v30a. Recorded as a future-amendment candidate.

Every edit asserts its match count. Nothing is forced.
"""
import json
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

# ---- the registered line, read from disk. Never from memory. ----------------
reg = REPO.joinpath("PREREG.md").read_text(encoding="utf-8").split("\n")[1021]
assert reg.startswith("3. Fires on `fixture_contaminated`"), reg[:60]

CONTAM = "3. Fires on `fixture_contaminated`"
BRANCH = reg[reg.index("**under the reconstructed"):]
assert BRANCH.endswith("**;"), BRANCH[-20:]
print("registered line 1022 read from disk, %d chars" % len(reg))
print("  contaminated limb carried : %r" % CONTAM)
print("  ambiguity branch carried  : %r" % BRANCH[:58] + "...")

NEW_OP = (
    CONTAM + ", and on `fixture_corrected` its runtime findings match the "
    "fixture's declared ground-truth map \u2014 findings the map predicts are "
    "required, findings it excludes are false positives, and cells the map does "
    "not cover are unscored \u2014 " + BRANCH)

# the two properties P1 demands, asserted rather than asserted-in-prose
assert NEW_OP.startswith(CONTAM), "contaminated limb not byte-identical"
assert BRANCH in NEW_OP, "ambiguity branch not byte-exact"
assert "every fixture side" not in NEW_OP, "the universal rewrite survived"

NEW_WC = (
    "\u00a710.1's criterion 3 is replaced so that the CORRECTED-SIDE limb asks the "
    "question SC-3 registers \u2014 whether a candidate's findings MATCH the declared "
    "map \u2014 instead of whether the candidate is SILENT there. **The "
    "contaminated-side limb `Fires on \u0060fixture_contaminated\u0060` is carried "
    "forward byte-identical to registered v30, and the ambiguity branch is carried "
    "byte-exact, em-dash included** \u2014 both verified at R47/P1 against "
    "`PREREG.md` line 1022 as read from disk.\n\n"
    "**Scope, and why it is this narrow (R47/P1\u2013P2).** An earlier revision of this "
    "draft also displaced the contaminated-side limb, rewriting it from EXISTENTIAL "
    "(\u201cfires\u201d \u2014 one finding anywhere on the contaminated side) to UNIVERSAL "
    "(\u201cmatch the map on **every** fixture side\u201d \u2014 a per-cell match across the "
    "whole declared scored population, plus a two-sided false-positive prohibition). "
    "That tightening is **not reached by this clause's stated reason**, which is "
    "entirely about the corrected side, and **no sentence of the amendment disclosed "
    "it**. It is WITHDRAWN from v30a and recorded as a candidate for a future "
    "amendment carrying its own stated reason and its own ledger row (HISTORY.md "
    "H-39). It may well be defensible on its merits; a tightening whose reason "
    "appears nowhere in the amendment carrying it is how a registration stops being "
    "trustworthy, and being defensible is not the test.\n\n"
    "The C2 retention block beneath item 3 preserves the superseded item verbatim. "
    "**Order (R39/F2):** this REPLACE is applied first; the retention blockquote is "
    "then written directly beneath the resulting operative item 3, before item 4.")

NEW_RET = (
    "   > **\u00a710.1 line 1022 (kill-gate criterion 3) \u2014 SUPERSEDED BY v30a, "
    "consequential to \u00a76.2 line 461. Registered v30 text, retained verbatim, NOT "
    "operative:** \"" + reg + "\" *Retired **as to its corrected-side limb only**, "
    "because that limb is a second copy of the premise criterion 3 (line 461) "
    "retires \u2014 that silence on the corrected side is the correct behaviour. Under "
    "SC-3 the corrected side is characterized, never clean, and a tool silent where "
    "the map declares a violation is silent where it should fire. **The "
    "contaminated-side limb and the ambiguity branch are carried into the operative "
    "item byte-identical** (R47/P1); the contaminated-side tightening an earlier "
    "draft carried is withdrawn from v30a and deferred (R47/P2, H-39). Recover the "
    "registered line byte-exact with `git show prereg-v30:PREREG.md`.*")

p = D / "_X5_hunks_v2.json"
d = json.loads(p.read_text(encoding="utf-8"))
nop = nret = 0
for h in d["hunks"]:
    cl = h.get("clause") or ""
    if cl.startswith("C2 operative"):
        assert "every** fixture side" in h["operative_text"], "C2 op not in the expected prior state"
        h["operative_text"], h["what_changes"] = NEW_OP, NEW_WC
        nop += 1
    elif cl.startswith("K2 \u00a79.2 \u2014 C2 retention"):
        assert h["operative_text"].lstrip().startswith("> **\u00a710.1 line 1022"), "retention not as expected"
        h["operative_text"] = NEW_RET
        nret += 1
assert nop == 1, "C2 operative matched %d times, expected 1" % nop
assert nret == 1, "C2 retention matched %d times, expected 1" % nret
json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("\nP1/P2 APPLIED  (operative %d, retention %d)" % (nop, nret))
print("\n--- NEW OPERATIVE ITEM 3 ---\n" + NEW_OP)
