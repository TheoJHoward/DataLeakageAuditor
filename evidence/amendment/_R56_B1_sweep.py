#!/usr/bin/env python3
"""DELTA R56/B1 - sweep every correction ordered since R47 for the two-field split.

Q4's failure was found because the author happened to ask about that one claim. Each
correction below is re-verified in the field that SHIPS, not the field that explains.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]
decl = REPO.joinpath("AVAILABILITY_DECLARATION.md").read_text(encoding="utf-8")
cer = REPO.joinpath("evidence/ceremony/CEREMONY_COMMANDS.md").read_text(encoding="utf-8")
prereg = REPO.joinpath("PREREG.md").read_text(encoding="utf-8").split("\n")
ssf = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8")

results = []


def rep(name, verdict, detail):
    results.append((name, verdict, detail))


# 1 -- the em-dash byte-exactness fix (R46/J4c) --------------------------------
reg1022 = prereg[1021]
branch = reg1022[reg1022.index("**under the reconstructed"):]
c2 = [h for h in hunks if (h.get("clause") or "").startswith("C2 operative")]
if not c2:
    rep("em-dash byte-exactness (C2 branch)", "NOT-APPLICABLE", "C2 operative hunk not found")
else:
    op = c2[0]["operative_text"]
    in_op = branch in op
    claim = "byte-exact, em-dash included" in (c2[0].get("what_changes") or "")
    rep("em-dash byte-exactness (C2 branch)",
        "LANDED-IN-OPERATIVE" if in_op else "COMMENTARY-ONLY",
        "branch byte-exact in operative_text: %s; commentary claims it: %s" % (in_op, claim))

# 2 -- §A.5's correction (R48/Q2) ---------------------------------------------
dead = "**SATISFIED.** This whole file is a Phase 0 product; no cross-tool comparison has been run."
live_new = "A cross-tool comparison WAS executed on 14 August 2026"
rep("\u00a7A.5 cross-tool statement (Q2)",
    "LANDED-IN-OPERATIVE" if (dead not in decl and live_new in decl) else "COMMENTARY-ONLY",
    "old assertion present: %s; corrected assertion present: %s" % (dead in decl, live_new in decl))

# 3 -- §A.1 item 2 (R48/Q4) ----------------------------------------------------
fam_live = "**The model family changes: XGBoost \u2192 LightGBM.**"
fam_new = "The registered anchor names no model family; this declaration names one."
rep("\u00a7A.1 item 2 model family (Q4)",
    "LANDED-IN-OPERATIVE" if (fam_live not in decl and fam_new in decl) else "COMMENTARY-ONLY",
    "old heading present: %s; corrected heading present: %s" % (fam_live in decl, fam_new in decl))

# 3b -- the same claim inside the AMENDMENT's operative text (R55/W5) ----------
live_hits = []
for h in hunks:
    op = h.get("operative_text") or ""
    for m in re.finditer(re.escape("the anchor's model family changed"), op):
        a, b = max(0, m.start() - 320), min(len(op), m.end() + 320)
        ctx = op[a:b]
        lo = max(ctx.rfind('"', 0, m.start() - a), ctx.rfind("\u201c", 0, m.start() - a))
        hi = max(ctx.find('"', m.end() - a), ctx.find("\u201d", m.end() - a))
        if not (lo >= 0 and hi >= 0):
            live_hits.append((h.get("clause") or "")[:30])
rep("model-family claim in AMENDMENT operative text (W5)",
    "LANDED-IN-OPERATIVE" if not live_hits else "COMMENTARY-ONLY",
    "live (unquoted) assertions remaining: %d %s" % (len(live_hits), live_hits or ""))

# 4 -- the three false §9.2 statements (R48/Q2) --------------------------------
d1 = "no cross-tool comparison has been run"
rep("declaration \u00a7A.5 line ~1041 (Q2)",
    "LANDED-IN-OPERATIVE" if decl.count(d1) <= 1 else "COMMENTARY-ONLY",
    "occurrences of the false phrase: %d (1 permitted: quoted inside the correction)" % decl.count(d1))

d2 = "| Reconstruction in Phase 0, before cross-tool | 448 | SATISFIED |"
rep("declaration walk-summary line ~1586 (Q2)",
    "LANDED-IN-OPERATIVE" if d2 not in decl else "COMMENTARY-ONLY",
    "bare SATISFIED row present: %s" % (d2 in decl))

d3 = "| **Cross-tool comparison per \u00a79.2** | **NOT RUN** |"
rep("CEREMONY_COMMANDS.md line 28 (Q2)",
    "LANDED-IN-OPERATIVE" if d3 not in cer else "COMMENTARY-ONLY",
    "bare NOT RUN row present: %s" % (d3 in cer))

# 5 -- the C6 re-scoping (W2) --------------------------------------------------
kg = D.parent / "killgate" / "k6" / "K6_RESULTS.md"
c6_strong = "five tools" in kg.read_text(encoding="utf-8") if kg.exists() else None
cited_repo = ("five tools" in decl) or ("five tools" in cer)
rep("C6 re-scoping (W2)",
    "NOT-APPLICABLE" if not cited_repo else "COMMENTARY-ONLY",
    "strong claim still in K6_RESULTS.md: %s; cited in declaration/ceremony: %s "
    "(W2 is a separate track and NOT YET DONE)" % (c6_strong, cited_repo))

# 6 -- the line-459 marker (R54/W3) -------------------------------------------
old459 = "**\u00a76.2 line 459 \u2014 v30a, ADDED NOT SUPERSEDED.** Criterion 1 stands byte-exact."
new459 = "THE TEXT IS UNCHANGED; THE REQUIREMENT IS NOT."
in_src = (old459 not in ssf) and (new459 in ssf)
in_hunk = any(new459 in (h.get("operative_text") or "") for h in hunks)
rep("line-459 marker (W3)",
    "LANDED-IN-OPERATIVE" if (in_src and in_hunk) else "COMMENTARY-ONLY",
    "corrected in source: %s; corrected in a hunk's operative_text: %s" % (in_src, in_hunk))

print("  %-52s %-20s %s" % ("CORRECTION", "VERDICT", "EVIDENCE"))
print("  " + "-" * 118)
bad = 0
for name, verdict, detail in results:
    flag = "" if verdict != "COMMENTARY-ONLY" else "  <-- "
    if verdict == "COMMENTARY-ONLY":
        bad += 1
    print("  %-52s %-20s %s%s" % (name[:52], verdict, detail[:60], flag))
print()
print("  COMMENTARY-ONLY (correction did not reach the operative field): %d" % bad)
