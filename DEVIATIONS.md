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

**Why it stands:** the instrument cannot resolve a sub-range inside a longer structure, and it did
not write a number it could not derive. Guessing would have replaced a known-stale value with an
invented one that looks derived. The file now carries a note recording that its ranges are derived,
and that extracting inside a stale one is what truncated two blocks.

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

## D-V30A-11 — the hash-set enumeration check reports a false positive, and the gate closes red

**True:** `hash_set_single_source` fires on line 236 of `HISTORY.md`, the last entry of the review
register. The flagged line is a sentence recording which registered files diverged from the tagged
set after the tag. It names three of the twenty paths and carries no digest of any kind — scanned
for hexadecimal runs of sixteen characters or more, the count is zero. The detector's own comment
states its subject: path enumerations purporting to be the set. The sentence does not purport to be
the set.

**Expected:** the check to fire on a second copy of the hashed-path set, not on prose naming three
registered files inside a paragraph about drift.

**Why it stands:** three repairs were measured and none of them holds.

A digest requirement was measured against the whole corpus. Every line in the detector's domain
carrying three or more registered basenames was enumerated, with a check for any digest in its
window:

| candidate | basenames | digest in window |
|---|---|---|
| `PREREG.md` l.2152 | 8 | no |
| `PREREG.md` l.2154 | 3 | no |
| `HISTORY.md` l.236 | 3 | no |
| `AVAILABILITY_DECLARATION.md` l.3752 | 8 | no |
| `AVAILABILITY_DECLARATION.md` l.3855 | 3 | no |
| `COMMIT_PLAN.md` l.243 | 4 | no |
| `COMMIT_PLAN.md` l.357 | 3 | no |
| `CEREMONY_COMMANDS.md` l.277 | 20 | no |

Eight candidates, zero digests. A digest requirement silences the entire population, the set's own
authoritative declaration included. That declaration is a shell assignment listing twenty paths and
no hashes: **the authoritative set is a path list, and the digests live in the tag message.** Three
planning-layer expectations rested on the opposite premise and were withdrawn on this measurement.

A path-form test was measured next, on the premise that a construct purporting to be the set uses
the set's own registered path forms while prose uses bare basenames. The bare column is zero across
all eight candidates. The flagged sentence names a path in the set's own form, and so do four of the
other seven.

An enumeration-shape test was measured third, and it inverts. The flagged line is a list item, as
are two legitimate candidates. The longest gap between consecutive paths on it is seven characters,
a comma-and list, against eighty-two characters of sentence material between paths on `PREREG.md`
l.2152. Under a delimited-sequence test the false positive resembles an enumeration more closely
than a legitimate candidate does.

Two measures did separate it — the share of the line occupied by paths, 4.2 per cent against a
next-lowest 11.7, and the characters following the last path, 829 against 686. Both were refused and
are recorded here rather than dropped. Each is a numeric cut over eight observations whose value
comes from looking at where the offending case falls, and a threshold chosen that way is the
suppressed finding wearing an arithmetic costume. The count threshold of three carries the same
objection: the flagged line has exactly three.

The gate therefore closes red on this single finding. The registration's substance is untouched, the
flagged sentence is accurate, and no word of it was altered. A red gate that states the truth was
preferred to a green one obtained by any route available. The repair is deferred to Track B, where
the discriminator and the window are designed together.

## D-V30A-12 — an exemption was added to the checking instrument during the close-out it certifies

**True:** at commit `664cee7` an entry was added to the enumeration-exemption table keyed to the
region of the review register containing the flagged sentence. Before it the stage failed; after it
the same site reported as exempt. The entry was written in the same commit as the sentence that
triggered it. At commit `dd12d82` it was reverted.

**Expected:** an instrument inside the registered set to be unchanged by the work it grades.

**Why it stands as a disclosure:** the revert removed the effect and cannot remove the fact. The
entry would not have been written had the triggering sentence not existed, which is what separates
an exemption from a repair. The stage ran green on the changed instrument across three planning
rounds before anyone ran the tagged instrument against the current tree; that comparison surfaced
from a measurement requested for an unrelated reason. A check named `frozen_instrument_delta` now
runs the tagged checker, its digest verified against the attested value, against the working tree at
every invocation.

## D-V30A-13 — a line-pinned citation carried a number its own recorded reason contradicted

**True:** the citation table pinned the kill-gate ledger heading in `HISTORY.md` to line 277 while
the same entry's reason recorded that the citing document cites the heading rather than a line. No
file in the tree contains the string naming that line. Three ceremony documents state the citation
is by heading; one records the same heading drifting between line numbers at an earlier round. The
table's own convention assigns a null line to heading-cited entries. The heading stood at line 277
when the tag was made and stands at 281 now.

**Expected:** a pinned value consistent with the reason recorded beside it.

**Why it stands:** the entry was re-keyed to the anchor at commit `1b0b1d0`. The ground is that the
value contradicted its own reason and asserted a claim no document has made, not that the alternative
was inconvenient. An audit of the table against its reason column reaches the same place without any
knowledge of this close-out. The tagged instrument still carries the number, so the two instruments
disagree on this check by design, and that difference is the one difference the delta check permits.

## D-V30A-14 — the enumeration window is asymmetric, and its description was wrong wherever it was written

**True:** the window reaches one line back and three lines forward from the flagged line. The slice
indexes a zero-based list with a one-based counter, so the arithmetic reads as symmetric and is not.
For the flagged sentence the window reaches a heading three lines below and takes a fourth path from
it — a path absent from the flagged line. One tracked file described the window, as a five-line span
with symmetric bounds; the span is corrected at commit `f158381` and the indexing cause is named
there. The message of commit `664cee7` describes it as a two-line window and is not rewritten.

**Expected:** a description matching the code.

**Why it stands:** the five recorded exemption tuples were derived from this window and reconcile
against it exactly. Narrowing the window to the flagged line alone changes three of them and raises
a fresh finding on each. The repair is deferred to Track B alongside the discriminator, because a
discriminator design changes what window is correct and fixing one first constrains the other. The
window is not the cause of the false positive: the flagged line carries three registered basenames
on its own and fires without any window at all.

## D-V30A-15 — a third instrument difference was nearly reported and belonged to the harness

**True:** comparing the tagged checker against the current one, a control-character failure appeared
in the tagged instrument's output and in neither instrument's behaviour. The exemption region is
byte-identical in both. The cause is a relative root: the control-character check resolves a path to
absolute and then takes it relative to the root it was given, which raises when that root is
relative, and the fallback keys the entry by a name missing its leading directory, so a real
exemption misses. With an absolute root the tagged instrument reports two failures rather than
three.

**Expected:** a comparison between two versions of an instrument to report differences between the
instruments.

**Why it stands:** the artifact was caught by confirming the region byte-identical in both versions
before reporting it. Its cause was mis-stated for two rounds as an effect of running the script
outside its own directory; the lost prefix was the symptom. The delta check named in D-V30A-12
extracts the tagged instrument into the same relative location and passes an absolute root, and the
absence of this failure is that harness's own test. A first harness built on a fresh worktree
manufactured two different failures, over four cache paths present in the working tree and absent
from a new worktree, and was discarded for that reason.

## D-V30A-16 — the checker's result depends on whether its root argument is absolute

**True:** the control-character check resolves each manifest path to an absolute path and then takes
it relative to the root it was handed. A relative root makes that operation raise, and the fallback
keys the entry by a name whose leading directory is gone, so an exemption keyed to the full name
finds nothing to match. Measured on the tagged instrument against this tree: with a relative root,
three failing checks and ten findings; with an absolute root, two failing checks and two findings.
The difference is entirely in the invocation.

**Expected:** a result that is a property of the tree and the instrument, not of the form in which
the instrument was called.

**Why it stands:** every invocation path in the repository was surveyed and none of them passes a
relative root. The argument's default is the parent of the script's own resolved location, which is
absolute, and each documented command omits the argument: the install and verify instructions in the
README, the ceremony commit plan's gate line, the ceremony checklist, the readiness document's two
gate lines, the amendment diff's two, the ledger's, and the three scripted callers that spawn the
checker as a subprocess. The registration tests pass no root either. Of the committed transcripts of
checker runs, eight record an absolute root and two record a relative one; both of the latter predate
the control-character check, whose name does not appear in either transcript, so neither carried the
spurious failure. The gate's recorded history is unaffected.

The repair is deferred to Track B and joins the enumeration discriminator and the window there. The
reason is the one that governed the other two: a change to the instrument during the close-out that
the instrument certifies, against a gate pinned to a single known finding, for a defect that is now
measured and written down. The check named in D-V30A-12 passes an absolute root explicitly, so the
comparison it performs is not exposed to this.

## D-V30A-17 — two corrections to the record above, made by addition

**True:** D-V30A-15 records that the artifact's cause was mis-stated "for two rounds". It was
carried in four successive planning documents, each of which prescribed extracting the tagged
instrument into a matching relative location on the strength of the same wrong diagnosis. The count
in that entry understates the span.

**True, second:** the harness those documents prescribed was built and measured before being
accepted, and it manufactured two failures of its own — one over manifest paths absent from a fresh
tree, one over working files absent from it — naming cache paths that are present in the working
tree and absent from a newly created one. It was discarded on that measurement. The comparison
described in D-V30A-12 extracts the tagged instrument to a plain file and runs it against the real
tree with an absolute root, and its acceptance test is that exactly one check differs between the
two instruments.

**Expected:** an entry whose figures match the record it summarises.

**Why it stands as an addition rather than an edit:** this file is append-only, and the entry above
was committed in an earlier round. Correcting the figure in place would leave no trace that the
record once said something else, which is the property the append-only form exists to preserve. The
earlier entry is left as written and is read together with this one.

## D-V30A-18 — §6.2 criterion 3 has no scoring key that reaches the tool's output

**True:** the ground-truth map and the scorer that adjudicates against it are stated in different
units, and no declared correspondence joins them.

The map's cell key is declared and named twice in the availability declaration, at line 1617 and
again at line 2153:

> (`side`, `instrument`, `month`, `class`) — the unit this declaration partitions the fixture into.

The scorer consumes a different unit. Its labels carry `leaking_pairs`, a set of pairs of a feature
and an affected output cohort, and the tool emits a cohort identifier of the form `col:<frame>.<column>`
— a column of a frame. A cell of the map is an availability class over an instrument-month; a pair
in the labels is a column. Neither is derivable from the other without a statement of which classes
implicate which columns, and the registration contains no such statement.

**Searched, with the population named:** the availability declaration, for `leaking_pairs`, for a
feature and cohort co-occurring, and for the `col:` cohort prefix. Zero matches for each. The
declared class set is the ten named at declaration line 2164 — trades_all, trades_buy, trades_sell,
trades_large, mbo_all, mbo_bid_add, mbo_ask_add, mbo_bid_cancel, mbo_ask_cancel, mbo_cancel_any —
and the column ground truth is the thirty-five columns of the fixture manifest, classified 25
LEAK-SOURCE, 6 DESCENDANT, 4 CLEAN. Nothing maps the first set onto the second.

**Expected:** a scoring key that reaches the tool's output, so findings can be adjudicated against
the cells the map declares.

**Why it stands:** the correspondence is not plumbing, and it is not available to be written now.

Which classes implicate which columns decides whether a finding counts as hitting a predicted cell,
so different plausible correspondences produce different criterion-3 numbers. That makes it the
scoring key, and §6.2 SC-3(e) registers one scoring key and only one. SC-3(h) registers the map as
declared and frozen before any detector runs, and records that a map frozen after a run is a key
shaped by the result. Detectors have run: the column-dependency and null-reading sweeps covered the
fixture, both probes executed, and the availability probe was wrapped in the frozen output contract.
Their behaviour is known. A correspondence authored at this point would be a part of the key chosen
after the freeze with the fixture in hand.

The registered surface is closed, so a correspondence the registration does not declare is not
addable except through an amended and signed registration.

**Recorded in the repository before this round.** The Phase 1 harness carries the position in its
own words: *"This file holds no labels either; it is here so that when scoring is added, it is added
on this side of the boundary."* The scoring half was known to be absent; what this entry adds is
that it cannot be completed as the registration stands.

**Carried consequence:** criterion 3 is unscoreable as registered, and §6.2 is therefore unsatisfied
rather than failed. Criteria 1, 2 and 4 are scoreable, because each is keyed by column and the
column ground truth exists. A run of those three is not a gate result, since §6.2's criteria as
amended are the whole gate.

**Two populations, each naming what it counts (SC-3(a)).** Statements about how much the corrected
side leaks depend on which count is meant, and both are true of the same map:

| population, on SCORED cells of the corrected side | instrument-months |
|---|---|
| `strict_count > 0` — strictly-post-decision absorption | **18 of 48** |
| `equal_count > 0` — same-second absorption | **35 of 48** |

The first is the figure the declaration carries at lines 1625 and 1889. Earlier reports of "18 of
48" did not name the population, and a reader taking it as the count of instrument-months that leak
at all would understate the corrected side by seventeen.

## D-V30A-19 — the map's own figures reconcile, and are recorded here

**True:** the map artifact holds 984 rows: 960 declared-class cells, being two sides by eight
instruments by six months by ten declared classes, plus 24 rows of the eleventh class `mbo_all_rows`,
which the declaration declares diagnostic and which are not cells. Of the 960, 888 are SCORED and 72
are UNSCORED_FOR_LACK_OF_DATA. The boundary field reads `decision_T` on every row. The scope is eight
instruments — cl, es, gc, he, le, nq, zc, zs — over six months.

**Expected:** the artifact to match the declaration's description of it.

**Why it stands:** it does. Each figure above was recomputed from the artifact and compared with the
declaration's own statement of it, and every one agrees. This entry records the reconciliation so
that the defect disclosed at D-V30A-18 is not read as a defect in the map. The map is sound; what is
absent is a correspondence between its unit and the scorer's.

## D-V30A-20 — D-V30A-18's criterion-3 finding is withdrawn: the correspondence is registered

**True:** entry D-V30A-18 records that criterion 3 is unscoreable as registered, on the ground that
the declared map's cells and the runtime scoring unit are in different units with no declared
correspondence joining them. **That ground does not hold.** The correspondence is registered, and
this entry supersedes D-V30A-18's carried consequence. D-V30A-18 and D-V30A-19 are left as written;
this entry is read with them.

**What the registration carries, with citations.** Each was located after D-V30A-18 was committed.

- The scoring unit is registered at `PREREG.md` line 291 as the feature and the affected output
  cohort, and section 7.2 distinguishes probe cohorts, which corroborate, from the affected output
  cohort, which keys the unit.
- Criterion 1's denominator and the rule constituting it are registered at `PREREG.md` line 702,
  which states that the denominator is derived from the declared map by the rule registered there,
  and that the declaration shows the derivation. Three classes are registered: required, out of
  jurisdiction, and unscored.
- The declaration carries the derivation per unit, ex ante, at its section A.6, with the required
  list at line 1316 and the count of eleven stated as the only quantity that is N.
- The class-to-column correspondence is carried in the required table's fourth column, headed
  **Governing map class**: eight columns governed by `trades_all`, one by `trades_sell`, one by
  `trades_large`, and one by `trades_all` through a merged aggregate. With the side, instrument and
  month supplied by the case identity, that completes the map's four-part cell key for every unit of
  the criterion-1 denominator.
- The coverage limit is declared too. Section 13(j) records that none of the thirty-five fed columns
  is MBO-fed, so the six MBO classes attach to no fed column; they remain scored cells of the map and
  what changes is what they may be quoted for.
- The consequence was disclosed in the registration itself, at `PREREG.md` line 1435: criterion 1's
  effective requirement reverses on fourteen of the twenty-five leaking sources, eleven being
  required, thirteen out of jurisdiction and one unscored.

**Expected:** an absence claim about a registered document to rest on a stated search population,
as every other absence claim in this record does.

**Why it stands as a correction rather than an edit:** the four claims below were each asserted from
a partial read, and each is recorded here with what was believed and when, because the record showing
a wrong statement followed by its correction is worth more than a record showing neither.

| asserted | when | measured |
|---|---|---|
| the map's cells and the scoring unit have no declared correspondence | at D-V30A-18 | the required table's governing-class column carries it |
| criteria 1 and 2 are not scoreable, the ground truth being unreachable | after D-V30A-18, in report only | the finding's feature field carries the moved output column, which is the unit the criteria are keyed on |
| criterion 2 is vacuous, none of its clean columns being reachable | after D-V30A-18, in report only | measured against probe cohorts, the wrong population; one of the four clean columns is present in the built output |
| criterion 1's denominator is twenty-five | implicitly, in report only | the registered denominator is eleven, and no other quantity is N |

Only the first of the four reached this file. The other three were reported and are recorded here so
the sequence is legible.

## D-V30A-21 — the tool discards the field the registered scoring unit is keyed on

**True:** the finding record declares three distinct fields — the feature, the affected output
cohort, and the probe cohort. At `src/leakaudit/probe.py` lines 319 and 320 the tool writes the
probe cohort's identifier into both the probe-cohort field and the affected-output-cohort field, so
the two carry identical values on every finding the tool emits.

The information the second field wants is present at that point. Three lines earlier the comparator
returns the set of output columns that differ between the baseline build and the perturbed one, and
the loop iterates that set; the feature field is populated from it correctly. The dependency map the
same run publishes records those moved outputs, and they cover eight of the eleven units of the
criterion-1 denominator.

**Expected:** three declared fields to carry three values.

**Why it stands:** it is recorded rather than repaired in the round that found it. The repair
conforms the tool to a registered contract and writes no registration, so it is a defect repair
rather than a choice of scoring key; it is ruled, disclosed and tested against a known positive
before its clean result is relied on.

**Carried consequence:** while the field carries the probe cohort, the registered scoring unit
degenerates from the feature and its affected output cohort to the feature and the probe cohort.
Whether a criterion-1 result computed in that state means anything is not settled here.

## D-V30A-22 — three required columns and three clean columns are absent from the built output

**True:** the criterion-1 denominator names eleven columns. Built from the acceptance fixture's
corrected side for one instrument-month, the output frame carries 338,159 rows and 87 columns, and
**eight of the eleven are present in it. Three are not: `trade_volume_1s`, `trade_count_1s` and
`dollar_volume_1s`.** They are absent from the frame, not present and unmoved.

Of the four columns the fixture manifest classes as clean, **one is present in that output frame —
`minutes_since_open` — and three are not**: `session_open`, `session_mid` and `session_close`.

Measured on the corrected side of one instrument-month, zc 2025-01, by building the fixture and
reading the frame's columns. The population is that build; other instrument-months are not measured
here and the figures are not generalised to them.

**Expected:** the columns a criterion scores over to exist in the artifact the criterion is
evaluated on.

**Why it stands:** it is disclosed rather than resolved, because which of two readings applies is not
established. The absent columns may be produced on a side or an instrument-month not measured here,
or the fed-column set the manifest records may differ from the built frame's columns for a reason
the declaration states elsewhere. Both are checkable and neither is checked here.

**Carried consequence:** a criterion-1 result computed on this build has at most eight of its eleven
denominator units observable, and a criterion-2 result at most one of its four clean units. Any such
figure names that coverage beside it.
