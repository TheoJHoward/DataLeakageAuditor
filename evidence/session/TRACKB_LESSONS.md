# Track B lessons

The review register in `HISTORY.md` closed at lesson 45 and is not reopened per
round. Track B's lessons accumulate here, plain and dated, for a considered
append later.

Each entry records what happened and what it costs to get wrong. Nothing here
creates, amends or narrows a rule; these are observations, not instructions.

---

## TB-01 — *(28 August 2026)* A merge can resurrect a defect that was deliberately removed

`phase1`'s copy of the checker carried the line-pinned citation form that R163 §3
ruled against and main had converted to an anchor. "Main wins" was the correct
resolution, and it was correct for a reason stronger than recency: importing the
older side would have undone a ruling.

The ruling had already been demonstrated by then, not merely argued. The anchored
citation moved three times as the register grew — 281, then 313, then 315 — and
resolved at each. The pinned form would have been stale by 36 lines at the first
of those and would have needed re-pinning at every append after.

**Every reconciliation with an older branch is a chance to reinstate something
that was removed on purpose, and the conflicts are only where that shows up
loudly.** The quiet cases are the files that merge cleanly because only one side
touched them. What made this one safe was checking, for each conflicted file,
whether the older side's unique content was superseded text or genuine work —
and the answer differed per file, so the question had to be asked per file.

Measured, for that merge: zero lines unique to `phase1` in the review register;
two in the checker, both the ruled-against form; four in the README, all pre-tag
hash values; thirty in the session record, a pre-tag snapshot; fifty-three in the
availability declaration, including a citation to a clause that does not exist.
Six files, six times the older side lost, and each time for a stated reason.

---

## TB-02 — *(28 August 2026)* An invariant can be asserted, cited, and unenforced

`src/leakaudit`'s docstring stated that the package "never accepts, imports, or
constructs `CaseLabels`" — the SC-7(c) separation every acceptance number
depends on — and cited `leakaudit.trace.assert_key_free` as stating it
executably. That module did not exist, and the string occurred nowhere else in
the repository.

The assertion was **true**: a complete AST enumeration over nine modules and
1,984 lines found no import, no bare `import protocol` (which would make the key
reachable by attribute), no dynamic import machinery at all, and the only three
textual occurrences inside docstrings. So nothing was ever wrong with the tool.
**A correct invariant with no check is still an unverified assertion**, and the
citation pointing at an absent file made it a false statement in the code
carrying the claim.

Two things this round is worth remembering for:

**The natural repair for the natural check is an exemption.** A text matcher
looking for `CaseLabels` flags the very docstrings that state the invariant, and
the obvious fix is to exempt them — which is the move this project spent a whole
close-out learning to refuse. Parsing removes the temptation rather than
resisting it: a docstring is a string constant, so it simply is not a reference,
and there is nothing to exempt. **Choose the instrument that has no false
positives to forgive.**

**The check that existed was shaped like a check and could not fail.** A text
scan in the probe suite tried to strip docstrings by splitting on triple quotes,
and its assertion carried `or True`. Its two live assertions caught
`import CaseLabels` and `CaseLabels(` but not `import protocol...`, the
attribute route. It is now a delegation to the parser.

**A fix can be correct and still have a second-order cost.** Repointing the
fixture path into `evidence/` made Python write `__pycache__` there, and the
evidence tree is attested file by file, so two unattested files appeared and the
gate went to two findings. Measured, not anticipated. The import now suppresses
bytecode for its own scope. **When a fix moves work into an attested tree, ask
what the work leaves behind.**

---

## TB-03 — *(28 August 2026)* A registration can be internally consistent and still unscoreable

The acceptance gate's third criterion scores findings against a declared
ground-truth map. The map is sound: 984 rows reconciling exactly against the
declaration's own description, its cell key declared and named twice, its scored
and unscored counts matching, its boundary uniform. The scorer is sound: it
consumes labels, applies registered gates, and its separation from the tool is
now checked executably. **Every part is right and the two do not meet.** The
map's cell is an availability class over an instrument-month; the scorer's unit
is a column. Nothing in the registration says which classes implicate which
columns, and without that the criterion cannot be adjudicated at all.

**What is worth remembering is when it surfaced.** The gap had been present since
the map was declared, through a signing ceremony, a close-out, a branch merge and
several rounds of work on the surrounding code. Reading the criterion did not
reveal it. Reading the map did not. Reading the scorer did not. It appeared the
moment a delta required a **numeric threshold and a falsifiable expectation,
stated per criterion, before anything ran** — because writing the expectation for
that criterion meant naming the unit it would be measured in, and there was no
unit to name.

Without that requirement the sequence would have been: notice the units differ,
write a small translation to bridge them, run, obtain numbers, and publish them.
The numbers would have looked exactly like a gate result. The translation would
have been a part of the scoring key, authored after the detectors' behaviour was
known — which is the specific failure this tool exists to detect.

**Two things follow.** A pre-commitment is not only a guard against tuning a
threshold to a result; it is a **completeness check on the specification**, and it
finds holes that reading cannot, because reading tolerates an unstated step and
writing an expectation does not. And an unscoreable criterion is a finding about
the registration, not an obstacle to route around: it is worth more published
than the passing gate it displaced.

---

## TB-04 — *(28 August 2026)* An absence claim about a registered document needs a population too

*"The registration declares no correspondence"* was asserted four times across
three rounds, each time from a partial read, and each time it was wrong. What was
actually registered:

- the scoring unit, at `PREREG.md` line 291 — the feature and the affected
  output cohort — with section 7.2 distinguishing probe cohorts, which
  corroborate, from the cohort that keys the unit;
- criterion 1's denominator and the rule constituting it, at line 702, stating
  that the denominator is derived from the declared map by the registered rule
  and that the declaration shows the derivation;
- the per-unit partition, ex ante and in full, in the declaration's section A.6,
  with the required list of eleven;
- **the class-to-column correspondence itself**, as the fourth column of that
  table, headed *Governing map class* — the very thing declared absent;
- the coverage limit, at section 13(j): none of the thirty-five fed columns is
  MBO-fed, so six of the ten classes attach to no fed column;
- and the consequence, disclosed in the registration at line 1435, that
  criterion 1's requirement reverses on fourteen of twenty-five.

**This project already had the rule and applied it everywhere else.** A
zero-match search over the file set is reported with its population and its
exclusions; a figure from the map names which population it counts; a check whose
population is empty raises rather than passing. The one place the discipline was
not applied was to claims about the registration itself — the largest document in
the repository, 2,228 lines beside a declaration of some 4,400, exactly where a
partial read is likeliest and least visible.

**The tell was available and was not read as one.** Four successive absence
claims, each narrowing after a fifth search, is not four independent findings; it
is one search that keeps being too small. The second one should have prompted a
change of method rather than another grep.

**What replaces it.** An absence claim about the registration carries the same
apparatus as any other: the files searched, the terms, the sections excluded and
why. And where the claim would rule something unscoreable or unavailable, the
positive form is searched for first — not *"does it say there is no
correspondence"* but *"where would a correspondence be declared if one existed"*,
which in this case was a table column two lines from a section heading already
cited for a different figure.

**The failure was symmetrical, and the record says so.** The planning layer wrote
the requirement into the deltas and did not apply it to its own assertions; the
execution layer reported the absence claims as findings without demanding a
population of itself. Neither noticed for three rounds.

---

## TB-05 — *(28 August 2026)* A ceiling is a property of the frame, not of the tool

The same ceiling was quoted four times in four rounds and gave a different number
each time:

| quoted | figure | frame the question was actually about |
|---|---|---|
| first | 0 of 4 reachable | the probed **input** cohorts |
| second | 8 of 11 | the Phase 5 built frame |
| third | 11 of 11 | the Phase 7 fed set, where the columns are defined |
| fourth | 8 of 11 | the rebuild pair, which is what the criteria are evaluated on |

**Every one of those was correct about its frame and none of them named it.**
The figure moved because the question moved, and because the answer was written
as though the figure were a property of the detector — "the tool reaches eight of
eleven" — when it is a property of which artifact the question was asked about.

This is the population rule the registration already imposes on any figure
published from the declared map, met again one level down. A ceiling names its
frame every time it is quoted, exactly as a count names the population it counts.

The cost of not doing so was three rounds: a ceiling attributed to the tool
invites a repair to the tool, and two of those rounds went looking for one.

## TB-06 — *(28 August 2026)* Backticks in a commit message, and a heredoc in a file edit

Two shell-quoting slips in one round, both after the hazard was named in this
project's own register.

**A commit message passed inline through the shell.** Its body quoted five terms
in backticks, the shell substituted each as a command, and all five vanished from
a message that was then pushed. Four sentences read with holes in them where the
subject used to be. Rewriting pushed history is barred here, so the message stays
wrong and the correction appends — which is the right outcome and a worse artifact
than getting it right once.

Every other commit this round used a message written to a file and passed by
reference, which is immune. The regression was reaching for the inline form
because the message was short. **It was not short.**

**A file edited through a heredoc.** A one-line substitution in a test file was
made by piping a script into the interpreter, which is the indirect write path
the drafting rule forbids for file content, for the reason demonstrated twice in
this register: content that passes through a quoting layer arrives changed, and
the change is invisible until something downstream disagrees.

**What both have in common** is that the tool for the job was already built and
already in use, and the shortcut was taken because the edit looked too small to
be worth it. That is the same shape as lesson 44 in the closed register: a named
hazard is not an avoided one, and the defence is to make the bad path
unavailable rather than to remember not to take it. Here the good path costs one
extra call.

---

## TB-07 — *(31 August 2026)* A registration can be signed, internally consistent, and still have an acceptance gate that cannot be run

The gate's ground truth is enumerated per column and counted per cell of a key
whose elements are side, instrument, month and class. The gate's scorer is keyed
on a pair whose second element is a decision cohort — a set of output rows
sharing a decision time. Both statements are in the registration. Neither
mentions the other, and no declared object crosses between them.

Everything else reconciles. The map's figures cross-check against two
independent measurement rounds with zero disagreeing cells. The denominator
derives from a registered rule and prints its partition check. The exclusions
are declared pre-run with grounds and artifact citations. The input surface is
declared and the scoring key is withheld from the tool. The one place it comes
apart is the join between the two halves, which is exactly the place a document
this careful would not think to look, because each half is complete on its own
terms.

**What made it findable was a rule about what may not be done.** Every earlier
round proposed a repair at the level of a field: the field carries the wrong
value, so change the value. Each was refused for want of a declared source for
the new value. The refusals accumulated. When the question finally moved from
*which value does this field carry* to *which unit does the registration
declare*, the answer was already written down in two places that had never been
read against each other.

The transferable part is not the finding. It is that a discipline forbidding the
invention of a missing piece converts a silent incompatibility into a loud one.
Had a labels producer been written at any point in the preceding eight rounds,
it would have worked, produced numbers, and buried this.

---

## TB-08 — *(31 August 2026)* When a registration enumerates a closed scope, the first question about any artifact is which row of it that artifact occupies

The coverage table names eleven detector rows and says of itself that the table
is the scope and that it closes. The acceptance criteria attach to two of those
rows. Eight rounds of work went into a field of an instrument that is none of
the eleven.

The question was never asked. "The tool" was treated as one thing, and the
field-level questions that followed were all well-formed and all aimed at
nothing the acceptance section reads. The instrument's own module header had
said so from the day it was written — that its cohort is a whole column and is
not a decision cohort, because that layer has no availability model — and it was
read past for eight rounds because nobody was asking the question it answers.

The cost of asking is one read of a table that declares itself closed. The cost
of not asking was every field-level round that followed, a pre-commitment frozen
on the wrong instrument, and a two-hour run launched against it.

The rule generalises past detectors: before what an artifact does, before what
it emits, before any question about its fields — which row of the closed
enumeration is it. If the answer is *none*, that is the finding, and it outranks
everything downstream of it.

---

## TB-09 — *(1 September 2026)* A frame can be interpretive, and TB-05 applies to it unchanged

TB-05 recorded that a ceiling is a property of the frame rather than of the
tool, after the same figure was quoted four times with four values. That was a
numerical frame — which artifact, which column universe.

The population run produced a headline shape of 66 scoring contexts and 726 unit
contexts. Both figures are true, and both are true **under a reading**: that the
first criterion is scored per side and instrument-month wherever the map carries
a strict count. Under a contaminated-only reading the same output bytes read 48
and 528. Nothing about the run differs; the denominators differ by a factor
approaching 1.4 because two defensible readings of one clause partition the
result differently.

**An interpretive frame is a frame.** It travels with the figure exactly as a
numerical one does, and for the same reason: a reader given the number without
it cannot check it.

Two things kept this honest rather than convenient. The reading was fixed in the
pre-commitment before any number existed, so it could not have been chosen for
its effect on a count. And it is the **harder** reading — it adds eighteen
contexts in which the tool could have failed. A reading that made the
examination easier would deserve suspicion; one that adds tests to it is
suspicious only if adopted after seeing that they pass, which the commit order
rules out.

The figure that survives both readings is the one worth leading with: zero
misses.

---

## Open items — recorded, not acted on

- **Whether SC-7(c) belongs in the registration gate.** A pytest-only check is
  weaker than a gate check: the gate is what the registration binds, and a suite
  can be skipped where the gate cannot. Adding it changes a registered instrument
  and would surface in the delta-of-findings comparison against the frozen
  checker. Deferred to the D2 subsystem — discriminator, window, relative-root
  defect — which touches that instrument anyway, so the two changes are ruled and
  disclosed together rather than separately. Raised R175 §6.

- **The install on a second machine.** The author's to run, and the only limb of
  criterion 5 that nothing incidental can discharge. It settles the dependency
  floors as a by-product: they are `numpy>=1.26`, `pandas>=2.1`, `pyarrow>=14`,
  and every result recorded here was measured against numpy 2.4.2, pandas 3.0.1
  and pyarrow 23.0.1 on one machine. Whether a resolver that picks pandas 2.x
  yields a working package is unknown. Recorded as unknown; widening or pinning
  the floors to dispose of it would swap an untested risk for an untested claim.
  Raised R189 §4.

- **Whether the acceptance section is scored at column granularity.** Its four
  criteria are worded about columns; the metric family and the kill criterion's
  gates read the feature-and-cohort pair. So the label gap of TB-07 blocks the
  second and not obviously the first. Reading it either way is a choice about a
  scoring key made after the detectors ran, which is why it is recorded here and
  put to the author rather than settled. Raised R188 §3.2, framed R189 §3.
