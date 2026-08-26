#!/usr/bin/env python3
"""LEDGER-CITATION RESOLUTION.  DELTA R59/E1.

Operative text cites ledger entries - `HISTORY.md` H-nn, `DEVIATIONS.md` D-nnn. A citation
to an entry that does not exist and that **no ceremony step will write** is the SC-8(g)
defect in a different file: text resting on authority that is not there.

THREE STATES, and only one is a defect:

  RESOLVED - the entry exists in the ledger now.
  PENDING  - the entry does not exist yet, but a ceremony step is on record to write it.
             Legitimate: the ledger takes ONE hashed state at the ceremony rather than
             several unhashed ones. Reported every run so the count stays visible, and
             carried into the ceremony as a gate that must clear before the tag.
  ORPHAN   - the entry does not exist and NOTHING will write it. **Defect.** This is how
             a record that "was decided" ends up existing nowhere - the shape that left
             the seven disclosures in ROUND_STATE alone for twelve rounds.

The check FAILS on ORPHAN only. PENDING is surfaced, never silently accepted, because a
pending citation that the ceremony forgets becomes an orphan at exactly the moment nobody
is looking.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

CITE = re.compile(r"\b(H-\d{1,3}|D-\d{3})\b")


def run(verbose=True):
    hunks = json.loads((D / "amendment" / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]
    op = "\n".join((h.get("operative_text") or "") for h in hunks)
    ssf = (D / "amendment" / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8")
    part1 = ssf[ssf.index("# PART 1"):ssf.index("# PART 2")]
    hist = REPO.joinpath("HISTORY.md").read_text(encoding="utf-8")
    devs = REPO.joinpath("DEVIATIONS.md").read_text(encoding="utf-8")
    x4 = (D / "ceremony" / "X4_REGENERATION_REQUIREMENTS.md").read_text(encoding="utf-8")
    cer = REPO.joinpath("evidence/ceremony/CEREMONY_COMMANDS.md").read_text(encoding="utf-8")
    plan = x4 + "\n" + cer

    cites = sorted(set(CITE.findall(op)) | set(CITE.findall(part1)))
    resolved, pending, orphan = [], [], []
    for c in cites:
        if c.startswith("H-"):
            written = bool(re.search(r"^###\s+%s\b" % re.escape(c), hist, re.M))
        else:
            written = c in devs
        if written:
            resolved.append(c)
        elif c in plan:
            pending.append(c)
        else:
            orphan.append(c)

    if verbose:
        print("  ledger entries cited by operative text: %d  %s" % (len(cites), cites))
        print("  RESOLVED (exist in the ledger now)      : %d  %s" % (len(resolved), resolved))
        print("  PENDING  (a ceremony step will write it): %d  %s" % (len(pending), pending))
        print("  ORPHAN   (nothing will write it)        : %d  %s" % (len(orphan), orphan))
        if orphan:
            print("    *** operative text cites authority that does not exist and is unplanned ***")
        elif pending:
            print("  PASS \u2014 no orphan citation. **CEREMONY GATE: every PENDING entry above must")
            print("  exist in its ledger before the tag**, or the amendment ships citing nothing.")
        else:
            print("  PASS \u2014 every ledger citation resolves now")
    return orphan


if __name__ == "__main__":
    import sys
    sys.exit(1 if run() else 0)
