#!/usr/bin/env python3
"""DELTA R47 / P7 - limb (i) HARD-FAILS.

"A limb that only records a deviation is not a gate limb, by J3's own rule."
That rule is SC-8(g), drafted at J3 s2: a gate item states the condition under
which it FAILS. Recording a deviation states no such condition.

Line-anchored, and every anchor is asserted against its expected content before
anything is written.
"""
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
p = D / "J3_C1_REDRAFT.md"
L = p.read_text(encoding="utf-8").split("\n")

# ---- anchor 1: the operative limb, lines 88-90 (1-indexed) ------------------
assert L[87].startswith("> that figure within"), L[87][:50]
assert "recorded as a DEVIATION" in L[88], L[88][:50]
assert L[89].endswith("*(ii)* **INTEGRITY** \u2014 each entry is"), L[89][-40:]
NEW_LIMB = [
    "> that figure within \u00b10.010 absolute **fails this gate row**. An entry whose",
    "> originating figure is unavailable, or was produced under a different model family,",
    "> **also fails this gate row, unless the declaration registered that entry ex ante as",
    "> having no originating counterpart and stated why** \u2014 a ground declared before any",
    "> Phase 1 measurement, never after one; *(ii)* **INTEGRITY** \u2014 each entry is",
]
L[87:90] = NEW_LIMB
print("limb (i) rewritten: 3 lines -> %d" % len(NEW_LIMB))

# ---- anchor 2: failure-table row 1 ------------------------------------------
OLD_CELL = ("Under limb (i) this is a recorded DEVIATION with its cause, not a silent pass. "
            "The registered pair's provenance and the family change are both surfaced at the gate.")
NEW_CELL = ("Under limb (i) as settled at R47/P7 this **fails the gate row** \u2014 so **the row fails "
            "on today's artifact**, and Phase 1 does not pass until either the anchor reproduces or "
            "the declaration registers ex ante that the entry has no originating counterpart, and why.")
hits = [i for i, ln in enumerate(L) if OLD_CELL in ln]
assert len(hits) == 1, "table cell match count %d" % len(hits)
L[hits[0]] = L[hits[0]].replace(OLD_CELL, NEW_CELL, 1)
print("failure-table row 1 updated at line %d" % (hits[0] + 1))

# ---- anchor 3: s5(b) becomes a decision TAKEN -------------------------------
start = next(i for i, ln in enumerate(L) if ln.startswith("**(b) Limb (i) records a deviation"))
end = next(i for i in range(start, len(L)) if L[i].rstrip().endswith('substitute *"fails this gate row"*.'))
assert end - start == 6, "s5(b) spans %d lines, expected 7" % (end - start + 1)
NEW_B = """**(b) Limb (i) hard-fails. SETTLED by the author at DELTA R47/P7; no longer an open decision.**
The draft above recorded a deviation instead of failing. That was the one place this redraft was
deliberately weaker than a maximal reading, and it does not survive its own rule: **SC-8(g)
requires a gate item to state the condition under which it FAILS, and an item that only records a
deviation states no such condition.** A limb that cannot fail is not a limb.

**The consequence, stated plainly because the author is entitled to it before signing.** Failure
mode 1 is live on today's artifact \u2014 \u00a7A.1: *"There is no horizon at which the registered pair is
reproduced."* Under the hard fail **the Phase 1 gate row fails as things stand.** That is P7's
intended effect and not a side effect: the registered anchor is an externally-originating target
the fixture demonstrably misses, and a gate that passed anyway would be the withdrawn C1 by
another route. The row is cleared by reproducing the anchor, or by the declaration registering
**ex ante** that the entry has no originating counterpart and why \u2014 **never** by choosing a
tolerance after seeing the miss (\u00a77.0).

**Interaction with P8, which is not yet settled.** If P8 finds the originating record is not keyed
per horizon and side, then the *unavailable* branch \u2014 not the comparison \u2014 governs every entry,
and under the hard fail the row fails for a record-keeping reason rather than anything about the
tool. **A limb whose exception branch governs every case is mis-drafted**, and limb (i) would need
re-scoping before adoption. Flagged because P7 and P8 interact: adopting P7 before P8 answers is
adopting a limb whose behaviour is unknown.""".split("\n")
L[start:end + 1] = NEW_B
print("s5(b) replaced: 7 lines -> %d" % len(NEW_B))

# ---- status line -------------------------------------------------------------
S = "**DRAFTED, UNAPPLIED, UNVERIFIED BY ANY PARTY THAT DID NOT DRAFT IT.**"
hits = [i for i, ln in enumerate(L) if S in ln]
assert len(hits) == 1
L[hits[0]] = L[hits[0]].replace(
    S, S + " *(R47/P7 applied:\nlimb (i) hard-fails. R47/P8 pending: whether every declared entry has an originating\ncounterpart \u2014 see \u00a75(b).)*", 1)

p.write_text("\n".join(L), encoding="utf-8")
print("\nP7 APPLIED. J3_C1_REDRAFT.md now %d lines." % len(L))
