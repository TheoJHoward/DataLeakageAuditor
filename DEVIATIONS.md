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

## D-V30A-23 — criterion 3 is scoreable, and D-V30A-22's absent columns have a declared reason

**True, and this entry supersedes two carried consequences of earlier entries.** D-V30A-18 recorded
criterion 3 as unscoreable; D-V30A-20 withdrew that on its ground. This entry answers the question
D-V30A-20 left open — whether the correspondence reaches far enough — and it does. D-V30A-22
recorded six columns as absent from the built artifact; the absence has a declared reason and is not
a defect.

**Criterion 3's scored population is fully dispositioned, and every disposition is declared before
any detector runs.** The criterion scores over the map's cells: the criterion's own clause registers
that the map covers the whole declared scored population, and the declaration's criterion-3 entry
lists what it supplies under it — the artifact and its schema, the named cell key, the ten violation
classes, the declared scored population and its subclasses, the per-cell expected findings, the
unscored ledger, and the reporting re-aggregation. Of the 960 declared-class cells:

| cells | how the population is reached | declared at |
|---|---|---|
| 288 | the governing-class column of the required table, three classes | section A.6.1 |
| 576 | the six MBO classes, attaching to no fed column | section 13(j) |
| 96 | the `trades_buy` class, a degenerate unit excluded before any run | section C.4(a) |

The third was the residue this record would otherwise have reported as undeclared. It is not: the
class is zero strict and zero equal in every one of its 96 cells on both sides, because the buy-side
aggressor test matches none of the values the source actually carries, so the column it feeds is
identically zero. It is excluded on the registered degenerate-unit ground, declared out before any
run, and its reporting as excluded rather than as missed is registered too.

**The six absent columns are Phase-7-added, and the declaration says so.** The declaration carries a
section for the columns Phase 7 feeds that are absent from the Phase 5 set — nine of them, tabulated
with a declared role and verbatim construction evidence for each. The six recorded absent at
D-V30A-22 are a subset of those nine. The build measured there was the Phase 5 builder, which by
declaration does not carry them.

So the ceiling recorded at D-V30A-22 is an artefact of which stage was built, not a property of the
fixture. **The columns are absent from the Phase 5 frame, not from the fixture**, and D-V30A-22's
two open readings are closed by the first of them.

**Expected:** a measurement to name the stage it was taken at, as it names its side and its
instrument-month.

**Why it stands:** the operational consequence is worth recording, because it decides where a run of
criteria 1 and 2 would have to happen. Eight of the eleven required units and one of the four clean
units are present in the Phase 5 frame; three required and three clean are added at Phase 7. A probe
over the Phase 5 frame therefore cannot observe the whole of either criterion's population, and the
surface a scoring run needs is the frame that carries all thirty-five fed columns. That is a fact
about where to run, not a defect in what was run.

**Populations, named.** The cell figures are over the 960 declared-class cells of the map artifact,
the 24 diagnostic rows excluded. The column figures are over one build: corrected side, zc 2025-01,
338,159 rows and 87 columns, and they are not generalised to other sides or instrument-months. The
readings behind this entry were taken by enumerating the sections that would house each answer, by
their own headings, and reading them; the enumeration is the population, and it replaces the keyword
searches that produced four wrong absence claims in the three rounds before this one.

## D-V30A-24 — "declared before any run" is verified from the history, and the ceiling is a stage, not a defect

**True:** three dispositions carry the whole of criterion 3's scoreability and the exclusion of 96
cells between them — the governing-class column of the required table, the six-class coverage limit,
and the column-level gate dispositions whose heading asserts that they are declared before any run.
That assertion is now checked against the commit history rather than taken on its own word.

| what | commit | date |
|---|---|---|
| the declaration's first commit, carrying all three dispositions | `ffa6d94` | 2026-08-13 |
| the governing-class column revised | `0acab4e` | 2026-08-25 |
| the column probe and the two detectors | `6e256d1`, `66063da` | 2026-08-26 |
| the dependency-map run and its results | `e84c711`, `7e8b902` | 2026-08-26 |
| the detector sweep's results | `8121549` | 2026-08-26 |
| the availability probe | `2ceb3c9` | 2026-08-27 |
| that probe under the frozen output contract | `e943799` | 2026-08-28 |

**Every disposition predates every run, by thirteen days.** The later revision of the governing-class
column predates the first run by one. The claim holds.

**The degenerate-predicate disposition anticipated the run that would have found it.** The
column-level dispositions record, on 13 August, that the buy-side aggressor test matches none of the
values the source carries, so the column it feeds is identically zero and its class is zero in every
one of its 96 cells on both sides. The dependency-map machinery surfaced the same constantly-false
predicate on 26 August. The order is the favourable one: the registration named the degeneracy
before any detector was in a position to report it.

**Expected:** an ex ante claim to be verifiable as ex ante.

**Why it stands:** it is recorded because three dispositions now carry weight they did not carry
before, and because the check is cheap and was not otherwise going to be made. A disposition frozen
after a run scores nothing under the criterion's own clause; these were not.

**The clean columns are disposed of, and the two questions about them are different.** Their absence
from the measured frame and the treatment of a finding on them are separate matters with separate
answers. The absence is the Phase 7 addendum's: they are among the nine columns Phase 7 feeds that
the Phase 5 set does not carry. The treatment is the column-level dispositions': the session flags
are lagged deterministic clock functions, which is staleness rather than unavailability, declared as
a documented as-built property so it cannot later be re-read as a discovery, and licensing no
corrected-side finding.

**Criterion 1's ceiling is a stage, and the stage is reachable.** The fed set is defined in the Phase
7 simulator, one of the registered twenty, as the thirty-five features its two feature lists compose.
The frame measured at D-V30A-22 came from the Phase 5 builder, which the declaration records as
carrying nine fewer. So the ceiling of eight of eleven recorded there is a property of which builder
was called, and the whole denominator is present in the frame the fed set is defined over.

**Populations, named.** The dates are over the commits reachable from the current branch tip, found
by searching the declaration's history for each disposition's own distinctive text and by taking the
first commit that added each run's artifact. The column figures remain those of one build: corrected
side, zc 2025-01, 338,159 rows and 87 columns, not generalised to other sides or instrument-months.

## D-V30A-25 — three units of criterion 1's denominator are absent from the artifact its criteria are evaluated on

**True:** criterion 1's denominator is the eleven units the declaration derives at its section A.6.1,
drawn from the thirty-five-column fed set. The criteria are evaluated on the rebuild pair, whose
column universe the declaration gives as the forty-five-column set of the earlier builder. Three of
the eleven — `trade_volume_1s`, `trade_count_1s` and `dollar_volume_1s` — are among the nine columns
the later stage adds and the earlier set does not carry, so they are absent from the frame the
criteria are evaluated on.

Measured on one build of that frame: corrected side, zc 2025-01, 338,159 rows and 87 columns. Eight
of the eleven are present in it and three are not. The figure is not generalised to other sides or
instrument-months, and it is a property of that frame rather than of the tool.

**Expected:** the units a criterion scores over to be present in the artifact the criterion is
evaluated on.

**Why it stands, and how the registration disposes of it.** Three registered rules settle this
between them and none of them is discretionary.

The denominator does not move. It is derived from the declared map by the rule the registration
carries, and reachability is not that rule. Scoring the criterion over the eight that are reachable
would substitute a different denominator for the registered one, and the count of the required list
is the only quantity that is N.

Neither registered exclusion ground reaches them. Exactly two are registered: a degenerate unit that
cannot carry a finding of the scored class at all, and a unit whose construction or lag treatment is
declared unresolved. Absence from the evaluation artifact is neither, and reinstating or removing a
unit is a class C amendment in any case.

The state they take is registered, and it is not `unscored`. The unscored state is entered only by a
unit named in the declaration's unscored ledger with its ground, frozen before any detector runs, and
the registration states expressly that absence of data at run time is not that state but the not-run
state its cause selects. The section that selects it draws the boundary: missing or impossible inputs
are `unsupported`, supplied-and-valid inputs that then fail are `could-not-run`. These three are
missing inputs on this frame.

**Carried consequence:** on the rebuild pair, criterion 1 has eleven required units of which eight
are observable and three take the `unsupported` coverage state, on the ground that the column is not
present in the evaluation artifact's universe. The registration adds that an entry in that state may
name a covering detector, which reduces the gap without closing it, and that none of these states is
displayed in a way mistakable for a pass. A published criterion-1 figure therefore carries all three
numbers — the denominator, the observable count, and the unsupported count with its ground — and a
result at eight of eleven is a statement about the artifact rather than about the detector.

**Populations, named.** The eleven are the required list of the declaration's section A.6.1. The
thirty-five and the forty-five are the two column universes the declaration names in its two artifact
sections. The eight and the three are from the single build named above. The reading was taken by
enumerating the exclusion clause, the unscored clause and the not-run states section by their own
headings and reading them, and that enumeration is the population of the read.

**What this entry does not decide.** The re-derivation of the two artifact-allocation sentences is
already recorded elsewhere as a disclosure-class item requiring a further amendment; this entry names
a consequence of that allocation which that record does not name, and does not reopen it.

## D-V30A-26 — a pre-commitment was frozen on a refuted premise, and the cohort it turned on is a set of rows

**True, and in the order it happened.**

A pre-commitment for the acceptance run was committed and pushed. Its stated
premise was that the criteria are scored from a finding's feature field alone and
that the affected-output-cohort field is an input to none of them. A run began
against it and reached the end of its first side.

The premise is false. The event's pair is the feature together with the affected
output cohort, and every metric in the registered machinery is gated by a match of
that pair against the labels — the two yields, the conditional recall, the cohort
sensitivity, the unprobed rate, and the feature discovery recall, which projects
to the feature but filters through the pair match first. Not one reads the feature
alone.

The run was stopped before the premise was checked, and no output was read at any
point. That ordering is what preserved the pre-commitment property for whatever
is written next: nothing was seen, so a later expectation is still genuinely
written before a result.

**Expected:** a claim recorded as unverified to be verified before it is frozen,
rather than after.

**Why it stands:** the pre-commitment is void as a pre-commitment and superseded.
It is not edited, amended or deleted. Editing one stops it being a
pre-commitment; deleting one removes the record of the premise it froze. Its
output is quarantined under a directory named for it, with a README stating its
status, and the three files' digests were recorded before anything moved them —
which is what makes "never read, never altered" checkable rather than promised.
The digests were recomputed after the move and are unchanged.

**The machinery is registered, and that settles the direction.** The metrics, the
gates and the event derivation are all defined in the runtime reference module,
which is one of the twenty hashed paths and is byte-identical to what the tag
attests. Its behaviour is not a candidate defect; the tool conforms to it.

**What the registration means by cohort, established by reading the sections that
define it rather than by inference.** A mask built for a decision time corrupts
the cells unavailable at that time; for an output ROW whose own decision time is
earlier, the unavailable set is larger, so that row can leak silently. A change at
any row whose decision time is at or before the mask's is a valid finding, and
silence is informative only for the rows whose decision time equals it. The
scoring unit is then locked as the feature together with the affected output
cohort.

**So a cohort is a set of output ROWS sharing a decision time.** It is not a
column. The availability probe emits cohorts of exactly that kind — its cohorts
are seconds, and a cohort whose in-second rows moved carries a finding. The column
probe emits cohorts that are columns of a frame.

**Carried consequence:** the affected-output-cohort field as the column probe
writes it does not denote a decision cohort under either form it has carried — not
the probed input column it held until this round, and not the moved output column
it holds now. Both name columns. The repair is therefore neither confirmed nor
simply reversible, and it is left in place rather than reverted on suspicion; its
own test still shows the field carries what the code intends, which is a different
claim from carrying what the registration intends.

**What this makes open.** Supplying the labels for this detector requires stating
what its affected output cohort is, and the registration's answer is a unit the
detector does not emit. Constructing that correspondence now would be choosing a
component of the scoring key after the detectors have run, which the registration
forbids for the same reason it forbids a map frozen after a run. It is recorded
here and not chosen.

**Populations, named.** The field question was settled by reading the metrics
function and the event derivation in the runtime reference module, and the lines
are quoted in the round's report. The cohort question was settled by reading the
section that defines a probe's silence and its cohort, the scoring-unit table, and
the display requirement that a finding print its probe cohort and its affected
output cohort as two separate things; the enumeration of those sections is the
population of that read. The digests are of the three quarantined files as they
stood before and after the move.

## D-V30A-27 — the acceptance criteria attach to two named detector rows, and the instrument seven rounds of field work went into is not one of them

**True, and stated plainly rather than reorganised around.** The instrument the acceptance
criteria are evaluated on is the availability probe, with the label probe where it applies. The
field work of the preceding eight rounds, the affected-output-cohort repair, and the harness the
void pre-commitment named were all aimed at the column probe, which the acceptance section does
not score.

**How the attachment is established, by reading the sections that carry it rather than by keyword
search.** The criteria adjudicate *runtime findings*, and the first of them turns on whether the
finding's promotion status makes the reported tier proven or review. The tier section defines a
runtime finding by that field and draws the boundary in terms: the review rows that are not
runtime detectors are named and excluded. The metrics section then assigns both runtime rows —
preserving and promoted — to exactly two rows of the coverage map and to no others. The coverage
section says of those same two rows that they emit at a tier derived from promotion status alone,
which is the exact property the first criterion turns on. The declaration section records that
every finding of those two rows prints its declaration and its cohorts. The kill criterion gates
both of their combinations by name; the ambiguity-branch clause computes its yield per runtime
detector. The routing clause makes jurisdiction between detectors a declared object, and the
declaration performs it in those terms for the fixture's one dual-ground column. The coverage
table closes itself: eleven detector rows, and the table is the scope.

**The negative half of the population, because an attachment claim needs one.** The column probe's
identifier appears in no registered document — not the specification, not the design companion,
not the declaration. Neither do the two identifiers of the value-read and null-read detectors. The
phrase the machinery keys its records on appears in the specification zero times.

**The tool said so in its own header, from the day it was written.** The column probe's module
documents that its cohort is one whole source column and states that it is not a decision cohort,
because that layer has none, because it has no availability model. The coverage row it would have
to be needs an availability model. It is therefore neither of the two rows, and the header was
never in disagreement with the registration — only with the reader.

**Expected:** work on an instrument to begin by establishing which row of a closed enumeration
that instrument occupies.

**Why it stands:** the enumeration is closed, and it was closed before any of this work started.
Nothing in the tool changes as a consequence of this entry, and nothing is reverted on account of
it. What changes is which artifact a later acceptance run reads.

---

## D-V30A-28 — the acceptance gate cannot be executed as registered: its ground truth and its scorer are declared in different units

**True.** The declared expected findings are enumerated per column and counted per cell. The
scoring machinery is keyed on a pair whose second element is a decision cohort. No declared object
crosses between the two, so the labels the machinery consumes cannot be transcribed from the
declaration — they can only be invented, and inventing them after the detectors have run is
choosing a component of the scoring key after the fact.

**The population of the read, by heading.** The conformance walk's criterion-3 subsection, which
names its own supply list; the ground-truth map section and its subsections (a) through (d); the
two-sided enumeration section with its per-column tables and its column-level dispositions; the
required-list subsection of the walk. Then, on the other side: the section defining a probe's
silence and its cohort, the runtime scoring-unit table, and the labels, event and metric
definitions of the reference reducer.

**What the declaration supplies, in its own words.** The map artifact and its schema; the cell key,
named — side, instrument, month, class; the declared violation classes; the declared scored
population; the per-cell expected findings; the unscored ledger; the reporting re-aggregation. The
cell key is named and it is not a cohort. The map's schema carries a boundary field, two violation
counts and a row count per cell, and its boundary reads the same value on every row.

**What the per-cell expected findings actually look like.** The two-sided enumeration lists them by
column, each with the map class that governs it; the required-list subsection does the same for the
eleven units of the first criterion's denominator. The per-instrument-month statements are counts
and rates, not row sets.

**The one row-level object, and why it does not close the gap.** The declared cohort predicate says
a row shares a wall-clock second with its predecessor. It is a predicate over output rows, and it
is checkable before any detector runs from the lattice timestamp alone — but it is one set per
side rather than a family indexed by decision time, and the declaration itself declares it
necessary and not sufficient: in-cohort means a violation is possible and adjudicated against the
map cell. Its own figures make the insufficiency measurable — the cohort is 1,966,088 rows of
24,768,472 corrected rows, of which at least 1,024,196 violate in some class, leaving up to
941,892 that violate in none. The declaration records that it does not know which cohort rows
leak, and it never states it per column at all.

**Why that is fatal to transcription rather than merely awkward.** The labels object is a frozen
set of feature-and-cohort pairs. The cohort sensitivity metric intersects the labels' cohort
strings with the identifiers the detector itself emitted, so the labels' cohort component lives in
the detector's own identifier namespace. Nothing declared is in that namespace, and no declared
rule maps a cell of the map into it. The freeze clause asks that every declared object the gate
consumes be regenerable and checkable from the declared inputs alone before any detector runs; the
pairs are not.

**Expected:** a signed registration's ground truth and its scorer to be stated in the same unit.

**Why it stands:** it is a finding about the registration, not a blocker on the tool, and it is
recorded as one. No labels producer is built. Closing the gap decides what every published gate
number means and is therefore class C, which is the author's and not an implementer's. The
partial-scope note that follows from it: the criteria of the acceptance section are themselves
worded at column granularity, while the metric family and the kill criterion's gates read the
pair — so the blockage is not uniform, and which level the section is scored at is part of the
same decision.

**How it was found, recorded because the method is the transferable part.** By a discipline that
forbade supplying the missing piece. Each earlier round proposed a repair at the level of a field;
each was refused for want of a declared source; the refusals accumulated until the question moved
from which value a field carries to which unit the registration declares, and there the answer was
already written down in two incompatible places.

---

## D-V30A-29 — criterion 5's own instrument had never measured the thing it names, and asserted a falsehood while declining to

**True.** The registration checker carries a check named for installability, wired to the release
stage and cited to the kill criterion with the only date on it. Its body returned "the installable
package does not exist yet; this check cannot pass before the implementation it verifies". The
package had existed for days: packaging metadata, two shipped packages, a recorded install into a
clean directory and an import from that installed copy alone.

**And the front page asserted the same falsehood, more visibly.** The repository's README stated
that it is a pre-registration and not a tool, and that no detector implementation exists. Both
sentences were true when written. Both were false by the time anyone read them, on the public
front page of a public repository.

**What was done, and in what order.** The check was implemented against the real package, over six
limbs, each of which is a defect that happened here rather than one imagined for completeness:
packaging metadata that exists and parses; a declared licence file that is present; every
first-party package a shipped module imports being itself shipped; every declared package
directory existing and carrying a module; every third-party import of a shipped module being a
declared dependency; and a front page that is true and names the install document. The third limb
is the one that fired for real — a shipped module imports the reducer package, that package was
absent from the first distribution, and the install succeeded and then raised on first use after
the metadata build had already gone green.

**Its clean result was not believed until it had failed.** Twenty-two cases were written before the
result was quoted: one violating synthetic per route, a negative control that stays silent, a
paired test that the historical defect's synthetic goes silent once the package is shipped, a case
proving the false front-page claim is caught across a line wrap because the real one was wrapped,
and a case proving that quoting a retired claim inside a blockquote does not fire — so that the
check cannot push the repository into deleting its own history to go green.

**What the check does not do, recorded beside what it does.** It builds nothing, installs nothing
and imports nothing, and it reads one machine's checkout. Its passing note says so in its own
output. The dependency floors are untested downward against an older resolution of one of them,
and that stays recorded as unknown rather than disposed of by widening or pinning them.

**Expected:** the instrument for a dated obligation to have been pointed at the obligation.

**Why it stands:** the check was a placeholder that outlived its subject, and a placeholder that
asserts the subject does not exist is worse than an absent check, because it reads as a measurement.
The corrected sentences on the front page are recorded as corrections rather than deleted, for the
reason the ledger exists.

## D-V30A-30 — the availability probe's trace emitter kept one moved column per cohort and discarded the rest

**True.** The trace builder recorded the alphabetically first column that moved
in a probed second and dropped every other one. The probe itself had them all —
its cohort record carries the full tuple of moved columns — so the loss happened
at the boundary between the probe and the registered output contract, and it is
silent: a trace carrying one finding where ten belong is well formed, resolves
legally, and reports a completed schedule.

**It is wrong in both directions the two scoreable criteria turn on.**

The first criterion asks that every ground-truth leaking source column receive a
finding attributed to **it**. Ten columns moving in one second produced one
attribution and nine silences, and the criterion would have read as nine misses
that never occurred — an understatement of the tool, which is the direction
people notice.

The second criterion forbids a finding of any tier on a manifest-clean column on
the characterized side. A clean column that moved and sorted after the survivor
disappeared from the trace entirely — a false negative in the direction that
hides a violation of the criterion the tool is being examined by. **A detector
whose trace can silently drop its own false positives is grading itself**, which
is the defect the registration's own note about primary and secondary
classification was written against.

**The registered unit was never one record per cohort.** An evidence event is
keyed on the detector, the promotion status, the feature and the affected output
cohort, so two features in one second are two events by the registered
definition. The schedule resolver takes the set of strategy-and-cohort pairs, so
emitting several records for one cohort leaves the completion state meaning
exactly what it meant.

**Expected:** an emitter to carry what the probe measured.

**Why it stands:** the repair was made before the run that depends on it and is
disclosed in the pre-commitment rather than in the result, so no number here was
produced by an instrument changed after a number was visible. Eleven cases cover
the emission on synthetic cohorts; two of them were run against the replaced
emitter, fetched from the history by content, to establish that they fail on it —
a clean column sorting last, and ten required columns in one second. Both
produced one finding then and the full set now.

---

## D-V30A-31 — the front-page check excused every blockquote, and a live claim can sit in one

**True.** The criterion-5 check excludes blockquoted lines from its scan of the
front page, so that a retired claim kept on the record does not fire it —
otherwise the cheapest way to pass would be to delete the history, which is the
incentive this project exists to resist.

**The exemption was too wide.** It excused any blockquote at all. A blockquote is
used for emphasis at least as often as for quotation, so a live false assertion
parked in one would have passed the check while reading to a human as the page's
own voice. The exemption was right and its form was not.

**Narrowed.** A blockquote block is excused only where the block itself says the
claim is retired, matched over the whole block rather than per line — because
once the text wraps, the marker and the claim are rarely on the same line, which
is the same wrapping mistake the body scan had already made once. Every excused
block is reported as a note naming the marker that excused it, so an exemption is
visible rather than silent.

**Expected:** an exemption to be as narrow as its reason.

**Why it stands:** five further cases cover it — a marked block stays silent, an
unmarked one fires, an unmarked block of innocent text stays silent so the
narrowing did not make the check fire on blockquotes as such, the marker and the
claim on different lines are still matched, and the excusing note names its
marker. The question was asked by the planning layer rather than found by the
instrument, and it is recorded that way.

---

## D-V30A-32 — two of the four acceptance criteria are scored, on one instrument-month, and this is not a gate result

**True, and the order it happened in is the point.** A pre-commitment was
committed, naming the harness, the exact invocation, the inputs, the declared
lists, the disposition of everything unreachable, and one falsifiable
expectation per criterion. Then the harness ran once, exit 0, empty stderr. Then
its output was committed exactly as written. Nothing between those steps was
adjusted, and the two commits are in the history in that order for anyone to
check.

**The result.** Scored on the characterized side of the pair, for one
instrument-month of forty-eight.

- **The first criterion, denominator eleven: eight satisfied, three unsupported,
  none missed.** Each of the eight rests on at least one primary finding
  attributed to that column, in a declared cell the map records as non-zero —
  89,568 strict violations for the eight units governed by the all-trades and
  sell-trades classes, 23,633 for the large-trades one. The cell is checked per
  unit by the harness rather than carried over from the pre-commitment.
- **The three unsupported are the columns the later builder adds and the earlier
  one does not carry.** They are neither hits nor misses, they stay in the
  denominator, and no display puts them where a pass could be read.
- **The second criterion: the one reachable clean column receives no finding of
  any tier; the other three are unsupported on the same ground.** The reachable
  population is one, which the pre-commitment stated as thin rather than
  vacuous, and the thing that would have failed it did not occur.
- **The control side is silent** — 250 eligible cohorts, zero findings — which
  is the discrimination the pair exists to demonstrate.
- **No descendant column receives a finding**, which was a stated prior and
  holds.

**Twenty-one moved columns are in neither declared list, and they are named and
left unclassified.** They are the merge intermediates and the earlier builder's
order-book-derived columns; none appears in the thirty-five-column manifest,
because the frame the criteria run on carries eighty-seven columns while the
manifest describes the fed set of the other artifact. A column the manifest does
not carry is neither declared leaking nor declared clean, so it enters no
criterion. Choosing a state for it would be selecting a disposition the
registration does not select, which is the same move refused twice already this
round.

**Expected:** a stated expectation to be compared against a result, in that
order, with any difference reported as a finding.

**Why it stands:** it is recorded because the numbers are good and that is
exactly when a scope statement is worth writing down. **This is not a gate
result and is not published as one.** Two criteria of four; one instrument-month
of forty-eight; one side of two scored. The remaining two criteria are blocked
on the label gap recorded above, which is a finding about the registration
rather than a property of this run. Nothing here licenses a claim about the
tool's performance, and the run file carries every one of those limits as data
rather than as prose.

## D-V30A-33 — the violation predicate was reading equal counts as violations, and the tie rule says otherwise

**True.** The harness that scored one instrument-month treated a declared cell as
carrying no violation only when its strict count **and** its equal count were both
zero. The tie rule is declared `available`, so the comparator reads a value as
available when its instant is at or before the decision instant. **An event at
exactly the decision instant is therefore available, and an equal count is a
violation only under the branch the declaration did not take.**

**It changed nothing where it was written and two cells where it was extended.**
At the single instrument-month it was written for, the governing cells carry
89,568 strict, so the predicate never reached the equal counts. Across the whole
declared population two cells have zero strict and one equal — **es 2025-10 and
es 2025-11 on the corrected side** — and the old predicate would have scored them
as declaring a violation the declaration does not declare, then recorded a miss
when no finding arrived.

**Corrected before the run, not after.** The predicate is a strict count alone.
The correction is disclosed in the pre-commitment the run was made under rather
than in the result, so no number was produced by an instrument changed once a
number was visible.

**Expected:** a predicate to follow the declared branch rather than the union of
both branches.

**Why it stands:** the defect was invisible at the scale it was written at and
became visible only when the population widened. That is worth recording as the
shape of the thing rather than as a one-line fix: a predicate that is
conservative in the direction of finding more violations is not safe, because
here it would have manufactured two misses out of two cells the map declares
clean under the rule the declaration actually chose.

---

## D-V30A-34 — criteria 1 and 2 are scored across the whole declared population, and this is still not a gate result

**True, and in the order it happened.** A pre-commitment was committed and
**pushed before the run began**, so the ordering is checkable off this machine.
It enumerated the population, fixed the invocation, stated the cost model and its
halt, named what did not carry over from the single-instrument-month run, and
stated one falsifiable expectation per criterion together with four further
priors. Then the harness ran once, exit 0, empty stderr, 46,976 seconds. Then its
output was committed exactly as written.

**The population is the whole declared one.** Forty-eight instrument-months,
eight instruments by six months. The archive carries all forty-eight, verified by
enumerating the files the fixture's own loader reads. **Nothing was sampled and
there is no absence list.** One partial absence is recorded because it is real
and belongs to the fixture rather than to the run: one instrument carries no
order-book file in any of its six months, which the declaration already states,
and every required unit is trade-derived so no criterion is touched by it.

**The result.**

- **Criterion 1: 66 scoring contexts — 48 on the characterized side and 18 on the
  other, which is the count derived from the map before the run and matches the
  declaration's own list of eighteen. Across 726 unit contexts: 528 satisfied,
  198 unsupported, ZERO missed.**
- **Criterion 2: 48 clean, 144 unsupported, zero violated.** Its reach did not
  grow: **one reachable column per instrument-month**, forty-eight in total,
  exactly as it was for one, and the figure is never stated without that.
- **The three later-builder columns were predicted absent everywhere and are
  absent in all forty-eight on both sides.**
- **The dual-ground column's condition was asserted per instrument-month rather
  than inherited, and holds in all forty-eight.**
- **The control held in both directions:** thirty instrument-months silent where
  the map declares nothing, eighteen carrying findings where it does, split by a
  list computed before the run.
- **No descendant column received a finding anywhere.**
- **Forty-eight of forty-eight completed.** The named memory risk did not fire.

**Twenty-one features in neither declared list, and they are still named and left
unclassified.** Five appear in all forty-eight and sixteen in forty-two, the six
missing being the instrument with no order-book stream. **They are not coverage
and are never quoted as coverage.**

**Where the estimate was wrong, it was the half labelled unpredicted.** 13.05
hours against about eight. The term the single measured point actually measured
is the term the halt watched, and it never fired on any instrument-month. The
other term was refused as a prediction in advance, on the ground that one
warm-cache measurement cannot be extrapolated across a two-hundred-fold range,
and quoted only as an order of magnitude. The overrun landed there.

**Expected:** stated expectations to be compared against a result, in that order,
with any difference reported as a finding.

**Why it stands:** the numbers are good, which is exactly when the scope
statement earns its place. **This is not a gate result and is not published as
one.** Two criteria of four. The remaining two are blocked on the label gap
recorded above, which is a finding about the registration rather than a property
of this run, and no amendment has been opened. Nothing here licenses a claim
about the tool's performance.

## D-V30A-35 — the context count is true under a reading, and the reading travels with the figure

**True.** The population run's headline shape — **66 scoring contexts and 726
unit contexts** — holds under the reading that criterion 1 is scored per side and
instrument-month wherever the declared map carries a strict count. **Under a
contaminated-only reading the same run reads 48 contexts and 528 unit contexts**,
over the same output bytes, with the same zero misses.

**The reading, and its three grounds.** The routing clause satisfies a required
entry only by a finding on the side the map declares, which makes the first
criterion side-relative by its own incorporated clause, while the second names
the characterized side in its own text and the first does not. The derivation
reproduced the declaration's own list of eighteen corrected instrument-months
exactly, from the map, before the run — a reading that regenerates an independent
declared figure is corroborated rather than merely available. And it is the
harder reading: it adds eighteen contexts in which the tool could have failed. A
reading that made the examination easier would deserve suspicion; one that adds
tests to it does not.

**It is still a reading, and the figure carries it.** Wherever 66 contexts or 726
unit contexts appears, the reading appears with it. This is the same discipline
the register already records for a ceiling quoted four times with four values:
the figure is a property of the frame, and here the frame is interpretive rather
than numerical.

**What does not move under either reading.** Zero misses. Zero violations of the
clean-source criterion. Thirty silent and eighteen non-silent corrected
instrument-months, split by a list computed before the run. The three
later-builder columns absent in all forty-eight on both sides. The dual-ground
condition holding in all forty-eight. Forty-eight of forty-eight completed.

**Expected:** an interpretive frame to travel with the number it produces.

**Why it stands:** the two readings differ by a factor approaching 1.4 in the
denominator of the most quotable figure this project has produced. A reader
given the larger number without the reading has been given a number they cannot
check, and the smaller number is the one that survives every reading.

---

## D-V30A-36 — the identity control criterion needs no labels, and no identity control exists to run it against

**True, and the two halves matter separately.**

**It needs no labels.** The criterion is one sentence: silent under the identity
control on both sides. The control it names replaces the unavailable cells with
an exact copy of themselves, so any difference in the output is a measurement
artifact rather than a detection. What is scored is whether the detector emitted
anything at all — a property of its own output, compared against nothing. The
routing clause adds one further way for it to fail: a declared sentinel, an
as-built artefact present identically on every side, which cannot differentiate
the sides, so a detector firing on it has produced a false positive under this
control. That sentinel is enumerated ex ante in the declaration, with its
signature. **Neither route reads the pair-keyed labels the metric family
consumes, and neither reads the declared map.** This criterion is not blocked by
the correspondence gap recorded earlier in this register.

**No identity control exists.** The availability probe's perturbation is written
inline and is unconditionally a change: an in-range offset for integers, a
negation for booleans, a large deterministic addition for everything else. There
is no strategy that writes the cells back unchanged. The strategy vocabulary of
the corruption module carries four names and none of them is identity. The one
place the word appears in the instrument is the column probe's handling of a
shuffle that happens to be the identity permutation, which is recorded as a
control artifact — the detection of a degenerate perturbation, and the opposite
of a control run: it records that a probe did not happen, where a control run
records that one happened and moved nothing.

**What building it would take, stated so the size of the thing is visible.** A
perturbation mode that writes the unavailable cells back unchanged; a run of it
on both sides; a check that the emitted output is empty; and a check against the
declared sentinel's signature. Its cost is the same three builds per side as a
real probe, because the expense is the rebuild rather than the perturbation.

**Why it is worth building rather than dismissing as a tautology.** An identity
perturbation over a deterministic builder is trivially silent in its values — and
that is not what the control tests. It tests the mechanism that writes values
back: an assignment that preserves the values can still alter a column's dtype or
its index, and a difference introduced there would appear in every real probe's
output as a finding that belongs to the harness. The determinism guard compares
two clean builds and does not exercise that path at all.

**Expected:** a criterion that is scoreable to have an instrument.

**Why it stands:** it is recorded before any decision is taken about it. Nothing
is built, nothing is pre-committed and nothing is run on it, because what to do
about it is a scope call and the establishing of the fact is not.

## D-V30A-37 — a correction: the population run's overrun was in the PREDICTED term, not the unpredicted one

**The record says the opposite, and the record is wrong.** The commit carrying
the population run, and the entry above it, both state that the 13.05-hour
elapsed against an eight-hour estimate landed in the capture term — the term the
pre-commitment refused to predict. **It did not.** The measurement is in the run
file that was committed at the time, and it was not read carefully enough before
the claim was written.

| term | predicted | measured | |
|---|---|---|---|
| probe phase | 17,755 s | **41,806 s** | **2.35x over** |
| capture phase | not predicted; ~10,970 s quoted as an order of magnitude | **5,170 s** | the loose figure was **2.1x too high** |

**So the term the model was actually fitted on is the one that overran**, and the
term it declined to predict came in well under the figure quoted beside that
refusal. The pre-commitment's caution was pointed at the wrong half.

**Per instrument-month the probe phase ran between 0.94x and 4.21x its
prediction**, median 2.59x, worst at es 2025-11. **None exceeded the 10x halt**,
so the halt behaved correctly — but it did so with more margin to spare than the
record implies, and for a different reason than the record gives.

**Why the model under-predicted, established rather than guessed.** It charged
one term: snapshot rows, at 270 s per million, fitted on a single
instrument-month. At **that** instrument-month it is accurate — the population
run reproduced it at **1.04x**, 352.8 s against 340.8 s predicted, with one
build per side fewer. Everywhere else it is low, and the realised coefficient
runs from 646 to 1,137 seconds per million snapshot rows. Trade rows correlate
with the probe cost better than snapshot rows do — 0.814 against 0.727 — and the
instrument-month the coefficient was fitted on carries by far the lowest trade
count of the large instruments, 397,457 against eleven to thirteen million for
the two largest. **The model omitted a term, and it was fitted at the one point
in the population where omitting it costs least.**

**Expected:** a claim about which half of a forecast failed to be checked against
the file that measures it.

**Why it stands:** the error is not in the run, the harness, the pre-commitment
or any published number — every criterion result is unaffected. It is in the
narration of the run, which asserted a favourable property of the forecast that
the data does not support, and which was then relied on. That is exactly the
class of claim this register exists to catch, and it is worse for being
self-congratulatory: the sentence said the discipline had worked at the precise
point where it had not been checked.

**The transferable part.** A one-point cost model does not merely have wide error
bars — **it cannot see which term it omitted**, because at a single point every
term is confounded with every other. The model interpolated its own fitting point
to within four per cent while missing the population by a factor of 2.35. Fitting
at one point and extrapolating is not a weak measurement; it is a measurement
that reports its own weakness in the wrong place.

## D-V30A-38 — criterion 4 is scored across the declared population, and a stated prediction inside its pre-commitment was falsified

**True, and in the order it happened.** A pre-commitment was committed and pushed
before the run, carrying the invocation, the alignment-family count with its
ground, the audit population with the ground it was chosen on, the cost model,
the disposition of a shape change, and four falsifiable expectations. Then the
harness ran once, exit 0, empty stderr, 37,598 seconds. Then its output was
committed exactly as written.

**The result.** Forty-eight instrument-months, ninety-six sides, **every one
silent under the identity control. Criterion 4 is satisfied in all forty-eight**,
with zero moved columns and zero sides in a not-run state.

**The limb beyond the registered text, reported apart and never as the
criterion:** input invariance holds on all ninety-six sides — every checked
column unchanged in value, dtype and index, sixteen columns per side where the
order-book aggregate is present and eleven where it is not.

**The declared sentinel route produced no false positives, trivially, because
nothing moved** — and that is how it is reported rather than as a pass. The
signature is present on every one of the ninety-six sides: the wrapped column and
its five rolling descendants on eighty-eight, five of the six on eight. Present
identically on both sides in every instrument-month, which is what makes it a
sentinel and what the declaration declared ex ante. The enumeration was read from
the declaration and was not extended.

**THE FALSIFIED PREDICTION, AND IT IS MINE.** The pre-commitment predicted **one
distinct dtype signature** across the population for the frames the write-back
touches, on the argument that the control's subject is then the same object
everywhere. **Measured: two.** Forty-two instrument-months in one group; six in
another, and the six are the instrument whose order-book file does not exist, so
its signature carries an absence where the others carry a column list.

**The cause is the part worth recording.** That absence was established two
rounds earlier, named in the population pre-commitment, and reported in the round
that ran the population. The prediction was then written about a signature that
includes that frame, asserting uniformity anyway. **It contradicted a fact
already in this register.**

**What it costs, stated without minimising it.** Nothing in the result. Something
in the argument: the comparability ground for running everything stands on its
own and never rested on uniformity, but the claim that the larger reading "adds
no information" was offered as a reason the choice was cheap to make, and that
claim is false for six of forty-eight. The control's subject is **not** the same
object everywhere — on that instrument the write-back touches one frame rather
than two — and the six ran silent, which is information the smaller reading would
not have produced.

**The cost model, assessed term by term from the measured output rather than
against its total:** control phase predicted 33,863 s and measured 32,195 s
(0.95x); capture expected 5,170 s and measured 5,403 s (1.05x); total estimated
39,032 s and measured 37,598 s (0.96x). Per instrument-month the control ratio
runs 0.51x to 1.19x, median 0.88x, none reaching twice its prediction. The
forty-eight-point model is accurate on both terms and on their sum.

**Expected:** a prediction stated so it can fail, and reported as failed when it
does.

**Why it stands:** the prediction was made falsifiable at the planning layer's
insistence, precisely because it was the kind of claim that gets believed instead
of tested. It was tested and it was wrong. **This is not a gate result and is not
published as one:** one criterion of four, with criterion 3 blocked on the
declared-units gap recorded earlier in this register.

---

## D-V30A-39 — the compatibility branch of the identity control was never exercised by the run, and the synthetic case is what stands behind it

**True.** The pre-commitment settled, from the registration, that a shape or
column-set change under the identity control is a compatibility failure rather
than a finding or a control artifact — the third control owns shape and index and
says every comparison past a shape change is meaningless including one that looks
clean, the head of that section says control failures are never recorded as
findings, and the reason precedence puts compatibility ahead of control artifact.
It is not a pass: no not-run state is displayed in a way mistakable for one, so
the criterion has no answer on such a side.

**No side reached it.** All ninety-six were silent, so the branch is unexercised
by the run.

**It is recorded here so that the branch is not later described as tested by this
run.** What stands behind it is a synthetic case built for the purpose, in which
a write-back appends a row and the builder drops one, and the control returns the
compatibility state with its comparison recorded as void rather than clean. The
distinction matters: a branch demonstrated on a synthetic and never met in
production is in a different evidentiary position from one the production run
exercised, and conflating them is how an untested path acquires a reputation.

**Expected:** a branch's evidence to be named as what it is.

**Why it stands:** the same discipline that separates a control run from a probe
that did not happen. Both look alike in a log and mean opposite things.

## D-V30A-40 — criterion 3 is not scored, not amended, and not computed in any other form

**The author has ruled: do not amend.** Criterion 3 stands documented as
unrunnable as registered. It is not scored, no amendment is opened, and it is not
computed as exploratory analysis beside the gate.

**The ground, recorded so the ruling is legible later.** The criterion scores
findings against a declared map whose cells are keyed one way and a scorer keyed
another, with no declared object crossing between them — the finding recorded
above at `D-V30A-28`, established by reading the declaration's own supply list,
the map's declared cell key, the per-column enumerations, and the labels and
metric definitions of the reference reducer.

**Closing that gap needs a correspondence, and nobody in this project can author
one blind.** Three of the four criteria have by now been scored across the entire
declared population, and the record carries 243,211 findings from one run and a
silent identity control from another. A correspondence written after that is
written by someone who has seen how the detector behaves, which is the objection
the registration's own withholding clause exists to prevent — and the objection
sharpens as the evidence base grows rather than weakening.

**What is preferred to a number, and why.** A gate honestly not satisfied, with
its reason documented and its analysis in the open, is a better artifact than a
gate satisfied on a key authored after the fact. The criterion's absence is
recorded in the acceptance results as data rather than as prose, and no report
here describes the gate as passed.

**No labels producer is built for this registration, now or later.** The
requirement moves to the next registration, where it can be declared before any
detector runs, and it is written down as such in a standalone requirements
document rather than left in this ledger to be found.

**Expected:** a criterion that cannot be scored honestly to be reported as not
scored.

**Why it stands:** the alternative was available, cheap and defensible-sounding,
and it was declined. That is the whole of the record here.

---

## D-V30A-41 — the cross-tool claim is narrowed to what its own artifact supports

**True.** The headline this project is entitled to is narrower than a flat
statement that no external tool separates the acceptance pair, and the narrowing
is measured rather than modest.

**What the final comparison establishes**, for one instrument-month — `zc`
`2025-01`, both sides, 338,159 rows by 87 columns each, hashes recorded:

- **Four comparators were interpretable and none separated the pair.** One fires
  identically on both sides, and constant firing is not detection. One finds no
  duplicated rows on either side and cannot pose its grouping check at all. One
  passes both sides, its gate in its own regime with nothing to flag. One scores
  the corrected side *higher* than the characterized side, which is the opposite
  of a leakage signal.
- **Two rows are covered with exclusion and are never a pass.** One detects by
  varying pipeline order and a built table has no pipeline to reorder. The other
  is applicable in principle and could not run because of a dependency pin **in
  this project's own harness — a limit of the harness, not of the tool**.
- **Every one of the six was first shown to fire on a documented positive and
  stay silent on a documented negative, through the same adapter path the
  measurement used.** Until both limbs held, a tool's result was recorded as
  uninterpretable rather than as a null.

**Why the narrowing is not optional.** The earlier comparison round recorded, in
its own headline, that five of its defects all leaned the same way — toward the
conclusion this project wants — and it forbade citing any form of its five-tool
claim until the controls landed. They landed, and what they support is the
four-and-two shape above for one instrument-month, not a general statement about
external tooling.

**Expected:** a comparative claim to be stated at the strength its artifact
supports, with the scope of that artifact attached.

**Why it stands:** this is the strongest claim the project has, which is exactly
why it is the one most worth checking before it is repeated. The claim as
proposed was flattering, and the artifact behind it carries a prohibition on the
looser form of it. Recording the narrower form is what lets the claim be made at
all.

## D-V30A-42 — an extraction that replaced nothing, and the favourable claim made about it

**True.** A timezone-alignment rule lived inline in the availability probe and,
in a second copy, inline in the population harness. It was extracted into a named
function so that one rule would live in one place, and the round's commit message
said so: three chances to get one timezone rule wrong, in code strangers never
read, now reduced to one.

**That claim was false when it was written, and it stayed false for two rounds.**
The extraction added a third implementation and replaced neither original. The
probe still runs its inline copy. The harness still runs its inline copy. The
extracted function has never executed against the acceptance fixture — a search
of the harness for its name returns zero.

**And the three do not agree.** On an aggregate key that carries a timezone
against decision stamps that do not — which the acceptance fixture contains, in
its trade frame — the two inline copies CONVERT, assuming the aware column is
universal time and the naive stamps are wall-clock in the same zone. The
extracted function REFUSES, on the argument that the conversion is a choice the
data does not license.

**It was found by a guard written for a different purpose.** A check that the
per-column wiring had not moved the whole-frame result called the extracted
function, and the run stopped on its refusal after thirty-five seconds. Nothing
else would have found it: the function's own tests are synthetic, and the case
does not arise in synthetic frames because nobody builds one with a mixed
timezone by accident.

**Which rule is correct is a live question and is not settled here.** The
converting rule produced every number in this project's Phase 1 evidence. The
refusing rule's argument — that no conversion is derivable when exactly one side
carries a zone — is the argument this project would normally accept. They
contradict, both are mine, and reconciling them changes the probe, so it is
reported rather than decided in passing.

**No published number is affected.** The extracted function was never in the path
that produced any recorded result, which is the same fact that let it diverge
unnoticed. The whole-frame result was re-measured against the committed
population run this round and is unchanged on all eight compared terms.

**Expected:** an extraction to replace what it extracted, and a claim that it did
to be checked before it is written.

**Why it stands:** the failure has two halves and the second is the one the
register exists for. The first is ordinary — a refactor left its originals in
place. The second is that a favourable statement about the refactor went into a
commit message unverified, when checking it was one search for the function's
name. That is the asymmetry recorded earlier in this register, recurring in the
round that recorded it.

## D-V30A-43 — the availability model's documented rule is not the rule that runs, and the gap is one whole second wide on the frame it matters for

**True.** `AvailabilityModel`'s docstring states that an aggregate frame's
"declared availability instant is `key + window`". The probe does not compute
that. Its cell selection is `floor(key).isin(picked_seconds)`, which is the
instant `floor(key) + window`. Where a key already sits on a wall-clock second
the two are the same number and the difference cannot be observed.

**On the acceptance fixture's two declared frames, one is each case, and it was
measured rather than reasoned.** `magg.ts_floor` is on a second boundary for
464,199 of 464,199 rows — 100.0000%, no exceptions — so the documented rule and
the running rule are identical there for all five probed columns.
`trades.ts_event` is a raw event stamp and sits off the boundary on 397,408 of
397,457 rows — 99.9877%. For all eleven of its probed columns the documented
instant is LATER than the running instant, never earlier, by a median of
467.83 ms and a maximum of 999.999 ms. The direction is one-sided by
construction and the magnitude spans very nearly the whole window.

**The rule that runs is the correct one, and that is why this is a defect in the
statement rather than in the numbers.** `AVAILABILITY_DECLARATION.md` §3 and
§C.1 declare the trade join's availability instant to be `floor(T) + 1s` — the
instant the wall-clock-second aggregate completes — and the fixture builder
reaches every trade-derived feature through `groupby("ts_floor")` at
`phase5_ml_fixture.py` line 240, with no path from a raw trade cell to a feature
that bypasses it. The declaration, the pipeline and the running code agree on
`floor(ts_event) + 1s`. The docstring is the only artifact that says otherwise.

**No recorded number moves.** The documented rule was never executed; it is
prose. Every Phase 1 figure came from the running rule, which is the declared
one.

**Expected:** a docstring that states the arithmetic the function performs, and
in particular that a declared rule and an implemented rule not be allowed to
differ silently on the one frame in the fixture where the difference is
observable.

**Why it stands:** it was found only because a delta asked whether the
declaration and the frame path compute anything differently, and the honest way
to answer was to measure both rather than to read the docstring and agree with
it. Reading the docstring would have produced the wrong answer — that eleven
columns differ — and reading only the code would have produced the right answer
with no record that the tool tells its users something false. The second half is
the part this register exists for: an unverified favourable statement about
method, in shipped source, checkable in one measurement. That is the same class
as D-V30A-42, recorded in the round immediately before it.

**Not resolved here, and named for the author.** A stranger declaring
`aggregate_frames` with a key that is NOT already floored — which is what
`trades: ts_event` is — reads the docstring, expects `key + window`, and gets an
instant up to a full second earlier. Three readings are open and the choice
between them is a question about the probe's contract, not about prose: floor
such a key, which is what the code does; refuse it as not a wall-clock-second
key, which is what the word "aggregate" implies; or honour the documented
`key + window`, which is what the docstring says.

## D-V30A-44 — the probe's notes reached nobody, and two commit messages said otherwise

**True.** `AuditResult.explain()` rendered the unprobed frames, the probe's
domain paragraph and the check tally. It never rendered `source.notes`. Every
note the availability probe wrote about a run was therefore invisible to every
person running the command, and visible only to a caller inspecting the result
object in a library session.

**What was in those notes.** The flooring report added the round before — that a
declared aggregate key is not on second boundaries, with the measured fraction,
and that the run floored it. The per-column-modes fallback conflict — which
columns of a selected frame took the frame rule because no per-column mode was
declared for them. That a declared aggregate frame was absent from the supplied
frames and so nothing in it was corrupted. That a column's declared instants fall
in no selected second, so its silence is `none` and not `observed_silence`. Each
of those exists because a reader has to know it.

**Two favourable claims about the work are falsified by this.** The R205 commit
message said the conflict is named "in the run's own output, so the choice is
where a reader meets it rather than in a document they will not open." It was in
no output a reader meets. The R207 commit message said flooring is now reported
"in its own output"; the round's own delta had made shipping that flooring
silently a halt, and it shipped silently by a different route than the one being
guarded. Both claims were checkable by running the command once.

**It was found by walking the stranger path, not by a test.** The suite covered
that the notes are PRODUCED and asserted on `res.notes` directly. Nothing
asserted that any of them is rendered. A test written against the same mental
model as the code shares its blind spot, and the walk did not share it because
the walk only sees what is printed.

**Fixed, and the fix is covered.** `AuditResult.notes` reads through to the
source by reference, keeping the view-not-cache property, and `explain()` renders
them under `ABOUT THIS RUN:`. The unprobed-frames fact is dropped from that
section because it is already rendered from the structured field, and a first
attempt at that de-duplication compared strings that differ between the two
wordings and silently kept both. `tests/phase1/test_notes_reach_the_user.py`
asserts the flooring report is in the RENDERED text for a key that needs it,
absent for one that does not, that the unprobed fact appears exactly once, and
that the notes are not cached.

**Expected:** that a report added to satisfy a requirement be checked in the
place the requirement names, which was the tool's output and not a field on an
object.

**Why it stands:** it is the fourth instance of a detection that exists and does
not arrive, and the first that arrived nowhere at all. The earlier three surfaced
as library exceptions nobody reads as detections. This one was written, tested,
committed and described in two commit messages as reaching the reader, while
reaching no reader. The asymmetry recorded in this register — that unfavourable
claims get verified and favourable ones get asserted — recurs here for the third
consecutive round, in the round whose own delta had made the omission a halt.

## D-V30A-45 — the fix for the traceback item added two frames to a traceback

**True.** Item 6 of the definition-of-done walk was that a build function
returning the wrong type crashed inside `determinism.py` or `checks.py` with an
`AttributeError` naming a module the user has never opened. The fix wraps the
user's callable at the boundary in a guard that checks the return type and
raises a message naming what arrived and the route out.

**The wrap was applied twice.** The CLI wraps the loaded callable, and
`contract.audit` wraps again. Both are correct in isolation: the CLI guards the
availability and check paths, and `audit` guards library callers who never touch
the CLI. Together they nested.

**And the cost landed on the one case the fix was careful to preserve.** A user's
own pipeline raising keeps its traceback, because that traceback points at their
file and is the right answer. Double-wrapping put `contract.py, in checked`
into that stack twice — two frames of this tool's plumbing inserted into a
traceback whose entire value is that it points somewhere else. The user's
traceback went from 13 lines to 22.

**It was found by re-running the wrong turn, which is the only thing that would
have found it.** The suite was green. The three fixed cases all returned one
clean line. Nothing about the guard's own behaviour was wrong. The defect was
visible only in the stack of a case that is *supposed* to fail, and only by
looking at that stack rather than at its last line.

**Fixed.** The guard is idempotent — it stamps the wrapper and returns an already
guarded callable unchanged — with a test asserting `guarded_build(guarded_build(f))
is guarded_build(f)`, and a second asserting the user's own exception still
passes through.

**Expected:** that a fix be checked against the case it was written to preserve,
not only against the cases it was written to change.

**Why it stands:** the round's instruction was that every fix has its test
already written — re-run the exact wrong turn that found the friction. This is
what that instruction is for, and it earned itself on its first use by catching
a regression introduced by the fix it was checking. The three items it was
verifying all passed; the defect was in the fourth thing, the one being held
constant.

## D-V30A-46 — a criterion for pre-commit catches, and the entry that was missing under it

**True.** Two defects of one category were found in consecutive rounds: a fix's
own acceptance test finding a defect inside that fix, before commit. The
double-wrap received an entry, D-V30A-45. The generic marker received none — a
commit message and a paragraph in the walk document.

**Two instances of one category, one disclosed and one not, on no stated
criterion.** That asymmetry is how a register begins to mislead with nobody
having decided on it: a reader counting entries of a category counts one, and the
category has two.

**The criterion, stated now so the asymmetry has something to be resolved
against.** This register's scope is disclosures of fact about the tagged state. A
defect found and fixed before commit is not such a fact, and the default is
therefore that it does NOT get an entry. It gets one when either limb holds:

  (i) a claim was made about the work — in a commit message, a report, or a
      document — that the defect makes false; or
  (ii) the defect is of a class this register already carries, so that omitting
      it would understate a count a reader could take from the register.

**D-V30A-45 qualifies under both.** Its round's commit message described the
guard as fixed while it double-wrapped, and it is an instance of the class
D-V30A-42, -43 and -44 record.

**The generic marker qualifies under (ii), and it has no entry.** It is the
discarded-parameter defect — the class this register carries at D-V30A-21 and in
the five refusals of `contract.py` — appearing inside the fix written to close a
different defect. Under the criterion above it is a disclosure, and its absence
was the asymmetry.

**So it is recorded here rather than left in a commit message.** The marker
`__leakaudit_guarded__` meant "some guard is applied". A second guard, added later
for a different job, would have found the flag set, declined to apply, and left
its own check unperformed with nothing said. It was found by constructing the
two-guard case that R211 §1.2 required rather than by any test then existing, and
it is now keyed on the job — `GUARD_BUILD_RETURN`, carried in a set — with four
tests asserting both guards apply in either order, each stays idempotent in the
other's presence, and both actually fire.

**Expected:** that two members of one category are both disclosed or both not,
under a criterion stated somewhere, rather than each judged on how notable it
felt in the round that found it.

**Why it stands:** the criterion did not exist until now, so neither decision was
wrong when it was made; what was wrong was that no rule existed to make them
consistent. The register is append-only, so the earlier omission is repaired by
adding this entry rather than by editing D-V30A-45 or the walk document, and both
of those stay exactly as written.

**Carried consequence:** the criterion above is not registered vocabulary and
binds nothing. It is this register's own working rule for its own scope, and a
later round may replace it — in which case the replacement states what happens to
entries admitted under this one.

## D-V30A-47 — `ties_available` is a config key the loader validates and the probe never reads

**True.** `AvailabilityModel.available()` implements the locked comparator —
`a <= d` when `ties_available`, `a < d` otherwise. **A search of the whole
repository returns no caller.** The probe selects cells by
`floor(key).isin(picked_seconds)` and attributes movement by comparing a row's
floored decision second against the corrupted second; the tie question is
answered implicitly by that construction and the comparator is never invoked.

**Measured, not inferred, and on the input built to separate the branches.** With
decision stamps 200 ms inside each second — the shape the B-6 controls use — the
two settings give identical verdict, finding count, in-second and next-second
totals. With decision stamps **exactly on the second**, which is the only input on
which `a <= d` and `a < d` can differ, they are identical again. 25 findings, 25
in-second, 0 next-second, under both.

**The implicit behaviour matches the locked DEFAULT, and this was checked rather
than assumed.** A cell of second F becomes knowable at F+1s. A row stamped exactly
at F+1s floors to F+1 and is counted as next-second — legal, available — which is
`a <= d`, the branch `PREREG.md` §2.3 locks and §0.3 Claim A argues for. **So no
published figure was computed under the wrong rule**, and the status of the
reported Phase 1 results does not change.

**What does change is what a user's file can do.** `ties_available: false` is
accepted by the loader, type-checked, refused if non-boolean, documented in
`leakaudit schema` as *"whether a value whose instant equals the decision instant
counts as available"* — and has no effect. A user who declares the non-default
branch gets the default branch and no error, which is a silence about a
declaration, from a tool whose product is the difference between kinds of
silence.

**Expected:** that a key the loader validates reaches something that consumes it,
or is refused as unwired. The `_UNWIRED` registry was built for exactly this
shape and five parameters were routed through it; this key was not among them.

**Why it stands:** it is the class this project has put on its own halt list in
every recent round — a config key the loader reads and ignores — found in the
package that defines the class. It was found by asking a different question: an
audit of whether a known positive discriminates between the instrument built and
a plausible wrong one. The wrong instrument considered was one using the other
tie branch, and establishing that the controls could not tell them apart required
finding out whether the branch was reachable at all. It is not.

**Not repaired this round, and the reason is scope rather than difficulty.**
Wiring the comparator changes what the probe computes on the equal case, which is
a change to the availability probe's execution path — `availability.py` — and the
standing rule then requires the whole-frame fixture guard before the round is
reported done. The equal case is known to occur in the scored population: the
harness's own note records two cells, es 2025-10 and es 2025-11 corrected,
carrying 0 strict and 1 equal. Making the key live is therefore a measured change
with a guard attached, not a one-line fix, and it is reported rather than
attempted at the end of a round.

## D-V30A-48 — the round-reconciliation check scans a dead session's scratchpad and is blind to the live one

**True.** `check_round_reconciliation` implements D10 — every working-directory
file is in the repository or declared ephemeral. Its population is `_WORK_ROOT`,
a **hardcoded absolute path** to one session's scratchpad directory. That path
names a session that ended: it holds 679 files and nothing has written to it
since 26 August 2026. The session doing the work carries 11,985 files in a
different directory, and 149 such directories exist beside it.

**So the check's coverage of the current round's working files is zero**, and
every finding it can emit comes from a directory nobody is working in.

**It was found by asking a different question.** The gate emitted two findings
where one was expected. The second was `round_reconciliation` naming
`DEFERRED_ITEMS.md`: a stale copy in that dead scratchpad, byte-identical to the
version committed at HEAD until an append to the repository's copy left it
matching nothing. Verified against git and removed. Asking whether that scan was
deliberate is what exposed the path.

**What the check still does, stated so this is not read as "it does nothing".**
It compares digests against the repository and the manifest correctly, and its
ephemeral classification works. Pointed at a live working directory it would do
its job. It is aimed wrongly, not built wrongly.

**Expected:** that a check whose stated population is "the working directory"
resolves that directory at run time, or names the one it means and refuses when
that directory is absent or stale.

**Why it stands:** it is the same shape as D-V30A-29 — an instrument that had
never measured the thing it names — and the same shape as the `F2_DIR` defect
recorded in `INSTALL.md`, where a hardcoded absolute path into one machine's
session scratchpad meant four tests could run on exactly one computer. That one
was repaired; this one is its sibling in a registered instrument, and it survived
because a check that emits janitorial findings trains its reader to expect
janitorial findings.

**And that is the second-order cost, which is the part worth keeping.** A check
earns attention in proportion to the fraction of its findings that require
thought. This one has been spending that credit on a dead directory, and the gate
prints its output beside `hash_set_single_source` — disclosed, measured, pinned,
and substantive — in the same format, as one line of "N findings".

**Not repaired this round, and the reason is that the instrument is registered.**
`tools/check_registration.py` is one of the paths the `prereg-v30a` tag message
enumerates. It is revisable, so the repair is permitted — but changing a gate
instrument alters what the delta-of-findings comparison against the frozen
checker produces, which is a measured act with its own before-and-after, not an
edit to make at the end of a round. Reported with its population measured so the
repair starts from a number rather than from a suspicion.

## D-V30A-49 — `column_modes` never reached the probe from the command line

**True.** The version 3 key `column_modes` is parsed, validated with four
distinct refusals, stored on the loaded config, and documented at length by
`leakaudit schema` — the five modes a file may declare, the sixth reachable only
from the library, and the statement that a column with no mode is reported
undeclared rather than defaulted. **The CLI's call to `run_probe_a` omitted it.**

**So a user who declared per-column modes silently got the whole-frame path**,
with no error and nothing in the output to say so.

**That is not a missing capability, it is a wrong answer.** The two paths give
DIFFERENT results on the same data: measured at R205 as 25 cohorts with a finding
under the whole-frame rule against 0 under the per-column rule, on a frame whose
column was published half an hour before the row carrying it. The per-column path
was built specifically to suppress a false positive the coarse path produces — so
a user declaring modes **to correct a false positive kept the false positive**.

**Measured, not inferred.** The same pipeline was run through the installed
command with and without a `column_modes` block: identical findings, and the
per-column fallback note — which `run_probe_a` emits whenever `column_modes` is
non-empty — absent in both. Its absence was the symptom.

**Repaired in the round it was found, and the exception is stated.** The standing
rule is that a sweep finding is disclosed and not repaired in the same round
where it touches a registered instrument. `cli.py` is not registered and not on
the availability probe's execution path, the fix is one argument, and its
observable is a test asserting the fallback note now appears through the CLI.

**Expected:** that a key with four refusals behind it reaches the thing the
refusals exist to protect.

**Why it stands:** it is the same class as D-V30A-47, found in the same sweep,
and it is the more consequential of the two — the tie branch changes one row's
classification, this one silently selects a different probe path. Both were
invisible to the whole suite, for the reason recorded as TB-20: a defect that
makes a thing do nothing is invisible to tests of that thing.

## D-V30A-50 — `timestamp_column` is stored and reaches nothing

**True.** The version 3 key `timestamp_column` is accepted by the loader,
carried on `LoadedConfig`, and documented by `leakaudit schema` as *"the frame's
clock column. Default 'timestamp'."* The only reader anywhere is a test asserting
the loader stored it. The CLI never mentions it, and the probe uses each
aggregate frame's own declared KEY as the clock for the modes that need one.

**NOT wired, and that is a decision rather than a deferral.** The probe already
has a clock for each frame — the key the user declared in `aggregate_frames` —
and introducing a second one would create two answers to "which column is this
frame's clock" with nothing to arbitrate between them. Wiring it would be adding
a capability, not completing one, and there is no user asking for it.

**So the schema surface now says it is inert**, which is the other honest option
and the one this round took. Removing the key was rejected: a file that sets it
would then be refused for an unknown key, which turns a harmless declaration into
a breakage.

**Expected:** that a documented key either reaches a consumer or says it does
not, where the user reads it.

**Why it stands:** it is the third hit of the same sweep and the one where the
right answer was documentation rather than code. It is recorded because "we
looked and this one was fine to leave" is only worth anything if the looking is
written down — and because the standing test added this round will fail if
anyone adds a key without deciding which of the two it is.

**Carried consequence:** the check that enforces this reads `SCHEMA_DOC` for the
words that mark inertness. A future author who documents inertness in different
words gets a failing test rather than a silent gap, which is the intended
direction, and the word list is in the test rather than in the schema so that
widening it is a deliberate act.

## D-V30A-51 — the installability checker read an English sentence as an import statement

**True.** `check_installability` extracted imports with a line-matching pattern
over raw source text — any line beginning `from ` or `import `. It could not tell
code from prose. A docstring sentence explaining the identity control's known
positive — *"it is what someone implementing / from the registered sentence alone
would most likely build"* — was reported as importing a module named `the`,
neither stdlib nor shipped nor declared.

**The instrument was defeated by the text written to explain the instrument.**
That is not a coincidence: a heuristic that reads English as code gets defeated
disproportionately often by prose about parsing, imports and dependencies, which
is exactly the prose a checker's own documentation contains.

**Two rules point opposite ways here and it matters which governs.** *Fix the
world, not the instrument* is about not weakening an instrument so a TRUE finding
goes away; this finding was false, so it does not govern. *Never adjust content
toward an instrument* does govern — and the first repair taken was the wrong one:
the sentence was reworded so the pattern stopped choking. That left the parser
wrong and the next such sentence undefended, and it is corrected here. **The prose
is restored and the parser is replaced.**

**R163 §1's exemption test, stated because this is an instrument change.** *Would
this change have been made if the triggering content did not exist?* **Yes.** A
parser that reads an English sentence as an import statement is defective
whatever text happens to expose it. Defect repair, ruled, disclosed.

**The repair is a real parse, not a narrower pattern.** `ast` has no blind spot
here: a docstring is a string constant and simply is not an import node, so there
is nothing left to exempt. A tightened regex would be a heuristic with a smaller
blind spot, and it would have been labelled as one if it were what shipped.

**THIS PROJECT HAD ALREADY LEARNED THIS, ONCE, AND IN THESE WORDS.**
`TRACKB_LESSONS.md` TB-02 records the citation check moving from text matching to
parsing, with the reason: *"a docstring is a string constant, so it simply is not
a reference, and there is nothing to exempt."* The lesson was applied to one
checker and not to its neighbour. That is TB-21's shape — knowledge placed where
it governs one thing — recurring in the same file that records TB-21.

**The delta of findings, measured over the same tree with only the reader
changed:** one finding removed, zero added. The removed one is the false positive
above. Relative imports are skipped exactly as the superseded pattern skipped them
— a leading dot is not an identifier, so it never matched them — so this is not a
widening.

**And the repair is tested in BOTH directions**, because the plausible wrong
repair is a parser tightened until it stops seeing. Two assertions: the prose is
no longer flagged, AND a real import beside it in the same file is still caught —
including lazy imports inside functions, conditional imports, aliased imports and
dotted ones. A file that does not parse is now a finding rather than a silence —
the previous form read unparseable text happily and reported whatever it hit.

**Expected:** that a checker deciding what a module imports reads the module,
rather than matching lines that resemble imports.

## D-V30A-52 — `timestamp_column` is refused rather than accepted and ignored

**True.** The version-3 key `timestamp_column` was accepted, type-checked, stored
on the loaded config and documented — and reached nothing. Each aggregate frame's
clock is the key named for it in `aggregate_frames`, bound from the model, and
the per-column mode path passes that key. The config value was independent of it
and had no effect.

**Recorded at D-V30A-50 as inert-and-documented. That was the weaker of the two
honest options and this supersedes it.** Documenting a key as doing nothing still
leaves a user who sets it having declared something that changes nothing — the
declaration is accepted and silently has no consequence, which is P0's shape in a
quieter register.

**Refused, not wired, and the reason is arbitration.** Wiring it would give the
probe two clocks per frame — the frame's declared key and this — with nothing to
choose between them when they disagree. A second answer to a settled question is
worse than no answer.

**The key stays in the version-3 key set deliberately**, so the refusal can name
what to use instead. Dropping it would produce the generic unknown-key refusal,
which tells the user their key is unwelcome and not where the capability lives.

**Expected:** that a key the loader validates either reaches a consumer or is
refused. "Accepted, stored, documented, and inert" is a third state that reads to
a user exactly like the first.

**Why it stands:** the guard that holds this now recognises three legal states —
read, declared-unconsumed, declared-refused — and accepted-and-ignored is the one
that is not. `timestamp_column` was the case that forced the third state to be
named, and the guard would have passed it as merely unconsumed without it.

## D-V30A-53 — the per-column corruption path read the frame's mask and wrote the column's

**True.** In `availability.py`'s integer branch, `vals` was read with the
FRAME-level mask while the offset array `off` was sized from `cell_mask` and the
write targeted `cell_mask`. Where the two masks differ the branch raised a numpy
broadcast error — measured, shapes `(20,)` against `(22,)`. A partial conversion
left from R205, when the per-column path was added and the frame-level path
became its special case.

**THE BLAST RADIUS, MEASURED RATHER THAN ARGUED.** R225 §1: *plausibly is not
measured*, and `ties_available` set the form — the defect is reported together
with a checked statement about which published figures move.

*Which paths reach the broken branch.* Two conditions, both required. First,
`cell_mask` differs from `mask`, which happens only when a per-column mode is
declared for that column: `cell_mask = mask` is the initialisation, and the only
reassignment is inside `if spec is not None`, where `spec` comes from
`column_modes`. Second, the column's dtype is integer; the float and bool
branches never read `mask`.

*Whether any Phase 1 population could have entered one.* **No, and by
construction rather than by argument: the code did not exist.** `git log -S`
over `src/leakaudit/availability.py` names commit `1d949f9` as the first
introducing BOTH `column_modes` and `cell_mask`; there is no earlier commit
touching either string. `1d949f9` is the 124th commit of 147. The three Phase 1
acceptance artifacts were committed before it — `void_b065264/acceptance_run.json`
at the 104th, `criteria_12_run.json` at the 107th, `criteria_12_population.json`
at the 110th — and `git merge-base --is-ancestor 1d949f9 <each>` reports that the
per-column commit is NOT an ancestor of any of them. Checked directly at the
acceptance commit as well: `git show 6b242b3:src/leakaudit/availability.py`
contains the string `cell_mask` zero times. Every Phase 1 figure was produced by
a build in which one mask existed.

*And after the branch existed.* Reach still requires an explicit `column_modes=`
argument. Of the 23 call sites of `run_probe_a` in the repository, three pass one:
`cli.py` and two cases in `test_modes_wiring.py`. Neither Phase 1 harness —
`harness_criteria_12.py`, `harness_criteria_12_population.py` — passes it, and
`column_modes` is not a field of `AvailabilityModel`, so there is no route to it
that does not go through that keyword.

**THE CRASH IS THE LOUD HALF AND IT IS NOT THE WHOLE DEFECT.** The two masks
raise only where their SUMS differ. Where they select different cells in equal
number, `new` would be computed from the frame-mask cells and written to the
cell-mask cells — no exception, and a perturbation applied to cells whose
original values it did not read. That is the silent form, it was never observed,
and it is recorded here because "it crashed" would understate what the line could
do.

**R163 §1's exemption test, because this was found while doing something else** —
the `at_bar_close` path became reachable for the first time when
`bar_duration_seconds` was wired at R224, and the branch raised on the first run
that entered it. *Would this change have been made if the triggering work did not
exist?* **Yes.** A line reading one mask and writing another is wrong whatever
happened to expose it, and the repair is the one-word substitution the surrounding
comments already described. Defect repair, ruled, disclosed.

**Expected:** that a converted branch is converted throughout, and that the
positive exercising a branch actually enters it. R215 §0's refinement — a positive
every plausible wrong instrument fires on tests wiring, not validity — has its
third instance here, and its first in production code: R205's discriminating
positive used a FLOAT column, so it never reached the integer branch at all.

## D-V30A-54 — the inferred bar duration was taken in row order, and reported as one number

**Two defects, and only the first is what it looked like.**

**Finding A — the inference ran in row order.** `bar_duration` computed
`ts.shift(-1) - ts` over the frame as given. On a timestamp column that is not
sorted the differences run backwards, and the first live run against such a frame
reported `INFERRED VALUE: -1 days +23:59:59.725` — a negative bar duration, a bar
closing before it opens. `PREREG.md` line 255 says *inferred from SUCCESSIVE
timestamps*, and successive is an order on instants rather than on rows, so the
stamps are put in time order before differencing and the note says when that
reordering happened.

**Finding B — and a sort does not touch it.** The negative value was caught
because it was absurd. Had the column been mostly ordered with a few inversions,
or simply had irregular gaps, the same code would have produced a plausible wrong
number and nothing would have caught it — no reader, no test, no note. The
dangerous case is the near-miss that reads fine.

**AN IMPOSSIBLE DURATION IS NO LONGER EMITTED AS A VALUE.** A non-positive
successive difference raises, naming how many of how many and what to do instead.
Ordering makes a negative gap unreachable, so what this catches now is ZERO —
duplicate timestamps — and a zero bar duration is not a small one: it collapses
`at_bar_close` into `at_timestamp` silently, which is the mode returning the
answer of the mode it exists to be told apart from. The check is written against
`<= 0` so it still holds if the ordering is ever removed.

**AND THE VALUE THAT IS REPORTED CARRIES ITS FRAME.** The first form of the note
printed `_d.iloc[0]` under the label `INFERRED VALUE`. That is a point estimate
over a per-row series: right on a frame with regular bars, and on a frame without
one a single number standing for a set with no centre. The record now carries how
many successive differences there were, how many distinct values they took, and
their smallest, largest and median — and the note names a duration ONLY where all
the differences agree.

**WHERE THEY DISAGREE, NOTHING IS NAMED, AND THAT IS THE REFUSAL.** The note says
there is no single bar duration for the frame, gives the spread, and says what
disagreement means: either bars are missing — a gap of two bars read as a bar
twice as long, which puts that cell's availability later than it truly was — or
the column is not bar-shaped and `at_bar_close` is the wrong mode.

**THE ARITHMETIC IS NOT CHANGED, AND THAT IS DELIBERATE.** Collapsing the per-row
gaps to one inferred unit would be a better answer on a frame with missing bars,
and it is not the registered one: three documents say *the gap to the next
timestamp*, per row — `PREREG.md` line 255, `DESIGN.md` §2.1, and
`AVAILABILITY_MODES.md`'s `at_bar_close`. Refusing the route outright would narrow
a grant the registration makes, which is `ties_available`'s defect inverted. So
the refusal is of the CLAIM rather than of the route: the run declines to state a
bar duration the frame does not have, and computes what it was registered to
compute.

**Measured live, through the command line, on five frames**: regular stamps name
`1s` as well founded over 39 differences; the same stamps shuffled name the same
`1s` and say the column was not in time order; a frame with bars missing names no
value and reports 26 differences taking 2 distinct values from `1s` to `2s`;
duplicate stamps are refused with exit 2; a declared duration produces no
inference note at all.

**Expected:** that a quantity the tool could not resolve is reported as
unresolved rather than as a number, and that a number reported as a property of a
frame is one the frame has.

## D-V30A-55 — the two most-quoted figures in this project named no invocation

**True, and for many rounds.** Two counts are reported every round as evidence.
Neither carried the command that produced it, and both are ambiguous without one.

- **The suite line.** `python -m pytest tests/phase1` reports 598 passed and no
  failure. `python -m pytest tests` reports 756 passed and the known one. Both
  were true of the same tree on the same day. Every suite line handed over named
  neither target.
- **The gate line.** `python tools/check_registration.py --stage prereg` prints a
  different result depending on whether `LEAKAUDIT_WORK_ROOT` is set, because
  unset the working-directory check reconciles nothing. Every gate figure before
  R225 was the unset one, and the note saying its coverage was zero was not
  carried alongside the count.

**Neither number was wrong. Both were figures without their populations** — and
the rule against exactly that has been in force since R178 and enforced on the
tool's own output throughout. The project's own evidence was the place it was not
applied.

**A THIRD INSTANCE, FOUND WHILE FIXING THE FIRST TWO, and it is worse than
either.** Mid-session the shell's `PATH` reordered and bare `python` resolved to
CPython 3.11.9, which on this machine has no numpy. Every figure reported earlier
in the same session was produced by CPython 3.12.10 with numpy 2.4.2 and pandas
3.0.1 — and named no interpreter, so nothing in the record distinguished them.
The environment varied WITHIN one session and the reports could not say so.

**The repair is a durable rule, not a habit.** `OPERATING_RULES.md` §2 now
carries: a count reported as evidence carries the invocation that produced it —
the command, not a description of it. Suite lines, gate lines, manifest counts,
guard terms.

**And the user-facing statements are restated.** `README.md`'s verification
section now lists four invocations rather than two, says why the two gate rows
print the same headline for different reasons, and names the interpreter and
dependency versions. `INSTALL.md`'s environment table had a column headed "suite"
with no command; it names the command now.

**Expected:** that a count offered as evidence can be reproduced by the reader,
which requires knowing what was run.

## D-V30A-56 — `check_label_under_another_name` is named more broadly than it tests

**True, and it is a false statement in the user-facing surface.** The check
screens each feature against the declared label at Pearson `|r| >= 0.999`. Its
name says it finds the label under another name. A user who sees it report
nothing concludes their features contain no relabelled copy of the target.

**Measured, and the measurement is what makes this a name problem rather than a
threshold problem.** `y**3` is a *perfect* copy of a label — invertible, rank
order preserved, no information lost — and it screens at `|r| = 0.762`. It passes
at 0.999, at 0.99, at 0.95, at 0.90 and at 0.80. **No cutoff catches it**, because
Pearson measures linear agreement and a leak need not be linear. The full case
table is `evidence/session/LABEL_SCREEN_CASES.md`.

**So the parameter that was filed as the defect was the wrong dial.** The entry
was raised as a threshold the user could not see; the naming half of that closed
at R224, and the cases then showed that settability was not the open question at
all. That is recorded rather than quietly re-filed, because a candidate whose
reason changes underneath it is a candidate nobody has re-read.

**The silence stops overstating itself, ahead of the naming decision.**
`CheckResult` carries a `silence_is_about` scope, set only where a check's name
is broader than its test, and the found-nothing sentence prints it. The
accurately-named checks carry none, and a test holds that as the discriminating
negative — a scope line on every check would be decoration rather than a
statement about a specific known gap.

**What has NOT been decided, and it is deliberately left open:** whether the
check is renamed to what it does or extended to do what it says. Both costs are
reported and the choice is the author's.

**Expected:** that a check's name is a true statement about its behaviour,
because the name is the frame in which a user reads its silence.

## D-V30A-57 — `python` was recorded as the invocation, and it resolved to two different interpreters

**True, and it is R226 §0's own rule failing inside the round that adopted it.**
That rule said a count reported as evidence carries the command that produced it.
`python -m pytest tests` is not a command in the sense the rule needs: it is a
**name**, and on this machine it resolved to CPython 3.12.10 and later to 3.11.9,
in one session, with nothing announcing the change.

**The cause, established from the registry rather than inferred.** The Windows
uninstall registry records a per-component install date, and the component is
named: `Python 3.11.9 Add to Path (64-bit)`, `InstallDate = 20260903`. That
component prepends its directories to the user `PATH`, and the `PATH` read back
from `HKCU:\Environment` shows exactly that ordering, with `Python311` ahead of
`Python312`. A shell started before that write keeps the old order; one started
after does not. Both existed in the same session.

**The exposure is bounded and the suite half of it is empty, by measurement.**
Base 3.11's `site-packages` holds only the pip/setuptools bootstrap, every entry
stamped within seven seconds of the installer finishing on 3 September, with no
later mtime — so no third-party package was ever installed there and none was
removed. `…\Python311\python.exe -m pytest tests` reports `No module named
pytest` and produces no number. A shell resolving `python` to 3.11 does not fall
back to 3.12; it fails. So every suite figure that exists came from a shell whose
`PATH` predated the change. 3.13.1 is excluded by the ordering, which places it
after both.

**The gate half is non-empty and was compared rather than argued about.**
`check_registration.py` imports nothing third-party and runs under 3.11, so a
gate figure from that window is ambiguous as to its interpreter. The full stage
output — 112 lines, same work root — is **byte-for-byte identical** under 3.11.9
and 3.12.10. The manifest regenerator gives the same digest under both. Measured
for two interpreters at one commit, which is the bound on the claim.

**THE REPAIR IS IN THE INSTRUMENT, NOT IN THE OPERATOR'S HABIT**, because the pin
that failed was the habitual one. `check_registration.py` now prints its own
interpreter version, architecture and executable path on the second line of every
run, so a figure copied out of it carries that version whether or not whoever ran
it wrote it down. `OPERATING_RULES.md` §2 carries the rule's second half: the
recorded invocation uses the version-selecting launcher and the report carries
the resolved version. `README.md` and `INSTALL.md` are restated in that form,
with a line saying what to substitute if only one Python is installed.

**Expected:** that an invocation recorded as evidence resolves to the same thing
when a reader runs it, which a bare interpreter name does not guarantee.

**And the layer lesson is recorded separately** at `TRACKB_LESSONS.md` TB-22,
because this is the second instance of one mechanism: the 3.11 install was ruled
safe on side-by-side installation and reversibility, which are claims about files
on disk, while what changed was name resolution — the same shape as R220, where
`.gitattributes`' guarantee about git storage was read as a guarantee about a
Python edit performed above it.

## D-V30A-58 — a repository tool acquired a 3.12-only dependency an hour after the 3.11 floor was measured

**True, and found by rebuilding a measurement rather than annotating it.**

`tools/probe_path_guard.py`'s `watch()` calls `record_modules()`, which uses
`sys.monitoring` — Python 3.12 and later. The project declares
`requires-python = ">=3.11"`, and on CPython 3.11.9 the three `test_watch_*`
tests in `tests/phase1/test_probe_path_guard.py` fail with
`AttributeError: module 'sys' has no attribute 'monitoring'`.

**Measured at the corner of the declared dependency space**, rebuilt for this
purpose and kept: CPython 3.11.9 with `numpy==1.26.4`, `pandas==2.1.4`,
`pyarrow==14.0.2` pinned exactly. `<venv>\Scripts\python.exe -m pytest tests`
reports **763 collected, 755 passed, 4 failed, 4 skipped**. The published row for
that corner says **632 passed, 4 deferred, 1 known failure**.

**WHEN IT BROKE, ESTABLISHED FROM THE TREE.** At `a023011` (3 September 13:23),
the commit whose message is *"The corner of the declared space is measured"*, the
guard test file already existed with all three tests, and
`tools/probe_path_guard.py` already contained `sys.monitoring` — including the
line `raise RuntimeError("sys.monitoring is unavailable; this needs 3.12+")`. But
`watch()` used `sys.setprofile`, which works on 3.11, so those tests passed and
the row was correct when written.

At `7cfa037` (3 September 14:26) — *"a profiler I had left inside the guard"* —
`watch()` was rewired onto `record_modules()`. **Sixty-three minutes after the
corner was measured, and nothing re-measured the corner afterwards.**

**The 3.12-only requirement was already written down in the same file.** The
`RuntimeError` above was there when the caller was wired onto it. What was missing
was not knowledge of the constraint but any question about what it did to a floor
declared in a different file — TB-22's shape again, a guarantee at one layer and
a change at another.

**THE BOUND, so this is not read as larger than it is.** `pyproject.toml` declares
`packages = ["leakaudit", "protocol"]`, so `tools/` is **not distributed**.
`requires-python = ">=3.11"` is **not falsified**: at the corner the package
imports, 755 tests pass, and the non-fixture pipeline produces a body byte-
identical to the development environment's — sha256
`ddb133ff2fc959f0efb24124ca4d0f9dfc70f528cd5e1892136436c8dc34d9f1` under both.
What is false is the published suite figure for that row, and what is broken is a
repository instrument on the interpreter the project declares as its floor.

**Not repaired here.** R228 §0's branch for a measurement that does not reproduce
is to report what differs before touching any number, and the repair — a version
gate, a `setprofile` fallback, or a narrowed floor — is a decision about the
declared floor rather than a defect fix.

**Not swept.** Whether any other repository tool has acquired a 3.12-only
dependency the same way is unexamined, not confirmed clean.

**Expected:** that wiring a caller onto a recorder which raises "this needs 3.12+"
prompts the question of what the project's declared floor is.

## D-V30A-59 — "no venv was ever built on 3.11" claimed more than its population

**True, and it is mine, from R227 §1.** The population actually measured was
**surviving `pyvenv.cfg` files**, and a virtualenv deleted with its scratch
directory leaves no config and no trace. The supported statement is the weaker
one: *no surviving `pyvenv.cfg` records a 3.11 environment.*

**And the base-interpreter evidence was cited for something it cannot reach.**
That evidence — 3.11's `site-packages` holding only the installer's pip and
setuptools, every entry stamped within seven seconds of the install — bounds one
thing well: **nothing was installed into base 3.11**. A virtualenv does not
install into base `site-packages`, so it says nothing whatever about the venv
question. Two sound observations were joined into a conclusion neither supports.

**AND THE STRONGER CORRECTION IS THAT A SURVIVING ARTIFACT DOES RECORD IT.**
`<scratch>\dod_work\py311_out.txt`, timestamped 3 September 13:15 — two minutes
after the 3.11 installer finished — carries the banner:

    # python  3.11.9
    # numpy   1.26.4
    # pandas  2.1.4
    # pyarrow 14.0.2

That is the corner environment, recorded by the run itself. **The search
population was wrong, not merely narrow**: it looked for the environment's
configuration and not for what the environment produced, and the second survived
while the first did not.

**Expected:** that an absence claim names the population it searched, and that the
population is chosen to be one where the thing sought would appear.

**Why it is recorded at this weight.** It is a small sentence, and it is exactly
the kind that gets quoted later as settled. The correction costs one entry now;
the alternative is a false premise circulating with a disclosure number behind it.
