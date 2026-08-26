#!/usr/bin/env python3
"""DELTA R49 - R2 (refine SC-8(g)) and R1 (P6 ruled: separation is a context figure).

R2 is H-L13's refinement applied to a different clause: the first draft collapsed two
different objects into one prohibition, and enforcing it literally would have deleted a
real substitution detector.

R1 is a DISCLOSED REDUCTION, not a silent one. The registered v30 row entailed a 0.282
separation by requiring both 0.957 and 0.675 to +-0.010. Dropping the floor removes that.
The author has ruled it out on stated grounds and the clause says so - which is exactly
what R47/P2 demanded of a change in the opposite direction.
"""
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
p = D / "J3_C1_REDRAFT.md"
L = p.read_text(encoding="utf-8").split("\n")

# ---------------------------------------------------------------- R2: SC-8(g)
start = next(i for i, l in enumerate(L) if l.startswith("> **(g) A GATE ITEM THE FIXTURE CANNOT FAIL"))
end = next(i for i in range(start, len(L))
           if L[i].rstrip().endswith("without the replacement stating what the artifact must now do to fail it.**"))
NEW_G = '''> **(g) EVERY GATE ITEM STATES WHAT MAKES IT FAIL \u2014 AND AN ITEM THAT CANNOT FAIL IS ONE OF
> TWO THINGS, ONLY ONE OF WHICH IS A DEFECT.** Every gate item states, in its own text or in
> the clause it cites, **the condition under which it fails** \u2014 an observation that is
> possible, that the artifact under test could produce, and that would deny the gate.
>
> **(g)(1) REGRESSION GUARD \u2014 legitimate, and LABELLED.** An item that cannot fail *given
> correct behaviour of a frozen artifact*, but that **would** fail on corruption,
> substitution, or drift in what it reads, is a **regression guard**. It is legitimate and it
> is kept. It is **labelled a regression guard where it is written**, and it **states what it
> guards against** \u2014 the specific change in the world that would trip it. It is **not counted
> as evidence that the phase's gate was met.**
>
> **(g)(2) DECORATION \u2014 removed.** An item that cannot fail under **any** state of the world
> \u2014 because both sides of its comparison are the same bytes, or because its condition is a
> tautology \u2014 is decoration. It is **removed**, not labelled.
>
> **(g)(3) A ROW CARRYING GUARDS NAMES WHERE ITS PASS/FAIL EVIDENCE COMES FROM.** Where a gate
> row contains regression guards, the row **names the items that carry its pass/fail evidence**
> \u2014 those whose outcome is not determined before the phase opens. Without that sentence a
> reader concludes the row is empty.
>
> Where an item's failure condition is a comparison, the quantity compared against is **named
> and its origin stated** \u2014 a target derived from the same bytes the item tests is an
> integrity check, not an agreement check, and the two may not be substituted for one another.
> **A registered item the artifact currently fails may not be replaced by one it passes, in
> the same amendment, without the replacement stating what the artifact must now do to fail
> it.**'''
L[start:end + 1] = NEW_G.split("\n")
print("R2: SC-8(g) refined into (g)(1) guard / (g)(2) decoration / (g)(3) evidence-naming")

WHY = next(i for i, l in enumerate(L) if l.startswith("**Why the last sentence.**"))
L.insert(WHY, '''**Why (g)(1) and (g)(2) are separated \u2014 refined at R49/R2, on H-L13's ground.** The first draft
of this limb said only *"an item whose outcome is determined by the frozen artifact before the phase
opens is not a gate item"*. Applied literally that deletes the anchor's **substitution detector**
along with the tautology, and the two are not the same object: one cannot fail while the artifact is
correct, the other cannot fail at all. **Deleting a regression guard removes a real detector of a
swapped or corrupted fixture; keeping decoration inflates a row with weight it does not carry.**
Both directions are defects, which is why the limb now names both and disposes of them differently.
This is the same shape as H-L13's refinement: a rule written against one failure mode reached
something it should not have.

''')
print("R2: rationale inserted")

# ---------------------------------------------------------------- R1: the floor limb
s = next(i for i, l in enumerate(L) if l.startswith("> **the declared pre-fix/post-fix separation is stated per horizon"))
assert L[s + 1].rstrip().endswith("horizon's separation may fall below the floor the declaration registers ex ante**;"), L[s + 1]
L[s:s + 2] = ['> **the declared pre-fix/post-fix separation is stated per horizon and side as a PUBLISHED',
              "> CONTEXT FIGURE, carrying no pass/fail consequence** (R49/R1);"]
print("R1: separation limb converted to a published context figure")

# ---------------------------------------------------------------- R1: failure table row 3
hits = [i for i, l in enumerate(L) if l.startswith("| 3 | **A declared horizon's pre/post separation")]
assert len(hits) == 1
L[hits[0]] = ("| 3 | ~~A declared horizon's pre/post separation falls below the registered floor.~~ | "
              "**WITHDRAWN at R49/R1 \u2014 no floor is registered.** Separation is published as a context "
              "figure with no pass/fail consequence. Declared deltas remain **0.034708 / 0.183464 / "
              "0.177131**, published, against the registered pair's implied **0.282**. |")
print("R1: failure-table row 3 withdrawn")

# ---------------------------------------------------------------- R1: s5(a)
start = next(i for i, l in enumerate(L) if l.startswith("**(a) The separation floor's value is not set here, deliberately.**"))
end = next(i for i in range(start, len(L)) if L[i].rstrip().endswith("and not mine."))
NEW_A = '''**(a) The separation floor: RULED at DELTA R49/R1. There is no floor.** Separation is published as
a **context figure per horizon and side, carrying no pass/fail consequence.**

**The reasoning, recorded because the ruling is a reduction and a reader is entitled to it.** The
AUC gap is a property of the **FIXTURE**, not of the tool under test; the amended gate scores a
detector's **findings against the declared map**, so a separation floor imports a v30-era instrument
into a v30a-era gate and measures the wrong object. And the number could not be set honestly: any
value other than **0.282** would be chosen from the distribution this fixture already exhibits,
which \u00a77.0 forbids \u2014 while 0.282, the separation the registered pair implied, **the fixture fails at
all three horizons** (0.034708 / 0.183464 / 0.177131), so registering it would mean the gate cannot
pass. A floor that can only be set by looking at the data is not set.

**DISCLOSED, because this is a reduction and R47/P2's rule cuts both ways.** The registered v30 row
required *both* 0.957 and 0.675 to \u00b10.010, which **entailed** a pre/post gap of 0.282 \u00b1 0.020. That
entailment was the registered row's only separation test, and **this amendment removes it and
replaces it with a published figure that decides nothing.** It is recorded here, in the ledger, and
in the clause \u2014 the same treatment R47/P2 required of the contaminated-side tightening, in the
opposite direction. A reduction whose reason appears nowhere is the failure mode; a reduction the
author rules on the record is a decision.'''
L[start:end + 1] = NEW_A.split("\n")
print("R1: s5(a) rewritten as a ruling with disclosed reduction")

p.write_text("\n".join(L), encoding="utf-8")
print("\nJ3_C1_REDRAFT.md now %d lines" % len(L))
