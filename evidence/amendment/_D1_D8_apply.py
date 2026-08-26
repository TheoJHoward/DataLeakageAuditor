#!/usr/bin/env python3
"""DELTA R37 items D1 and D8, applied with a match-count assert on every edit."""

import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")


def read(p):
    with open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def sub(path, old, new, expect, label):
    p = D / path
    s = read(p)
    c = s.count(old)
    assert c == expect, f"{label}: match count {c}, expected {expect}"
    write(p, s.replace(old, new, expect))
    print(f"  [ok x{c}] {label}")


# --------------------------------------------------------------- D1.1
W7 = ("> **(w7) REPORTING OBLIGATION.** The gate report publishes the count of `waived` "
      "detector-case entries, **per detector and per combination**, as a count. **That count is "
      "zero.** A report that does not publish it has not discharged this limb: a prohibition "
      "whose observance is never published is not checkable.")

BOUNDS = W7 + """
>
> **What this limb does NOT permit.**
>
> **(1) It licenses the state in no case, and silence is not licence.** The empty enumeration is the whole of the permission. In particular, **a criterion's failure to name a detector licenses nothing**: a criterion that enumerates its detectors and omits this one, a criterion written before this detector existed, and a criterion that says nothing about detectors at all are **all silence for this purpose**. The omitted detector **bears on that criterion**, and its cases are executed to terminal results. Reading silence as licence would be waiving by omission \u2014 limbs **(i)** and **(iii)** above \u2014 and would move the licence from registered text to whoever last failed to update an enumeration.
>
> **(2) A ground may be added only by a further class C amendment to this limb** (\u00a70.2.1 line 93), committed and externally timestamped **before the affected detector is implemented or evaluated** (line 95), never after a fixture result is observed (\u00a76.2 line 480; SC-8). Any such ground must be **declaratory** under (w3). **And no such amendment may license the state for a detector the floor governs at a \u00a710.2 replacement criterion**: the floor forbids that above, there is no procedure by which it may be done, and this limb supplies none and may not be cited as one.
>
> **(3) "No data" is still not "waived"** (item (4) above), and this limb creates no route by which it becomes so. A cell with no data is `unscored` where SC-6(b)'s declared-ledger condition is met; absence of data at run time is otherwise the not-run state its cause selects (\u00a78.2). A run that produced nothing, a missing or impossible input, a crashed or failed strategy, and a surprising result are each disposed of there and by none of them does a case enter this state.
>
> **(4) "Experimental" is still not "waived"** (item (3) above). A detector or mode shipped experimental under \u00a710.2 criterion 3 executes its cases and reports their terminal results; the marking changes how findings are **labelled and asserted on**, never which coverage state a case takes.
>
> **(5) Jurisdiction is not waiver.** What a jurisdictional routing statement reaches is settled at SC-13c(c6), cited and not restated. A boundary on **where a finding is charged** is never a licence to leave a case **unexecuted**.
>
> **(6) It amends no other coverage state's entry condition and moves no boundary in \u00a78.2.** It reaches \u00a78.3 in exactly one way, deliberately: `waived` joins `assert_audit_complete()`'s failure set at line 929, so that emitting the prohibited state **fails an assertion instead of passing silently**. That is the whole of its reach into \u00a78.3 \u2014 no other assertion changes, and no other coverage state's treatment changes. **`unscored` is not added to that failure set, and must not be**: `unscored` is a *permitted* state that honest coverage accounting produces, whereas `waived` is *prohibited* by (w1), so a report emitting it is non-conforming on its face. A prohibition no assertion tests is not enforced; a permitted state that failed an assertion would punish correct reporting.
>
> **(7) It authorises no retro-fitting.** Text adopted or amended after a run does not reach a case already run, and a licence claimed after a case was reported is not a licence.
>
> **(8) It licenses nothing after tuning** (item (7) above)."""

sub("SCHEMA_SET_FINAL.md", W7, BOUNDS, 1,
    "D1.1 bounds block restored into applied text; bound (6) rewritten; D6 ground stated in-clause")

# --------------------------------------------------------------- D8.1 / D8.2
OLD_PTR = ("**`waived` is defined in \u00a710.2 (v30a).** That definition governs the word wherever it "
           "appears, including this table. **The conditions under which a detector-case may be "
           "reported in this state are not defined by this registration**; defining them is a class "
           "C change, and until it is made no case may be reported as `waived` on the strength of "
           "the state merely existing in this table.")
NEW_PTR = ("**`waived` is defined in \u00a710.2 (v30a).** That definition governs the word wherever it "
           "appears, including this table, and **SC-12(w) registers the condition under which a "
           "detector-case may be reported in this state.** Neither is restated here.")
sub("PREREG_v30a_DIFF.md", OLD_PTR, NEW_PTR, 1,
    "D8.1 APPLIED \u00a77.7 pointer redrafted (the H8 text is superseded)")

OLD_WHY = ("**Why the second sentence is drafted the way it is.** \u00a7A.12 defines what *being waived* "
           "means; it does **not** supply an entry condition for \u00a77.7's coverage state, and inventing "
           "one here would exceed the walk. The draft therefore says so explicitly and closes the "
           "permissive reading without creating a rule the walk does not support. **This is a "
           "residual gap, reported in \u00a7(iii) item 12.**")
NEW_WHY = ("**Why the second sentence is drafted the way it is \u2014 REVISED, DELTA R35/B3 and R37/D8.** "
           "The earlier draft recorded a residual gap: \u00a7A.12 defines what *being waived* means and "
           "supplied no entry condition for \u00a77.7's coverage state, and inventing one would have "
           "exceeded the walk. **That gap is closed by this amendment.** SC-12(w) registers the entry "
           "condition \u2014 a prohibition with a closed and empty list of licensed grounds \u2014 so the "
           "pointer now names it instead of reporting its absence. The superseded sentence asserted "
           "the condition did not exist; leaving it standing would have shipped two registered texts "
           "disagreeing at the exact site of the defect being fixed.")
sub("PREREG_v30a_DIFF.md", OLD_WHY, NEW_WHY, 1, "D8.2 pointer rationale revised")

# --------------------------------------------------------------- D8.3 / D8.5
OLD_A = ("*(K1's finding F-6 \u2014 that `unscored` would otherwise have repeated `waived`'s "
         "missing-entry-condition\ndefect, and that \u00a77.7's `waived` still has none after this "
         "amendment \u2014 stands as the drafting record\nfor limb (b); the reference to it is kept "
         "here, in apparatus, and removed from the applied clause\ntext.)*")
NEW_A = ("*(K1's finding F-6 \u2014 that `unscored` would otherwise have repeated `waived`'s "
         "missing-entry-condition\ndefect \u2014 stands as the drafting record for limb (b); the "
         "reference to it is kept here, in\napparatus, and removed from the applied clause text. "
         "**F-6's second half is now spent:** it recorded\nthat \u00a77.7's `waived` would still have no "
         "entry condition after this amendment. **SC-12(w)\nsupplies one**, so that consequence no "
         "longer holds, and the sentence asserting it is struck rather\nthan softened.)*")
sub("SCHEMA_SET_FINAL.md", OLD_A, NEW_A, 1, "D8.3 SC-6 apparatus note corrected (was line 583)")
sub("SCHEMA_SET_ADOPTION.md", OLD_A, NEW_A, 1,
    "D8.5 superseded predecessor's apparatus note corrected")

# --------------------------------------------------------------- D8.4
OLD_K1 = ("**Consequence the author should note:** \u00a77.7's `waived` still has no entry condition "
          "after this\namendment, and now stands out as the only state in the table without one.")
NEW_K1 = ("**Consequence the author should note \u2014 SUPERSEDED, DELTA R35/B3.** As drafted this read: "
          "\"\u00a77.7's\n`waived` still has no entry condition after this amendment, and now stands out as "
          "the only state in\nthe table without one.\" That was true of the set as K1 left it. "
          "**SC-12(w) closes it**: `waived` now\ncarries an entry condition, and no state in \u00a77.7's "
          "table is left without one.")
sub("K1_SCHEMA_CLAUSES.md", OLD_K1, NEW_K1, 1, "D8.4 K1 F-6 consequence marked superseded")

# --------------------------------------------------------------- D8.6
OLD_R25 = ('POINTER \u2014 "`waived` is defined in \u00a710.2 (v30a)", with the residual-gap statement '
           '(no entry condition for the coverage state is defined by this registration)')
NEW_R25 = ('POINTER \u2014 "`waived` is defined in \u00a710.2 (v30a)", naming **SC-12(w)** as its entry '
           'condition (the residual-gap statement is superseded; DELTA R35/B3)')
sub("K2_AMENDMENT_LEDGER.md", OLD_R25, NEW_R25, 1, "D8.6 K2 working row R25 descriptor corrected")

print("\nD1 + D8 applied.")
