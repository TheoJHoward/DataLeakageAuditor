#!/usr/bin/env python3
"""DELTA R39 items F4 and F5. Every edit match-count asserted."""

import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")


def sub(path, old, new, expect, label):
    p = D / path
    with open(p, "r", encoding="utf-8", newline="") as f:
        s = f.read()
    c = s.count(old)
    assert c == expect, f"{label}: match count {c}, expected {expect}"
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s.replace(old, new, expect))
    print(f"  [ok x{c}] {label}")


# ------------------------------------------------------------------ F4
STALE = "the §7.7 pointer H1 drafts as hunk **H8** after line 856."
FIXED = ("the §7.7 pointer after line 856 — **redrafted at DELTA R35/B3; H1's H8 draft is "
         "SUPERSEDED** and may not be applied, because it asserts that the entry condition for the "
         "`waived` coverage state is not defined by this registration, which SC-12(w) makes false. "
         "The operative pointer text is Y3 §6.3's.")
for f in ("SCHEMA_SET_FINAL.md", "K1_SCHEMA_CLAUSES.md", "SCHEMA_SET_ADOPTION.md"):
    sub(f, STALE, FIXED, 1, f"F4 stale H8 pointer reference in {f}")

# ------------------------------------------------------------------ F5
sub("SCHEMA_SET_FINAL.md",
    "> **(f) PUBLICATION DISCIPLINE — three constraints, and they are the point of the rule.**",
    "> **(f) PUBLICATION DISCIPLINE — the constraints below, and they are the point of the rule.**",
    1, "F5 SC-4(f) fragile count removed")

sub("SCHEMA_SET_FINAL.md",
    "> **(d) FOUR FORBIDDEN USES OF NON-GATE DATA, REGISTERED BECAUSE EACH IS A ROUTE INTO THE ARITHMETIC.**",
    "> **(d) FORBIDDEN USES OF NON-GATE DATA, REGISTERED BECAUSE EACH IS A ROUTE INTO THE ARITHMETIC.**",
    1, "F5 SC-10(d) fragile count removed")

OLD_CLAIM = """**What was deliberately NOT changed, and why the distinction matters.** A scan of every clause found
three further in-clause numerals: SC-4(b)'s "EXACTLY THREE CLASSES, MUTUALLY EXCLUSIVE AND
EXHAUSTIVE" (with "There is no fourth class and no residue class"), SC-4(e)'s "Two grounds are
registered here", and SC-13c(c2)'s "rests on two grounds and on no other". **These stay.** They are
not references to an enumeration that might grow — they are **closure statements**, where the number
IS the rule: dropping the numeral would delete the constraint that the set is closed, which is a
weakening, not a de-fragilisation. H-L13's fragility is a count that must be re-bumped when its
target grows; a count that forbids the target from growing is the opposite object."""

NEW_CLAIM = """**The scan, corrected at DELTA R39/F5 — and the earlier version of this paragraph was wrong.** It
claimed a scan of every clause had found "three further in-clause numerals" and defended all three.
The scan was incomplete: it missed at least five, and **two of the five were not closure statements
at all**. A false statement about a scan is worse than the defects the scan missed, because it tells
a later reader the ground has been covered.

**Fixed as fragile counts** — each enumerates without forbidding growth, so adding an item silently
falsifies the numeral, which is exactly H-L13's shape:

- SC-4(f), was "PUBLICATION DISCIPLINE — **three constraints**"; now "the constraints below". Its
  items 1–3 carry no "and no fourth".
- SC-10(d), was "**FOUR** FORBIDDEN USES OF NON-GATE DATA"; now "FORBIDDEN USES". Its items (1)–(4)
  carry no closure sentence either.

**Kept, because in these the number IS the rule** — it is what closes the set, and striking it would
delete a constraint rather than de-fragilise a reference:

- SC-4(b) "EXACTLY THREE CLASSES, MUTUALLY EXCLUSIVE AND EXHAUSTIVE", which continues "**There is no
  fourth class and no residue class.**"
- SC-3(b) "THREE DISPOSITIONS, MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE MAP" — exhaustiveness is
  asserted in the heading itself.
- SC-6(c) "TWO LEVELS, AND THEY DO NOT COLLAPSE" — the count is the non-collapse rule.
- SC-7(a) "A DETECTOR RECEIVES EXACTLY TWO THINGS" — "exactly" is the input-surface restriction.
- SC-4(e) "Two grounds are registered here" and SC-13c(c2) "rests on two grounds **and on no other**".

**The test, stated so the next scan does not have to re-derive it:** if growth silently falsifies the
numeral, it is a stale reference and H-L13 applies. If growth is what the numeral forbids, it is a
closure constraint and removing it is a weakening §0.2.1 line 97 does not permit."""

sub("SCHEMA_SET_FINAL.md", OLD_CLAIM, NEW_CLAIM, 1, "F5 false scan claim corrected")
print("\nF4 + F5 applied.")
