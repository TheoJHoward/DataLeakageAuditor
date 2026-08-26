#!/usr/bin/env python3
"""DELTA R48 / Q6 - rekey limb (i), and correct what P8 and Q5 falsify in J3.

Q6  "the same horizon and side" is a one-to-many key: (5s, pre) selects 16 rows
    spanning 0.5420-0.9662, 42x the tolerance. Rekey to
    (side, instrument = ZC, model = LightGBM, horizon).

AND a correction I owe. At R47/P7 I wrote that "the Phase 1 gate row FAILS ON
TODAY'S ARTIFACT", citing §A.1's "there is no horizon at which the registered
pair is reproduced". That conflated two different comparanda: limb (i) compares
each entry against the ORIGINATING experiment's figure for its own key - Phase 6 -
NOT against the retired registered pair 0.957/0.675, which is what H2 retires and
is not limb (i)'s target at all. Against Phase 6 the pre-fix trio agrees to
|d| <= 4.4e-5. The row does NOT fail today.

The consequence is not comfortable and is stated rather than buried: with both
operands frozen, limb (i) cannot fail - so under SC-8(g)'s OWN rule it is a
regression test and must be labelled one.
"""
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
p = D / "J3_C1_REDRAFT.md"
L = p.read_text(encoding="utf-8").split("\n")

# ---- Q6: rekey limb (i). Lines 85-92 (1-indexed) -----------------------------
assert L[84].startswith("> **the reference anchor holds on both limbs"), L[84][:60]
assert L[91].endswith("Phase 1 measurement, never after one; *(ii)* **INTEGRITY** \u2014 each entry is"), L[91][-50:]
NEW = [
 "> **the reference anchor holds on both limbs**: *(i)* **AGREEMENT \u2014 A REGISTERED REGRESSION",
 "> TEST, LABELLED AS ONE UNDER SC-8(g)** \u2014 each declared reference-anchor entry is compared",
 "> against the figure the originating experiment recorded **for the same `(side, instrument,",
 "> model family, horizon)`** \u2014 the key stated in full because `(horizon, side)` alone is",
 "> one-to-many and selects 16 rows spanning 0.5420\u20130.9662, **42\u00d7 the tolerance below** \u2014 and any",
 "> entry that does not reproduce that figure within \u00b10.010 absolute **fails this gate row**. An",
 "> entry whose originating figure is unavailable, or was produced under a different model",
 "> family, **also fails this gate row, unless the declaration registered that entry ex ante as",
 "> having no originating counterpart and stated why** \u2014 a ground declared before any Phase 1",
 "> measurement, never after one; *(ii)* **INTEGRITY \u2014 ALSO A REGRESSION TEST** \u2014 each entry is",
]
L[84:92] = NEW
print("Q6: limb (i) rekeyed, 8 lines -> %d" % len(NEW))

# ---- failure table rows 1 and 2 ---------------------------------------------
def repl_row(marker, new):
    hits = [i for i, ln in enumerate(L) if ln.startswith(marker)]
    assert len(hits) == 1, "%s match %d" % (marker, len(hits))
    L[hits[0]] = new
    return hits[0] + 1

r1 = repl_row("| 1 | **An anchor entry does not reproduce",
 "| 1 | **An anchor entry does not reproduce the originating experiment's figure to \u00b10.010.** | "
 "**NO \u2014 NOT LIVE, and this corrects R47/P7.** The originating record is **Phase 6** "
 "(`phase6_main_summary.csv`, ZC/LightGBM/L2): 0.9662 / 0.9400 / 0.8564. The declared pre-fix trio "
 "reproduces it to **|\u0394| \u2264 4.4e-5**, far inside \u00b10.010. \u00a7A.1's *\"no horizon at which the registered "
 "pair is reproduced\"* is about the **retired** 0.957/0.675 pair, which H2 retires and which is "
 "**not this limb's comparand**. The post-fix trio takes the no-counterpart branch on \u00a7A.1 item 4's "
 "ex-ante ground (R48/Q7). **Both operands are frozen, so this limb cannot fail on this artifact \u2014 "
 "it is a REGRESSION TEST and is labelled one.** It detects a swapped or corrupted fixture, which "
 "is worth having; it is not gate weight. |")

r2 = repl_row("| 2 | **A recomputed entry does not equal",
 "| 2 | **A recomputed entry does not equal its declared value.** | **Also a regression test.** "
 "Expected deviation 0.000000 and any non-zero is a stop-and-report. Detects byte corruption, a "
 "changed AUC routine, a mis-transcribed declaration \u2014 none of which the frozen artifact can "
 "produce by itself. Labelled under SC-8(g), not counted as gate weight. |")
print("failure table rows %d and %d corrected" % (r1, r2))

# ---- add the honest summary under the table ---------------------------------
anchor = "**The row is therefore failable on this fixture as it stands**, which the withdrawn draft"
hits = [i for i, ln in enumerate(L) if ln.startswith(anchor)]
assert len(hits) == 1, "summary match %d" % len(hits)
end = hits[0]
while not L[end].rstrip().endswith("moment the floor is registered."):
    end += 1
NEWSUM = """**WHAT ACTUALLY CARRIES GATE WEIGHT, after R48.** Failure modes 1 and 2 are **regression tests**:
both operands are frozen, so neither can fail on this artifact, and SC-8(g) requires them to be
labelled rather than counted \u2014 *"an item whose outcome is determined by the frozen artifact before
the phase opens is not a gate item; it is a regression test, and it is labelled as one where it is
written."* **This draft now labels them.**

**The row remains failable, on other limbs**, and this is where its weight actually sits:

- **the separation floor (failure 3)** \u2014 failable the moment a floor is registered, and **live**:
  declared deltas 0.034708 / 0.183464 / 0.177131. **The floor is P6 and is the author's; it is not
  set here.**
- **the sliced variant (failure 4)** \u2014 genuinely open, because the padded slicer is Phase 1 work
  that does not yet exist. This is the limb most likely to fail on its merits.
- **the alignment controls and snapshot hashing (failure 5)**, and the \u00a710.0 ordering and
  claims-verified clauses that open the row.

**Stated plainly for the author:** if the separation floor is declared a context figure with no
pass/fail consequence (P6's recommendation), then of this row's *anchor* content **nothing is
failable on a frozen artifact** \u2014 the anchor becomes a regression suite and the row's live weight
is the sliced variant, the alignment controls and the ordering clauses. That may well be the right
design; it should be chosen knowingly rather than arrived at."""
L[hits[0]:end + 1] = NEWSUM.split("\n")
print("failability summary rewritten (%d lines)" % len(NEWSUM.split("\n")))

# ---- §5(c): settled ----------------------------------------------------------
start = next(i for i, ln in enumerate(L) if ln.startswith("**(c) Where does the originating figure come from?**"))
end = next(i for i in range(start, len(L)) if L[i].rstrip().endswith("by accident."))
NEWC = """**(c) Where the originating figure comes from \u2014 SETTLED at R48/Q5 and Q7; no longer open.** The
originating record is **Phase 6**: `results\\pc2_all_phases\\phase6\\second_pc\\phase6_main_summary.csv`,
keyed (`instrument`, `architecture`, `horizon_s`, `tier`), 96 rows, four instruments (NQ, GC, ZC, ZS),
both families. ZC / LightGBM / L2 gives **0.9662 / 0.9400 / 0.8564** at 5s / 10s / 30s.

**3 of 6 declared entries have a counterpart.** The three post-fix entries have none and none can
exist \u2014 the universal-lag correction that defines that side was first applied in Phase 7 itself.
Registered **ex ante** at declaration \u00a7A.1 item 4 (R48/Q7), so the no-counterpart branch is
exercised deliberately, on a stated ground, rather than by accident.

**Transcription refuted (R48/Q5).** Phase 7 re-derived: it trains its own models, reads no Phase 6
output, and Phase 6 stored no predictions to copy. The 32 byte-identical `shuffle_mean` values are
the expected output of **fixed seeds [42, 123, 456]**, not evidence of copying. **Not established:**
no Phase 6 script survives, so whether the agreement is deterministic identity or independent
convergence cannot be settled from the artifacts \u2014 which is one more reason limb (i) is labelled a
regression test rather than an agreement gate."""
L[start:end + 1] = NEWC.split("\n")
print("\u00a75(c) settled")

p.write_text("\n".join(L), encoding="utf-8")
print("\nJ3_C1_REDRAFT.md now %d lines" % len(L))
