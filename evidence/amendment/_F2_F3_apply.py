#!/usr/bin/env python3
"""DELTA R39 items F2 and F3.

F2  A RETENTION IS NOT A REPLACEMENT. Lines 992 and 1022 both resolve to case (a):
    the ledger row asserts a real change, so the REPLACE is drafted and the existing
    retention block then preserves the superseded text for the record.

    992  — K2 section 9.1's own retention text says "Only the Gate cell is changed in
           the operative row ABOVE". That operative row was never drafted. Without it
           the Phase 1 gate still tests "both fixture AUCs ... full and sliced": "both"
           names the anchor pair H2 retires, and "sliced" names the artifact H4 moves
           off the Phase 0 fixture. Leaving it registered means Phase 1's gate tests a
           retired anchor and an artifact no longer in the fixture.
    1022 — K2 section 9.2 places its retention "beneath the operative item 3", which
           likewise does not exist. Without it the kill gate still asks whether a
           candidate "is silent on fixture_corrected" while the acceptance gate scores
           against a declared map on BOTH sides. A candidate could satisfy 10.1
           criterion 3 by being silent on the corrected side - the behaviour SC-3
           registers as wrong.

    Case (b) - deleting the rows - is available and is what K2 section 9 calls H1's
    alternative, but it leaves both defects registered. Recorded, not taken.

F3  Every hunk gains an operative_text field. Extracted from source, never paraphrased.
"""

import json
import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

ssf = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8")
dd = (D / "PREREG_v30a_DIFF.md").read_text(encoding="utf-8")
k2 = (D / "K2_AMENDMENT_LEDGER.md").read_text(encoding="utf-8")
prereg = (REPO / "PREREG.md").read_text(encoding="utf-8").split("\n")

src = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))
hunks, findings = src["hunks"], src["findings"]


def ln(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else None


# ---------------------------------------------------------------- F2
C1_REPLACE = (
    "| **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 "
    "comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and "
    "conformance suite frozen; detector protocol; report skeleton; the three controls and the "
    "determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed "
    "with the measurement; **every declared reference-anchor entry reproduces within its registered "
    "acceptance interval, recomputed from the fixture's committed bytes per §6.2 as amended**; "
    "**the sliced variant is produced by the padded slicer and its Phase 1 CI obligation is "
    "discharged, with its slice boundaries declared**; **all four alignment-control cases behave as "
    "§6.5 requires**; snapshots hashed |")

C2_REPLACE = (
    "3. Its runtime findings match the fixture's declared ground-truth map on **every** fixture "
    "side — findings the map predicts are required, findings it excludes are false positives, and "
    "cells the map does not cover are unscored — **under the reconstructed declaration, or, where "
    "the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;")

NEW = [
    dict(clause="C1 operative row (§10 Phase 1 gate cell) — drafted at R39/F2",
         prereg_line="992", operation="replace", anchor_verified=True,
         anchor_text=prereg[991],
         operative_text=C1_REPLACE,
         what_changes="The Phase 1 gate cell is replaced. Phase, Work and Est. are byte-identical; "
                      "only the Gate cell changes. \"both fixture AUCs reproduce within ±0.010, full "
                      "and sliced\" is replaced by two separate obligations: every declared "
                      "reference-anchor entry reproduces within its registered interval, recomputed "
                      "from committed bytes; and the sliced variant is produced and its Phase 1 CI "
                      "obligation discharged with slice boundaries declared. The C1 retention block "
                      "beneath the phase table preserves the superseded row verbatim.",
         justification="K2 §9.1's retention text asserts \"Only the Gate cell is changed in the "
                       "operative row above\" — an operative row that was never drafted. Without it "
                       "the retention block quotes a row that is still live in the table three lines "
                       "above it: two contradictory readings at one site, which is the defect "
                       "retention blocks exist to cure. The Gate cell also reads on two superseded "
                       "objects — \"both\" names the anchor pair H2 retires, \"sliced\" names the "
                       "artifact H4 moves off the Phase 0 fixture — so leaving it registered means "
                       "Phase 1's gate tests a retired anchor and an artifact no longer in the "
                       "fixture. The alternative K2 §9 records (reject C1, drop the ledger row, "
                       "revert line 992) is available and leaves both defects standing; it is not "
                       "taken.",
         class_="C (consequential) — derived from §A.1 and §A.4; carried with H2 and H4. Ledger "
                "table (a): §10 line 992."),
    dict(clause="C2 operative item (§10.1 kill-gate criterion 3) — drafted at R39/F2",
         prereg_line="1022", operation="replace", anchor_verified=True,
         anchor_text=prereg[1021],
         operative_text=C2_REPLACE,
         what_changes="§10.1's criterion 3 is replaced so the kill gate asks the question SC-3 "
                      "registers: whether a candidate's findings MATCH the declared map on every "
                      "side, rather than whether it is SILENT on the corrected side. The ambiguity "
                      "branch is carried through byte-for-byte. The C2 retention block beneath item "
                      "3 preserves the superseded item verbatim.",
         justification="§10.1's criterion 3 is a second copy of the premise §6.2's criterion 3 "
                       "retires — that silence on the corrected side is correct behaviour. Under "
                       "SC-3 the corrected side is CHARACTERIZED, never clean, so a tool silent "
                       "where the map declares a violation is silent where it should fire. Left "
                       "registered, a candidate tool could satisfy the kill gate by exhibiting "
                       "exactly the behaviour the acceptance gate now scores as a miss — and the "
                       "kill gate is the criterion that decides whether this project stops. The "
                       "retention block presupposes an \"operative item 3\" that was never drafted; "
                       "without it the block quotes text still live directly above it.",
         class_="C (consequential) — derived from §A.8; carried with SC-3. Ledger table (a): §10.1 "
               "line 1022."),
]
for n in NEW:
    n["class"] = n.pop("class_")
hunks += NEW
print(f"F2: +{len(NEW)} REPLACE hunks drafted (992, 1022) — both case (a)")

# ---------------------------------------------------------------- F3
def bq_after(text, marker, start=0):
    i = text.find(marker, start)
    if i < 0:
        return None
    out, started = [], False
    for l in text[i:].split("\n")[1:]:
        if l.startswith(">"):
            started = True
            out.append(re.sub(r"^>\s?", "", l))
        elif started and l.strip() == "":
            out.append("")
        elif started:
            break
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) if out else None


def clause_of(tag):
    m = re.search(rf"^### {re.escape(tag)} — ", ssf, re.M)
    return bq_after(ssf, "**THE CLAUSE.**", m.start()) if m else None


def fenced_after(text, marker, start=0):
    i = text.find(marker, start)
    if i < 0:
        return None
    seg = text[i:]
    f = seg.find("```")
    if f < 0:
        return None
    e = seg.find("```", f + 3)
    return seg[f + 3:e].strip("\n") if e > 0 else None


EXTRACT = {}
for t in ("SC-1", "SC-2", "SC-3", "SC-4", "SC-5", "SC-6", "SC-7", "SC-8", "SC-9",
          "SC-10", "SC-11", "SC-12", "SC-13a", "SC-13b", "SC-13c"):
    EXTRACT[t] = clause_of(t)
for lbl, mk in (("H2", "### H2 — "), ("H3", "### H3 — "), ("H4", "### H4 — ")):
    i = dd.find(mk)
    EXTRACT[lbl] = fenced_after(dd, "**REPLACE with", i) if i >= 0 else None
EXTRACT["C1ret"] = fenced_after(k2, "**9.1 — C1 (line 992).**")
EXTRACT["C2ret"] = fenced_after(k2, "**9.2 — C2 (line 1022).**")
EXTRACT["SC-12w"] = bq_after(ssf, "> **(w) ENTRY CONDITION FOR §7.7's `waived` COVERAGE STATE")
EXTRACT["BLOCK"] = k2[k2.index("<!-- K2-BLOCK-BEGIN -->") + 23:k2.index("<!-- K2-BLOCK-END -->")].strip()

filled = 0
for h in hunks:
    if h.get("operative_text"):
        continue
    cl = (h.get("clause") or "")
    key = None
    for t in sorted(EXTRACT, key=len, reverse=True):
        if cl.startswith(t) or (t in cl and t.startswith("SC-")):
            key = t
            break
    if cl.startswith("H2"):
        key = "H2"
    elif cl.startswith("H3"):
        key = "H3"
    elif cl.startswith("H4"):
        key = "H4"
    elif cl.startswith("K2 §9.1"):
        key = "C1ret"
    elif cl.startswith("K2 §9.2"):
        key = "C2ret"
    elif cl.startswith("K2 §8.2"):
        key = "BLOCK"
    elif "pointer, redrafted" in cl:
        h["operative_text"] = ("**`waived` is defined in §10.2 (v30a).** That definition governs the "
                               "word wherever it appears, including this table, and **SC-12(w) "
                               "registers the condition under which a detector-case may be reported "
                               "in this state.** Neither is restated here.")
        filled += 1
        continue
    if key and EXTRACT.get(key):
        h["operative_text"] = EXTRACT[key]
        filled += 1

missing = [h for h in hunks if not h.get("operative_text")]
print(f"F3: operative_text filled on {filled} hunk(s); {len(missing)} still without")
for h in missing:
    print(f"    MISSING  line {ln(h)}  {h.get('clause','')[:62]}")

hunks.sort(key=lambda h: (ln(h) or 9999))
json.dump({"hunks": hunks, "findings": findings},
          open(D / "_X5_hunks_v2.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"\nwrote _X5_hunks_v2.json: {len(hunks)} hunks")
