# A22 — THE APPLIED-DEFECT SET, PRESENTED AS ONE SET

**⛔ HALTS by construction.** R137 §1.3: the author rules **correct-by-diff or
disclose-as-deviation for the whole set** — *"Not one at a time — that pattern produced five
reopenings."*

**Every defect below was APPROVED that way.** A20 established that `PREREG.md` is byte-identical to
`prereg-v30:PREREG.md` with `PREREG_v30a_APPROVAL.diff` applied. **Nothing here is an application
failure.** Each is text the approval record contains, describing neighbours the approval record
does not contain — because the approval was a subset of a larger plan.

**The set is derived, not transcribed.** R137 §1.3 enumerates six items; the derivation finds
**sixteen**, and §36.2 says report the set before fixing any of it. R137's list also counts
`l.1544` twice — once by line and once as *"the one uncleared deictic"* — and omits the four
amendments-block citations and the three `SC-12(w)` citations. **This is the whole set.**

---

## The two absences that cause class A

| # | what | state |
|---|---|---|
| **0a** | a `## v30a amendments` block | **does not exist anywhere in `PREREG.md`** |
| **0b** | an `**Amendment status:**` line | **does not exist**; l.6 still reads `**Status:** v30 —` |

l.6 reading `v30` is **not** a defect — `check_registration.py:75-77` parses that exact substring
into `_is_historical_note()`, determination recorded at A18/F1. What is absent is the *additional*
status line the amendment drafted, not a correction to l.6.

---

## Class A — four citations of the absent amendments block

| # | line | what it says |
|---|---|---|
| 1 | **1849** | *"…states and the amendments block **records**."* |
| 2 | **1853** | *"…recorded in the **v30a amendments block** (SC-13c(c2))."* |
| 3 | **1915** | *"…**amendments block in terms**, and it reaches nothing else…"* |
| 4 | **1917** | *"…**resolved by this clause** — it is recorded in the **amendments block** as a duplicated-authority…"* |

**l.1338 is NOT in this set.** It cites `§10.2 (v30a) [SC-13c(c2)]`, which **resolves** — SC-13c is
applied. Earlier rounds listed *"the five citations at ll. 1338, 1849, 1853, 1915, 1917"*; the
derivation clears l.1338 and the class is **four**, not five.

---

## Class B — clauses that describe neighbours which do not exist

| # | line | what it says | what is there |
|---|---|---|---|
| 5 | **1415** | SC-6b: *"§8.2, after `PREREG.md` line 915 **(after marker M2 where placed)**"* | **M2 is not placed.** The clause hedges its own anchor rather than failing on it |
| 6 | **2013** | SC-8b: *"the **item-3 marker** … follow the list"* | absent |
| 7 | **2013** | SC-8b: *"the **line-97 marker** is placed after line 97 in §0.2.1"* | absent; l.97 still reads *"both file hashes"*, unmarked |
| 8 | **2013** | SC-8b: *"**SC-8's revised M2**"* | absent |

**Mitigation for 6 and 7, recorded so the ruling is not made on a worse picture than the truth:**
item 8's own body registers the substance — *"where an earlier clause names the hashed files or
their number — item 3's three names, §0.2.1 line 97's 'both' — it … is superseded as the set by
this item."* **The rule is registered; the markers at the sites are not, and a framing note asserts
they are.**

---

## Class C — a citation of a DELETED registered row

| # | line | what it says |
|---|---|---|
| 9 | **1544** | *"…every detector-case coverage state **that row** carries other than `passed` and `failed`."* |

**`Detector-case coverage` occurs zero times in `PREREG.md`.** v30 l.855's row was removed by an
approved removal and never re-registered — A20b: not retained, no marker, longest surviving run
37/119 characters of shared vocabulary. §8.2's own row for this surface says it *"is re-registered
with `unscored`"*. **It is not.**

This is also the **only** deictic in the file whose referent is gone. The other two were read and
cleared: l.895's *"that row"* names a detector row in its own sentence; l.1163's names *"each §0.1
lock-table row"*, likewise.

---

## Class D — three citations of `SC-12(w)`, whose limb text is absent

| # | line | what it says |
|---|---|---|
| 10 | **1425** | *"Same correction DELTA R37/D1 made for **SC-12(w)'s own limb text**."* |
| 11 | **1427** | §7.7 pointer: *"**SC-12(w) registers the condition** under which a detector-case may…"* |
| 12 | **1565** | §8.3 assertion: *"carried with SC-12(w), **whose (w1) prohibits the state outright**"* — citing a sub-limb by number |

`SC-12(w)`'s limb — *"a prohibition, and a closed list of licensed grounds with no members"* — is
**not in `PREREG.md`**: `ENTRY CONDITION FOR` and `closed list of licensed grounds` occur **0**
times in the file and **2** and **1** times in `SCHEMA_SET_FINAL.md`. The `SC-12` record's clause
span is SSF ll.1081–1126; the limb sits at ~ll.1141–1173, **outside the span**.
`verify_schema_records.py` digests the declared span and cannot see that the span stops short of the
block it names.

---

## Class E — structural damage the amendment introduced

Attributed by a **differential** markdown scan against v30, so nothing pre-existing is charged to
the amendment.

| # | line | what | v30 → applied |
|---|---|---|---|
| 13 | **1380** | `\| Level \| States \|` — a table header and separator with **zero body rows** | 0 → 1 |
| 14 | **1417** | `\| **Strategy diagnostic** \| …` — orphaned **35 lines** below its header behind two blank lines, so markdown renders it as a **paragraph**, not a table row | 17 → 18 |

Verified again for this document: ll.1379–1380 are the header and separator, l.1381 is blank, and
the next non-blank line is the `SC-6a` comment. §7.7's *"two levels"* table now carries **no
coverage states at all**, while SC-6, §8.2's pointer and §10.2's `waived` all cite *"§7.7's row"*.

**The setext hazard did not recur:** `---` flush against a paragraph, 0 in v30 and 0 in the applied
file. Reported because a rule proven clean is worth as much as one proven violated.

---

## Summary — sixteen items, one ruling

| class | items | what they have in common |
|---|---|---|
| 0 | 2 | the block and status line the rest of the set refers to |
| A | 4 | citations of the absent amendments block |
| B | 4 | clauses describing markers that were never placed |
| C | 1 | a citation of a deleted registered row |
| D | 3 | citations of `SC-12(w)`'s absent limb |
| E | 2 | markdown structure the amendment broke |

**Every one was approved.** The two dispositions R137 §1.3 offers are **correct-by-diff** — which
means a new `PREREG.md` diff the author approves, and which for classes A and 0 means applying the
amendments block itself — or **disclose-as-deviation**, which leaves the registered file citing
things that are not in it and records that fact where a reader will find it.

**A22 halts here. `PREREG.md` is unchanged at `0c8da19f237cd243…` and nothing is staged.**
