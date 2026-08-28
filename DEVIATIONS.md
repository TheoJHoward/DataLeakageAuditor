# DEVIATIONS

Append-only. Each entry records **what is true**, **what was expected**, and **why it stands**.

Nothing here creates, amends, or narrows a rule. §0.2.1 places class A branches and class B
parameters in this file and keeps class C changes out of it, because a class C change needs an
amended registration first. **These entries are disclosures of fact about the tagged state, not
instructions to anyone.**

**Opened 28 August 2026, immediately after `prereg-v30a` was signed, pushed and stamped.** The tag
attests this file as empty; everything below was written after that attestation, which is what an
append-only deviations record is for. Verify the registered files against the tag, not against
`HEAD`.

---

## D-V30A-01 — SC-6b's reference resolves to an empty range

**True:** §7.7's table carries a header and a separator and no body rows. SC-6b's clause extends
§8.2's closing sentence by reference to that row, so the extension reaches nothing.

**Expected:** the v30 row that carried the detector-case coverage states was to be present, giving
the reference something to range over.

**Why it stands:** the row was superseded without retention when v30 line 855 was replaced. Nothing
downstream requires the range to be non-empty — no published preserving or promoted metric reads a
§7.7 detector-case state, `assert_audit_complete()` names its three states directly, `unscored` is
named expressly in SC-6b's own clause, and §8.2 carries its own enumeration. Re-registering the row
was considered and refused, because no consumer was waiting on it and doing so would have been a
change to registered text made to satisfy a reference rather than a reader.

**Carried consequence:** `waived` sits outside §8.2's display sentence. SC-12(w)'s limb prohibits
the state outright, so no entry in it can exist to be displayed. The protection is at entry, not at
display, and that is disclosed rather than repaired.

## D-V30A-02 — `SCHEMA_SET_FINAL.md` still annotates §AB as not applied

**True:** the adoption file's heading for §AB reads that it is drafted and not applied. §AB is
applied, at `PREREG.md` lines 1348–1395.

**Expected:** an annotation consistent with the applied state.

**Why it stands:** `SCHEMA_SET_FINAL.md` is frozen at the hash the author approved. Editing it would
break byte-identity with the approved artifact, which is worth more than an accurate annotation
inside it. Disclosable, not fixable.

## D-V30A-03 — SC-12(w)'s limb states a premise this file does not bear out

**True:** the limb opens by saying §7.7's table carries `waived` as a detector-case coverage state
and that it is the only state in that table lacking an entry condition. §7.7's table carries no body
rows, so the first clause does not hold of the applied file and the second is vacuous over an empty
set.

**Expected:** the premise to be true, as it was of v30 before line 855 was superseded without
retention.

**Why it stands:** the limb is approved content, extracted verbatim from the approved adoption file
and applied as written. Editing it would depart from what was approved. The premise is recorded here
so a reader who checks it is not left to guess which of the two is wrong.

## D-V30A-04 — §7.7's table has no body rows

**True:** the `Level` / `States` header and its separator are followed by a blank line. The table
renders empty.

**Expected:** the table to carry the coverage states that SC-6, §8.2's pointer and §10.2's `waived`
all refer to.

**Why it stands:** attributed to the amendment by a differential scan against v30, so nothing
pre-existing is charged to it. Repair would mean re-registering a row — see D-V30A-01.

## D-V30A-05 — an orphaned table row renders as a paragraph

**True:** the `Strategy diagnostic` row sits well below the header it belongs to, separated by
intervening content, so markdown renders it as a paragraph rather than a row.

**Expected:** the row adjacent to its header.

**Why it stands:** moving it would repair the structure and nobody asked for that change; it was
named rather than made, and it is named here.

## D-V30A-06 — two drafted objects never reached the file

**True:** `PREREG.md` contains no `## v30a amendments` block and no `**Amendment status:**` line.

**Expected:** both were drafted for the amendment.

**Why it stands:** the block was not approved content — it was not among the artifacts the author
approved — and one of its own assertions was false of the file it would have described. It was
refused rather than landed. The status line is a separate insertion that was not reached. Line 6's
existing status text is not a defect; the checker parses that exact substring as a historical note.

## D-V30A-07 — §AB asserts a pointer that was not inserted

**True:** §AB states that a pointer to the exception is inserted at line 816's own site. It is not.
Of the v30a insertion markers, exactly one still carries unapplied drafting apparatus, and the
pointer paragraph exists only as a fenced specimen.

**Expected:** the pointer applied at that site.

**Why it stands:** the pointer's own text cites the amendments block, which does not exist and never
will — see D-V30A-06. Applying it verbatim would have put that citation into registered prose one
commit after it was removed from four other sites; applying it corrected would no longer have been
the approved text. It was refused, knowingly, and the sentence it falsifies is disclosed here. This
is navigational prose; nothing ranges over it.

## D-V30A-08 — sixteen `BLOCK_MANIFEST.md` ranges are unresolved

**True:** the §A table's line ranges were re-derived from each structure's own delimiters. Eight were
corrected, all by exactly eight lines. Sixteen have no length-preserving candidate and were left
untouched and named; several of those are stale.

**Expected:** every declared range to bound its block.

**Why it stands:** the instrument cannot resolve a sub-range inside a longer structure, and a number
it cannot derive is one it must not write. Guessing would have replaced a known-stale value with an
invented one that looks derived. The file now carries a note that its ranges are derived and must be
re-derived before use.

## D-V30A-09 — the declaration's artifact allocation is inverted, and a term it relies on is undefined

**True:** the availability declaration's §0.1 and §0.2 each state which artifact §6.2's criteria are
evaluated on, and both statements are the reverse of what the criteria require. Separately, the term
`feature pipeline` appears once in the declaration and nowhere in `PREREG.md`.

**Expected:** allocation statements consistent with the criteria as amended, and a registered
definition for a term the criteria rely on.

**Why it stands:** the cause is on the record — both sentences were written when criterion 3 was a
silence test, and the change that made it a map-scoring test was never carried back into the
allocation. v30a amended that criterion but did not re-derive the allocation. The declaration is one
of the attested files and `PREREG.md` is closed, so neither can be corrected under this
registration; supplying the missing definition would require a further amendment. Disclosed here and
queued, not acted on.

## D-V30A-10 — the OpenTimestamps attestation was pending when it was committed

**True:** the receipt committed alongside the amendment commit hash carried calendar commitments
only, with no Bitcoin attestation, at the time of writing.

**Expected:** a Bitcoin attestation, which arrives after the calendars aggregate.

**Why it stands:** this is the ordinary sequence, and v30's receipt followed it. Recorded so the
committed receipt is not read as more than it was when written; the upgraded receipt is queued.
