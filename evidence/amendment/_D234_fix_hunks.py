#!/usr/bin/env python3
"""DELTA R37 items D2, D3, D4 — correct the hunk set.

D2  the five ledger rows with no hunk: each classified, none manufactured.
D3  one operation per line; H5 removed as superseded, H4 KEPT and its order stated.
D4  marker anchors re-anchored to complete-block boundaries.
"""

import json
import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

src = json.loads((D / "_X5_hunks.json").read_text(encoding="utf-8"))
hunks, findings = src["hunks"], src["findings"]


def ln(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else None


# ------------------------------------------------------------------ D3a: dedup
# The clause batches and the block batch each reported the same pointer/marker
# hunks, so the set carried duplicates. Drop the less current of each pair.
DROP = [
    (816, "§13c-P — SC-13c insertion point 2"),   # dup of the SC-13c entry
    (856, "SC-12(w)"),                             # the H8 pointer, superseded by the redraft
    (915, "S2(i) — SC-6 insertion point 2"),       # dup of the SC-6 marker+insert pair
    (961, "S2(iii) — SC-11 insertion point"),      # dup of the SC-11 entry
]
before = len(hunks)
kept = []
dropped = []
for h in hunks:
    cl = (h.get("clause") or "")
    # EXACT clause match for the 856 pair: "SC-12(w)" is the superseded H8 pointer;
    # "SC-12(w) consequential ..." is the redraft that must SURVIVE. startswith()
    # matched both and dropped the survivor.
    hit = next((d for d in DROP if ln(h) == d[0]
                and (cl == d[1] if d[0] == 856 else cl.startswith(d[1]))), None)
    (dropped if hit else kept).append(h)
hunks = kept
print(f"D3a dedup: {before} -> {len(hunks)}  ({len(dropped)} duplicate(s) removed)")
for h in dropped:
    print(f"    dropped line {ln(h):<5} {h.get('clause','')[:64]}")

# ------------------------------------------------------------------ D2: add the five
NEW = [
    dict(clause="H2 (schema layer: SC-2(d))", prereg_line="445", operation="replace",
         anchor_text="- **Reference AUC:** 0.957 and 0.675, **acceptance interval \u00b10.010 absolute**. The gate runs in `full` mode.",
         anchor_verified=True,
         what_changes="Line 445 is replaced by a four-line block: the operative v30a bullet, then a nested quote retaining the registered v30 sentence verbatim and marked NOT operative, then its retirement reason. The anchor becomes constituted by recomputation from the fixture's own stored per-row prediction and outcome columns, declared as an enumerated set of entries; the \u00b10.010 interval and `full` mode carry over unchanged.",
         justification="The registered anchor is a transcribed pair of numbers, and no horizon of the declared fixture reproduces it \u2014 the anchor's model family changed. A transcribed figure cannot be re-derived, so a disagreement between it and the artifact has no resolution procedure. Recomputation from committed bytes is a pure function of the artifact, so the anchor becomes checkable and a deviation approaching the interval becomes a stop-and-report rather than a pass. Text drafted at PREREG_v30a_DIFF.md H2; SC-2(d) is the schema layer over it, not a replacement for it.",
         class_="C \u2014 \u00a70.2.1 line 93 (it changes what a published number means and how an acceptance interval is applied). Ledger table (a): \u00a76.2 line 445."),
    dict(clause="H3 (schema layer: SC-2, SC-9(b))", prereg_line="450", operation="replace",
         anchor_text="- **Contamination availability class** recorded in the manifest.",
         anchor_verified=True,
         what_changes="Line 450 is replaced by a four-line block on the same shape as H2. The recording locus moves from the manifest to the reconstructed availability declaration \u2014 a file the amended tag message hashes \u2014 and the clause forbids an evidence artifact from carrying a declaration. The ground-truth column DAG and the count of independently leaking sources stay manifest content.",
         justification="A manifest is the product of a dated measurement round and records what was measured. Writing a declaration into it makes a measurement record carry a decision, and an evidence artifact is never adjusted toward a decision. Moving the locus to the declaration binds harder than the manifest did, because the tag hashes the declaration and so freezes the class at the tag; moving it afterwards becomes itself class C. The clause states explicitly that it moves the locus of one element and nothing else. Text drafted at PREREG_v30a_DIFF.md H3.",
         class_="C \u2014 \u00a70.2.1 line 93 (it changes where a declared gate input lives and what may carry it). Ledger table (a): \u00a76.2 line 450."),
    dict(clause="H4 (schema layer: SC-2(e), SC-3(f))", prereg_line="451",
         operation="replace",
         anchor_text="- **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.",
         anchor_verified=True,
         what_changes="Line 451 is replaced by a four-line block on the same shape as H2 and H3. The sliced variant leaves the Phase 0 acceptance fixture and is re-registered as a Phase 1 CI obligation with its scoring rule declared ex ante. **SC-2's clause block is inserted AFTER this replacement block, not after the registered line** \u2014 see the order note below.",
         justification="The registered clause requires an artifact produced by a component of the tool under development, while \u00a70.2.1 line 95 requires this amendment to be committed before that component exists. An element that cannot be satisfied at the instant it must be committed is amended explicitly \u2014 leaving it outstanding invites it to be quietly re-read as satisfied later, which is the failure \u00a72.7 exists to stop. The scoring rule is declared now precisely so it cannot be chosen after a result is seen. **ORDER, load-bearing (R37/D3):** H4 is the only operation on line 451 itself; SC-2 inserts after the block H4 produces. Applied the other way round, SC-2's anchor re-derivation finds the registered line gone \u2014 it survives only inside H4's retained nested quote \u2014 and the applier refuses on zero matches, which is the applier working correctly.",
         class_="C \u2014 \u00a70.2.1 line 93 (it moves an acceptance-criteria artifact between phases and registers its scoring rule). Ledger table (a): \u00a76.2 line 451."),
    dict(clause="C1 retention block (K2 \u00a79.1)", prereg_line="992", operation="insert",
         anchor_text="| **1** | Availability model and profiles; **verification of \u00a70.3 Claims A\u2013C and the \u00a76.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2\u20133 wknds | \u00a710.0 ordering followed; claims verified or a deviation filed with the measurement; both fixture AUCs reproduce within \u00b10.010, full and sliced; **all four alignment-control cases behave as \u00a76.5 requires**; snapshots hashed |",
         anchor_verified=True,
         what_changes="A retention blockquote is inserted immediately after the phase table's last row (after line 998, before line 1000), retaining the Phase 1 gate row verbatim and marked NOT operative, with its retirement reason and the `git show prereg-v30:PREREG.md` recovery command. It is placed outside the table because a blockquote inside a table breaks it.",
         justification="The Phase 1 gate cell reads on two superseded objects: \"both\" names the retired anchor pair of line 445, and \"sliced\" names the artifact line 451 moves off the Phase 0 fixture. Without this retention the amendments block's own item 1 \u2014 \"No registered sentence is deleted from this file\" \u2014 is false, because table (a) heads itself \"each retained verbatim at its site\". Only the Gate cell changes; Phase, Work and Est. are byte-identical. Text drafted at K2_AMENDMENT_LEDGER.md \u00a79.1.",
         class_="C (consequential) \u2014 derived from \u00a7A.1 and \u00a7A.4; not walk-cited. Ledger table (a): \u00a710 line 992."),
    dict(clause="C2 retention block (K2 \u00a79.2)", prereg_line="1022", operation="insert",
         anchor_text="3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration \u2014 or, where the fixture is semantically ambiguous (\u00a76.2), under the labelled hypothetical declaration**;",
         anchor_verified=True,
         what_changes="A retention blockquote is placed directly beneath \u00a710.1's operative item 3, at the list's three-space indentation and before item 4, retaining the registered kill-gate criterion 3 verbatim and marked NOT operative.",
         justification="\u00a710.1's criterion 3 reads on \u00a76.2's criterion 3, which SC-3 replaces: the registered wording tests silence on the corrected side, while the amended criterion scores against a declared per-cell map on both sides. Leaving the old wording operative would leave the kill gate testing a premise the acceptance gate no longer uses. This is the inbound-reference cure, and it is the same shape the open finding at line 1035 asks about. Text drafted at K2_AMENDMENT_LEDGER.md \u00a79.2.",
         class_="C (consequential) \u2014 derived from \u00a7A.8; not walk-cited. Ledger table (a): \u00a710.1 line 1022."),
]
for n in NEW:
    n["class"] = n.pop("class_")
hunks += NEW
print(f"\nD2 add: +{len(NEW)} hunks for the five ledger rows (all COVERED; none manufactured)")

# ------------------------------------------------------------------ D4: re-anchor markers
RULE = ("Marker placement rule (R37/D4): a supersession marker attaches to a COMPLETE BLOCK "
        "\u2014 a whole paragraph, a whole table, or a whole list \u2014 never inside one. "
        "A marker written inside a table breaks the table; inside a list it breaks the list.")
REANCHOR = {205: (212, "\u00a72.3's `AvailabilityModel` table runs 201\u2013212; the marker is written after line 212, before line 214."),
            459: (462, "\u00a76.2's criteria list item 1 runs 459\u2013462; the marker is written after line 462."),
            1050: (1054, "\u00a711's item list runs to item 7 at line 1054; the marker is written beneath the list, after line 1054.")}
n_fixed = 0
for h in hunks:
    if h.get("operation") != "marker":
        continue
    n = ln(h)
    if n in REANCHOR:
        tgt, why = REANCHOR[n]
        h["prereg_line"] = f"{n} (marker written at line {tgt}, the end of its block)"
        h["what_changes"] = (h.get("what_changes", "") +
                             f"  **Placement (R37/D4):** {why} {RULE}")
        h["anchor_verified"] = True
        n_fixed += 1
print(f"\nD4 re-anchor: {n_fixed} marker(s) moved to a complete-block boundary")
for n, (tgt, why) in REANCHOR.items():
    print(f"    line {n} -> written at {tgt}: {why}")

# ------------------------------------------------------------------ order note at 1035
for h in hunks:
    if ln(h) == 1035 and (h.get("clause") or "").startswith("SC-13b"):
        h["prereg_line"] = "1035 (after SC-12's inserted block; before line 1036)"

hunks.sort(key=lambda h: (ln(h) or 9999))
out = D / "_X5_hunks_v2.json"
json.dump({"hunks": hunks, "findings": findings}, open(out, "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(f"\nwrote {out.name}: {len(hunks)} hunks")
