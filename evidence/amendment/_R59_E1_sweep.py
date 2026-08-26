#!/usr/bin/env python3
"""DELTA R59/E1 - sweep for everything RECORDED that never LANDED.

The disclosures were established at R47 and lived only in ROUND_STATE for twelve rounds.
Anything in ROUND_STATE alone is at exactly that risk, and a staged file no ceremony step
applies is a record that does not exist.

For each item: WHERE IT IS NOW, and whether the ceremony will land it.
"""
import json
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

ssf = (D / "amendment" / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8")
part1 = ssf[ssf.index("# PART 1"):ssf.index("# PART 2")]
hunks = json.loads((D / "amendment" / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]
optext = "\n".join((h.get("operative_text") or "") for h in hunks)
hist = REPO.joinpath("HISTORY.md").read_text(encoding="utf-8")
devs = REPO.joinpath("DEVIATIONS.md").read_text(encoding="utf-8")
rs = (D / "ROUND_STATE.md").read_text(encoding="utf-8")
x4 = (D / "ceremony" / "X4_REGENERATION_REQUIREMENTS.md").read_text(encoding="utf-8")
cer = REPO.joinpath("evidence/ceremony/CEREMONY_COMMANDS.md").read_text(encoding="utf-8")
errata = D / "errata"
scratch_all = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                        for p in D.rglob("*.md") if p.is_file())


def where(needles, staged_hint=None):
    """Locate a record: registered text > staged repo file > scratch draft > ROUND_STATE > nowhere."""
    ns = needles if isinstance(needles, (list, tuple)) else [needles]
    if any(n in part1 or n in optext for n in ns):
        return "REGISTERED TEXT"
    if any(n in hist for n in ns):
        return "HISTORY.md (staged)"
    if any(n in devs for n in ns):
        return "DEVIATIONS.md (staged)"
    if staged_hint and (REPO / staged_hint).exists() and any(
            n in (REPO / staged_hint).read_text(encoding="utf-8", errors="replace") for n in ns):
        return "%s (staged)" % staged_hint
    if any(n in scratch_all for n in ns):
        return "scratch draft only"
    if any(n in rs for n in ns):
        return "ROUND_STATE ONLY"
    return "NOWHERE"


def on_landing_list(*keys):
    return "yes" if all(any(k in blob for blob in (x4, cer)) for k in keys) else "NO"


ITEMS = [
    ("\u00a710.1 missing third state (P10)",
     ["registers no third state", "\u00a710.1 registers no third state"], None, ("H-38",)),
    ("\u00a79.2 / \u00a711 conflict (Q3), l.107 quoted",
     ["could not both have been satisfied", "\u00a70.2.2 line 107"], None, ("D-003",)),
    ("twin-criterion-5 defect (H-37)",
     ["twin-criterion-5", "twin criterion 5", "two criteria numbered 5"], None, ("H-37",)),
    ("contaminated-side deferral (P2/H-39)",
     ["H-39", "contaminated-side tightening"], None, ("H-39",)),
    ("Z1/Z2/Z5 staged records",
     ["Z1_Z2_Z5", "Z1/Z2/Z5"], None, ("Z1",)),
    ("D-002 (timing)", ["D-002"], None, ("D-002",)),
    ("D-003 (\u00a79.2 comparison set)", ["D-003"], None, ("D-003",)),
    ("H-35 amendment ledger entry", ["H-35"], None, ("H-35",)),
    ("H-36 forecast note", ["H-36"], None, ("H-36",)),
    ("H-37 registration defect", ["H-37"], None, ("H-37",)),
    ("H-38 (\u00a710.1 third state)", ["H-38"], None, ("H-38",)),
    ("H-39 (deferred tightening)", ["H-39"], None, ("H-39",)),
    ("the seven disclosures (\u00a7AC)", ["WHAT THIS AMENDMENT DISCLOSES"], None, ("SC-1",)),
    ("K6 / killgate admitted to Phase 0", ["killgate"], None, ("killgate",)),
    ("W2b protocol (positive controls)", ["W2B_PROTOCOL", "positive control"], None, ("killgate",)),
]

print("  %-42s %-24s %s" % ("RECORD", "WHERE IT IS NOW", "ON CEREMONY LANDING LIST"))
print("  " + "-" * 100)
at_risk = []
for name, needles, hint, land in ITEMS:
    w = where(needles, hint)
    l = on_landing_list(*land)
    flag = ""
    if w in ("ROUND_STATE ONLY", "NOWHERE") or (w == "scratch draft only" and l == "NO"):
        flag = "   <-- AT RISK"
        at_risk.append(name)
    print("  %-42s %-24s %-4s%s" % (name[:42], w, l, flag))

print()
print("  DEVIATIONS.md is %d bytes  (D-001/2/3 are all DRAFTS until the ceremony writes them)"
      % len(devs.encode("utf-8")))
print("  HISTORY.md max H-number present: %s"
      % max([n for n in range(30, 45) if ("H-%d" % n) in hist] or [0]))
print()
print("  AT RISK (recorded but not landed, and not on a landing list): %d" % len(at_risk))
for a in at_risk:
    print("     - %s" % a)
