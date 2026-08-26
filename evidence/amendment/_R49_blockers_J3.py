#!/usr/bin/env python3
"""DELTA R49 / R6 blockers B1, B3, B4, B6 - all in J3_C1_REDRAFT.md.

B1  (k4) cites SC-8(g), which is NOT registered - SC-8's applied text runs (a)-(f).
    The only two occurrences of "SC-8(g)" in the source are my own citations. Fixed
    in the SC-4(k) script; here the limb labels that lean on it are re-grounded too.
B3  the anchor key omits `tier`, and omitting it DECIDES the 30s outcome: against the
    declared 0.856419, L1 |d|=0.026519 FAIL, L2 0.000019 PASS, L3 0.010181 FAIL.
B4  the sliced limb's +-0.010 has no comparand and changes a scoring rule SC-2(e)
    requires to be fixed at the move.
B6  the "different model family" branch is unreachable (the comparand is SELECTED by
    model family) AND rests on the claim R48/Q4 withdrew. Q4 told me to re-ground both
    dependents; I fixed H2 and the failure table and missed these two sites.
"""
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
p = D / "J3_C1_REDRAFT.md"
L = p.read_text(encoding="utf-8").split("\n")

# ---- the operative row: B1 label, B3 key, B4 sliced limb, B6 branch ---------
start = next(i for i, l in enumerate(L) if l.startswith("> §10.0 ordering followed"))
end = next(i for i in range(start, len(L)) if L[i].rstrip().endswith("snapshots hashed"))
assert end - start == 17, "operative row spans %d lines" % (end - start + 1)

NEW = '''> §10.0 ordering followed; claims verified or a deviation filed with the measurement;
> **the reference anchor holds on both limbs**: *(i)* **AGREEMENT \u2014 A REGRESSION GUARD, AND
> LABELLED ONE. What it guards against: a substituted, regenerated or corrupted fixture, which
> would move the recomputed entry off the figure the originating experiment recorded.** Each
> declared reference-anchor entry is compared against that figure **for the same
> `(side, instrument, architecture, horizon_s, tier)`** \u2014 the key stated in full because it is
> the only one that is one-to-one: `(horizon, side)` alone selects 16 rows spanning
> 0.5420\u20130.9662, **42\u00d7 the tolerance below**, and dropping `tier` leaves three rows per
> combination whose 30s values are 0.8299 / 0.8564 / 0.8666 \u2014 **two of the three fail \u00b10.010
> against the declared entry, so the key decides the outcome.** `tier` is the declared **L2**;
> `side` selects the declared entry and is not a column of the originating record. Any entry
> that does not reproduce its figure within \u00b10.010 absolute **fails this gate row**. An entry
> whose originating figure is **unavailable** fails this gate row **unless the declaration
> registered that entry ex ante as having no originating counterpart and stated why** \u2014 a
> ground declared before any Phase 1 measurement, never after one; *(ii)* **INTEGRITY \u2014 ALSO A
> REGRESSION GUARD, guarding against byte corruption of the committed fixture or a changed AUC
> routine** \u2014 each entry is recomputed from the fixture's committed bytes and must equal its
> declared value exactly, a deviation of any size being a defect in the recomputation and a
> stop-and-report;
> **the declared pre-fix/post-fix separation is stated per horizon and side as a PUBLISHED
> CONTEXT FIGURE, carrying no pass/fail consequence** (R49/R1);
> **the sliced variant's Phase 1 CI obligation is discharged and the variant is scored under
> \u00a76.2 (v30a) "Sliced variant \u2014 operative"**, whose ex-ante scoring rule governs it, with its
> slice boundaries declared;
> **all four alignment-control cases behave as \u00a76.5 requires**; snapshots hashed
>
> **THE PASS/FAIL EVIDENCE FOR THIS ROW** is carried by the sliced variant, the four
> alignment-control cases, the snapshot hashing, and the \u00a710.0 ordering and claims-verified
> clauses. Limbs (i) and (ii) are guards and are not counted toward it.'''
L[start:end + 1] = NEW.split("\n")
print("B1/B3/B4/B6: operative row rewritten (%d lines)" % len(NEW.split("\n")))

# ---- B6: s1(b) rests on the withdrawn claim ---------------------------------
s = next(i for i, l in enumerate(L) if l.startswith("**(b) The one substantive discrepancy became a disclosure duty.**"))
e = next(i for i in range(s, len(L)) if L[i].rstrip().endswith("which C1 did not carry into the gate cell at all."))
NEWB = '''**(b) WITHDRAWN at R49 \u2014 this ground does not survive R48/Q4.** This paragraph read: *"The one
substantive discrepancy became a disclosure duty. The anchor's model family changed \u2014 XGBoost \u2192
LightGBM (\u00a7A.1 item 2)."* **\u00a7A.1 item 2 was corrected on 21 August 2026 and now says the opposite**:
the cited source names six architectures with LightGBM listed first, and **no family changed**. The
paragraph cited the very item that withdraws it. R48/Q4 required both dependents of that claim to be
re-grounded; H2's justification and the failure-mode table were, and **these two sites were missed
until the R49/R6 verification found them.** The withdrawal costs the C1 case nothing: defects (a),
(c) and (d) are independent and (a) is fatal on its own.'''
L[s:e + 1] = NEWB.split("\n")
print("B6: \u00a71(b) withdrawn and re-grounded")

p.write_text("\n".join(L), encoding="utf-8")
print("J3_C1_REDRAFT.md now %d lines" % len(L))
