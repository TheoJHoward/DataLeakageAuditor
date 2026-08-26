#!/usr/bin/env python3
"""DELTA R60/F3 - staleness pre-check on W6's six items, against CURRENT text.

Each is re-verified before any fix is attempted. OPEN = still there. CLOSED-INCIDENTALLY
= a later round's edit already closed it, with what closed it named. Fix only the OPEN.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

ssf = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8")
part1 = ssf[ssf.index("# PART 1"):ssf.index("# PART 2")]
part5 = ssf[ssf.index("# PART 5"):] if "# PART 5" in ssf else ""
j3 = (D / "J3_C1_REDRAFT.md").read_text(encoding="utf-8")
hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]
op = "\n".join((h.get("operative_text") or "") for h in hunks)
decl = REPO.joinpath("AVAILABILITY_DECLARATION.md").read_text(encoding="utf-8")
f3j = REPO.joinpath("evidence/fixture_spike/f3/fixture_manifest_DRAFT.json").read_text(encoding="utf-8")

R = []


def item(n, name, open_test, evidence, closed_by=None):
    st = "OPEN" if open_test else "CLOSED-INCIDENTALLY"
    R.append((n, name, st, evidence, closed_by or ""))


# --- B1: the category "regression guard" used with no registered rule creating it
cat_in_op = ("REGRESSION GUARD" in op) or ("regression guard" in op)
rule_in_part1 = ("regression guard" in part1.lower() and "(g)(1)" in part1)
item("B1a", "'regression guard' category used in operative text with no registered rule",
     cat_in_op and not rule_in_part1,
     "category in operative: %s; a rule creating it in PART 1: %s" % (cat_in_op, rule_in_part1))

# --- B1: (g)(1) asymmetry vs the row's symmetric statement
g1_asym = "not counted\n> as evidence that the phase's gate was met" in j3 or \
          "as evidence that the phase's gate was met" in j3
row_sym = "not counted toward it" in op or "not counted toward it" in j3
item("B1b", "(g)(1) asymmetric ('gate was met') vs row symmetric ('pass/fail evidence')",
     g1_asym and row_sym,
     "(g)(1) says 'gate was met': %s; row says 'pass/fail evidence ... not counted toward it': %s"
     % (g1_asym, row_sym))

# --- B3: the false uniqueness claim, and the two-artifact key
uniq = "the only one that is one-to-one" in op or "the only one that is one-to-one" in j3
item("B3a", "'the only one that is one-to-one' - false (the 4-field Phase 6 key already is)",
     uniq, "claim present in operative/J3: %s" % uniq)
key5 = "(side, instrument, architecture, horizon_s, tier)" in op
item("B3b", "the 5-tuple is a key of NEITHER artifact (Phase 6 has no side; f1 has no tier)",
     key5 and "is not a column of the originating record" not in op,
     "5-tuple present: %s; caveat naming side as not-a-column present: %s"
     % (key5, "is not a column of the originating record" in op))

# --- B4: J3 failure mode 4 still states a +-0.010 test the deferred-to clause does not create
fm4 = bool(re.search(r"misses its declared entry by more than \u00b10\.010", j3))
item("B4", "J3 failure mode 4 states a \u00b10.010 sliced test the deferred-to clause does not create",
     fm4, "failure-mode-4 wording present in J3: %s" % fm4)

# --- B5: (k2)'s two conditions - freeze enumeration and non-DRAFT status
freeze_lists_manifest = "fixture_manifest" in decl[decl.index("Specifically and exhaustively"):
                                                  decl.index("Specifically and exhaustively") + 3000] \
    if "Specifically and exhaustively" in decl else False
is_draft = '"manifest_status": "DRAFT' in f3j
item("B5", "(k2) requires the manifest in the SC-8(a) freeze and non-DRAFT at the tag; neither is true",
     (not freeze_lists_manifest) or is_draft,
     "freeze enumerates the manifest: %s; manifest_status still DRAFT: %s"
     % (freeze_lists_manifest, is_draft))

# --- B6: J3 s5(b) still says the row fails, contradicting its own table row 1
s5b_fails = "the Phase 1 gate row fails as things stand" in j3
tbl_notlive = "NO \u2014 NOT LIVE" in j3
item("B6", "J3 \u00a75(b) says the row fails while its own table row 1 says NOT LIVE",
     s5b_fails and tbl_notlive,
     "\u00a75(b) 'fails as things stand': %s; table row 1 'NO - NOT LIVE': %s" % (s5b_fails, tbl_notlive))

# --- PART 5 completeness claim vs SC-4(k)'s unlisted lines
claim = "Anything not listed is byte-identical to SSA" in part5
k_listed = "(k)" in part5 and "SC-4" in part5 and "(k1)" in part5
item("P5", "PART 5 claims completeness while SC-4(k)'s lines are an unlisted difference",
     claim and not k_listed,
     "completeness claim present: %s; (k) listed among the differences: %s" % (claim, k_listed))

print("  %-5s %-64s %s" % ("ITEM", "W6 FINDING", "STATUS"))
print("  " + "-" * 104)
nopen = 0
for n, name, st, ev, cb in R:
    if st == "OPEN":
        nopen += 1
    print("  %-5s %-64s %s" % (n, name[:64], st))
    print("        evidence: %s" % ev[:96])
print()
print("  OPEN: %d of %d   (fix only these)" % (nopen, len(R)))
