# A35 — §7.7's DELETED ROW: THE DEPENDENCY CHECK, AND THE DISCLOSURE IT LICENSES

**DRAFT. HELD, NOT APPLIED.** `DEVIATIONS.md` is one of the twenty hashed paths and is edited only
by applying a diff the author has explicitly approved. This file is the proposed text and the
derivation behind it; nothing here has been written into a registered object.

**Determined against `PREREG.md` at `e7b0e5ae…`, 2228 lines, `main` at `2ca816c`** — i.e. after A33
landed hunks 1–3, because SC-12(w)'s limb is one of the things the answer turns on.

---

## THE QUESTION R142 §1.2 PUTS

SC-6b's clause ranges, by reference to §7.7's row, over *"every detector-case coverage state that row
carries other than `passed` and `failed`."* **The row is gone**, so the range is empty. R142 §1.2
makes the test a dependency question and fixes both outcomes in advance:

- nothing downstream requires SC-6b's range to be non-empty → **do not land hunk 4; disclose**
- a metric, gate or reducer **does** require it → **HALT and report what breaks**

**The answer is the first**, and the reason is one registered sentence rather than an argument.

## THE DECIDING FACT — line 1080

> **Every published preserving or promoted metric reads this state**, never the detector-case state
> of §7.7, which remains the unit `assert_audit_complete()` operates on. Both are stored.

**No published metric reads §7.7's detector-case state at all.** The dependency question is therefore
not *which* metric breaks but whether the single reader breaks — and SC-12(w)'s limb, landed at A33,
says the same thing from the other side: *"no runtime metric reads a detector-case state (§7.2.1),
and `assert_audit_complete()` reads it alone."*

## THE FOUR CONSUMERS, EACH TESTED SEPARATELY

| consumer | reaches its states how | needs the row? |
|---|---|---|
| **`assert_audit_complete()`** (l.1676) | names `unsupported`, `could_not_run`, `waived` **by name** | **no** |
| **`unscored`** under §8.2's closing sentence | SC-6b names it **explicitly in its own clause** (l.1649), not through the row | **no** |
| **§8.2's closing sentence** (l.1644) | §8.2 carries its **own** enumeration — `not_applicable`, `unsupported`, `could_not_run(reason)` | **no** |
| **every published runtime metric** | reads `schedule_state`/`evidence_outcome` (§6.6), never §7.7 (l.1080) | **no** |

**Not one of the four requires the range to be non-empty.** SC-6b's extension is a **no-op**, not a
break: with the row gone, §8.2's closing sentence falls back to the enumeration in §8.2 alone — which
is precisely the fallback SC-6b was written to prevent being the *sole* source, and which is
non-empty regardless.

**Hunk 4 does not land.** Landing it would re-register a row to make a clause's reference resolve,
and no consumer is waiting on it.

---

## WHAT THE EMPTY RANGE DOES COST — stated, because a no-op is not the same as no effect

**One state fell out of §8.2's display rule when the row was deleted: `waived`.** §8.2's own
enumeration does not name it, and the row that would have carried it is gone, so §8.2's *"None may be
displayed in a way mistakable for a pass"* **does not reach `waived`**.

**That gap is closed, but not by §8.2.** SC-12(w)(w1), landed at A33, reads: *"NO DETECTOR-CASE MAY
BE REPORTED `waived`. LICENSED GROUNDS: NONE."* **No entry in the state can exist to be displayed**,
and `assert_audit_complete()` fails on any that does. The protection is a prohibition at entry rather
than a rule at display — which is the direction SC-12(w) itself says the bound is forced in.

**This is disclosed rather than repaired** because repairing it means either re-registering the row
(hunk 4, ruled out) or extending §8.2's enumeration (a substantive change to operative text nobody
has approved).

---

## TWO DEFECTS FOUND WHILE DERIVING THIS, NEITHER REPAIRED HERE

### 1. SC-12(w)'s limb states a premise the file falsifies

The limb A33 landed opens (l.1923):

> §7.7's table carries `waived` as a detector-case coverage state and registers no condition under
> which a report may assign it. **It is the only state in that table without one.**

**§7.7's table carries nothing.** It is a header and a separator with **zero data rows** (ll.1486–1487).
The sentence was true of v30, whose l.855 carried the row; it is false of v30a, where l.855 was
superseded **without retention**. The second sentence is worse than false — it is **vacuous**: a
uniqueness claim over an empty set.

**This is not A33's error.** The limb is approved content, extracted verbatim from `SCHEMA_SET_FINAL.md`
at the approved hash, and applying it as written was the instruction. **It is disclosed because a
registered clause now rests on a stated premise its own file contradicts**, and a reader checking the
premise will find an empty table and be unable to tell whether the clause or the table is wrong.

### 2. §7.7's table is structurally broken independently of the deletion

- **ll.1486–1487** — `| Level | States |` and `|---|---|`, then a blank line. **A table with no rows.**
- **l.1524** — `| **Strategy diagnostic** | ... |`, **36 lines below the separator**, outside the
  table, rendering as a paragraph rather than a row.

The orphaned row is not the deleted one and landing hunk 4 would not fix it; it is named here so the
two are not confused. Moving it back would repair the structure — **a change nobody has asked for, so
it is named and not written.**

---

## PROPOSED `DEVIATIONS.md` ENTRY — the held text

> **§7.7's detector-case coverage-state row is not carried into v30a, and SC-6b's reference to it
> resolves to an empty range.** v30 line 855 was superseded without retention. SC-6b's clause extends
> §8.2's closing sentence *"by reference to §7.7's row and not to the enumeration in this section
> alone"*; with the row absent, that extension adds nothing and §8.2's own enumeration —
> `not_applicable`, `unsupported`, `could_not_run(reason)` — is the operative domain.
>
> **No metric, gate or reducer depends on the range being non-empty.** Line 1080 registers that no
> published preserving or promoted metric reads a §7.7 detector-case state; `assert_audit_complete()`
> is the sole reader and names its three states directly. `unscored` is reached because SC-6b names it
> expressly, not through the row. **The row was therefore not re-registered.**
>
> **One consequence is carried rather than closed:** `waived` is outside §8.2's display prohibition.
> SC-12(w)(w1) prohibits the state outright and `assert_audit_complete()` fails on any entry in it, so
> no entry can exist to be displayed; the protection is at entry, not at display.
>
> **SC-12(w)'s limb states that §7.7's table carries `waived` and that it is the only state in that
> table without an entry condition. §7.7's table carries no rows.** The premise was true of v30 and is
> false of v30a. The limb is approved registered text and is not edited here; the discrepancy is
> recorded so that a reader who checks the premise is not left to guess which of the two is wrong.
