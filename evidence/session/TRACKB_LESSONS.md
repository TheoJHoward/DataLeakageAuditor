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

**SIBLINGS — enumerated 3 September 2026, retroactively (R219 §0).** The shape is
*instruments that read source text and pattern-match it*, which is mechanically
enumerable. Measured over `tools/check_registration.py` by parsing it: **32
checks, of which 8 read Python source.** One parses (`check_installability`,
after R218). Four pattern-match: `check_control_characters`,
`check_legality_table`, `check_requirement_ids`, `check_unit_grammar`. Three read
source without doing either.

**Of the four, the shape applies only where the check's subject is CODE rather
than PROSE.** `check_control_characters` looks for control bytes, and a control
byte in a docstring is a real finding, so prose is correctly in its scope. The
other three take documentation consistency as their subject, where prose is the
thing being checked rather than a source of false positives. **So the sweep
returns no further instances**, and the one that was vulnerable —
`check_installability`, reading an English sentence as an import — is the one
already repaired at D-V30A-51.

*The enumeration is mechanical and complete; the classification of which four are
vulnerable is a reading of each check's subject, and it is mine.*

**And the lesson cost two applications to learn.** TB-02 was written when the
citation check moved from text to parsing, in these words: *"a docstring is a
string constant, so it simply is not a reference, and there is nothing to
exempt."* Nobody asked at the time what else scanned text. The neighbour was
found eight months later by being defeated by a docstring explaining an
instrument — which is why entries now carry this line at the moment they are
written.

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

## TB-10 — *(1 September 2026)* A one-point model cannot see which term it omitted, and a claim about a forecast needs checking against the file that measures it

Two failures, and the second is the worse one.

**The model.** The population run's cost model charged one term — snapshot rows,
at 270 s per million, fitted on one instrument-month. At that instrument-month it
is accurate to four per cent. Across the population it under-predicted the probe
phase by 2.35×, with a realised coefficient ranging from 646 to 1,137 s per
million. Trade rows correlate better than snapshot rows (0.814 against 0.727),
and the fitting point carries the lowest trade count of the large instruments by
an order of magnitude.

At one point every term is confounded with every other, so a one-point fit does
not merely have wide error bars: **it cannot tell you which term it left out.**
It will interpolate its own fitting point beautifully while missing the
population, and the quality of the interpolation reads as evidence for the model.

**The narration.** Worse, and the reason this is here rather than in the ledger
alone. The round's report and its commit message both said the overrun landed in
the term the pre-commitment had refused to predict — that the forecast had
"bounded its own reliability and was right about where it was unreliable". The
opposite is true: the refused term came in 2.1× **under** the figure quoted
beside the refusal, and the predicted term overran. The run file measuring both
was committed in the same act as the sentence that got it wrong.

The claim was favourable, it was about the discipline itself, and it was not
checked against the file sitting next to it. **A self-congratulatory claim is the
one that most needs a measurement behind it**, because nobody in the loop is
motivated to look.

---

## TB-11 — *(1 September 2026)* Claims that could be unfavourable were verified; claims that flatter the process were accepted

This is the entry a reader of this project should find first.

Every claim in this register that could have embarrassed the record was checked
hard. The instrument change that reverted. The provenance of the column-level
dispositions, verified from the commit history rather than from their own
heading. The label gap, found by refusing eight rounds of field-level repairs.
The detector allocation, which cost eight rounds of work aimed at an instrument
the acceptance section does not score. Each of those was adversarial toward the
record, and each was pursued to a citation.

**The calibration claim could only make the record look good, and it was the one
claim nobody examined.** The round that ran the full population said the cost
overrun had landed in the term the forecast declined to predict — that the
forecast "bounded its own reliability and was right about where it was
unreliable". The opposite was true, and the file measuring it was committed in
the same act as the sentence.

**The asymmetry is the finding.** It is the most dangerous one available, because
it is the direction that silently inflates a record and because nothing in a
review process is motivated to catch it. An adversarial reviewer attacks claims
that would embarrass the author; nobody is assigned to attack the ones that
please everyone.

**What follows from it, in practice rather than as a resolution:**

1. A claim about the method's own performance is a claim, carrying the same
   evidence standard as any other — and in practice a higher one, because no
   participant is motivated to falsify it.
2. A favourable self-assessment is checked against the artifact **before** it is
   repeated, not praised first and audited later.
3. A prediction is assessed **term by term from the measured output**, never
   against its total. The total that started this was 1.63x, and the story told
   about it was wrong in both directions at once — the predicted term overran by
   2.35x while the unpredicted one came in 2.1x under.

The round that followed put both of its own favourable claims to the test. The
cost model was stated as a per-instrument-month prediction with a halt, and came
in at 0.95x, 1.05x and 0.96x on its three terms. The schema-uniformity claim was
stated so it could fail, and it failed — against a fact already recorded in this
register two rounds earlier. **Two claims, both flattering, both tested, one
wrong.** That ratio is the argument for the rule.

---

## TB-12 — *(2 September 2026)* A known positive tests the premise, not only the code

A check was written to detect leakage that survives permuting the label. Its
known positive did not fire, and the implementation was not the reason.

The premise was false. Permuting a label destroys the pairing between a feature's
rows and the label's rows **regardless of why the pairing existed**, so a
positional relationship collapses exactly as a genuine one does. Measured on the
most positional relationship constructible — pure row order against a sorted
label — the shuffled absolute correlation came out 0.076, 0.050, 0.031, 0.046,
0.018. There is no statistic there to threshold.

Worse, the one case where a shuffled correlation persists is a heavily imbalanced
label, where a permutation often nearly reproduces the original vector. The check
would have reported class imbalance as positional leakage — a false positive
dressed as a subtle finding, which is the most damaging kind a leakage tool can
emit, because it is the kind users believe.

**The rule has a second use, and it is the stronger one.** Catching bugs is what
a known positive is usually for. What it did here was establish that the check
did not exist: a check that cannot be made to fire has not failed its test, it
has been shown to have no subject. The premise, not the code, was what the
positive tested.

The corollary is worth stating because it is counterintuitive: **a check that
passes every test you can write for it, and that you cannot construct a positive
for, is not a working check.** It is an untested claim wearing a green tick.

---

## TB-13 — *(2 September 2026)* A detection that arrives as a library's exception is a detection nobody reads as one

Three times now, in three different pieces of code.

1. The identity control's mask was index-aligned. A write-back that replaced a
   frame's index — one of the faults the control exists to catch — left the mask
   pointing at labels that no longer existed, so the *next* column's write raised
   a pandas `IndexError`.
2. The same control, again: a write-back that changed a frame's row count broke
   the positional mask the same way.
3. `availability_fn` returning too few values. The `Series` constructor raised a
   pandas error about index lengths before the module's own length check ran.

In every case the tool had **detected exactly what it was built to detect**, and
what reached the operator was a stack trace from somebody else's library, naming
an index. A crash reads as "the tool is broken"; the truth was "the tool found
the thing". Nobody triages a `ValueError` as a finding.

**The shape to watch for:** a validation that runs *after* the operation it is
validating. If the operation can itself fail on the invalid input, the library
raises first and the check never speaks. The fix is always the same and always
cheap — check before the operation, and raise the tool's own error with the
tool's own explanation.

This is the counterpart to the silence rules. Those exist so a non-answer is not
read as a clean one; this exists so a real answer is not read as a malfunction.
Both are about what the operator takes away, which is never the same as what the
code computed.

---

## TB-14 — *(2 September 2026)* An extraction that replaces nothing is a third implementation wearing the word "extracted"

One timezone rule lived inline in two places. It was pulled into a named function
so that one rule would live in one place — and neither original was removed. The
probe still runs its copy. The harness still runs its copy. The extracted
function has never executed against the real fixture.

**And the three do not agree.** On the case the fixture actually contains, the
two inline copies convert and the extracted one refuses. So the refactor did not
reduce three chances to get the rule wrong; it made three implementations where
there had been two, and put the newest one where nothing calls it.

**Two things would have caught it, both cheap.** Deleting the originals in the
same commit, which is what "extract" means. Or one search for the new function's
name, which returns zero from the harness and would have said so in a second.

**The tell to watch for:** a function whose only callers are its own tests. That
is not an extraction, it is a proposal. And synthetic tests will never notice,
because the divergent case is one nobody constructs by accident — a frame with a
mixed timezone arrives from real data, not from a fixture someone wrote.

**The second half is the worse one and it belongs beside TB-11.** The commit
message asserted the extraction had reduced the duplication. That was a
favourable claim about the work, made in the same act that failed to do it, and
checking it was one grep. The asymmetry TB-11 records — unfavourable claims
verified, flattering ones accepted — recurred in the round that recorded it.

---

## Open items — recorded, not acted on

- **Whether SC-7(c) belongs in the registration gate.** A pytest-only check is
  weaker than a gate check: the gate is what the registration binds, and a suite
  can be skipped where the gate cannot. Adding it changes a registered instrument
  and would surface in the delta-of-findings comparison against the frozen
  checker. Deferred to the D2 subsystem — discriminator, window, relative-root
  defect — which touches that instrument anyway, so the two changes are ruled and
  disclosed together rather than separately. Raised R175 §6.

- ~~**The install on a second machine.**~~ **CLOSED 3 September 2026, both
  limbs, and removed from this list rather than left saying something the record
  contradicts.** The item is struck through and not deleted, because a reader of
  an earlier revision needs to know it was open and how it closed.

  *The floors limb is discharged by measurement.* It read "whether a resolver
  that picks pandas 2.x yields a working package is unknown". It is now known:
  the declared floors were pinned exactly — numpy 1.26.4, pandas 2.1.4, pyarrow
  14.0.2 — on Python 3.11.9, the lowest point of every declared dimension at
  once, and the suite and a canonical pipeline digest are identical to every
  other measured environment. `INSTALL.md` carries the table. Nothing was widened
  or pinned; the numbers stand as declared and are now measured.

  *The stranger limb is discharged by ruling, not by measurement.* The author
  ruled on 3 September 2026 that nobody else walks it. The permanent recorded
  state is in `DEFINITION_OF_DONE_WALK.md` Part IV: met on the measurement
  available, by a walker who authored the code and knew every answer, which
  establishes that the six identified frictions are closed and not that a
  newcomer finds none. The uncontrolled variable is foreknowledge; environment
  was controlled separately. **That is a written limitation and therefore a
  limitation — which is why it is not carried here as a task.** Raised R189 §4,
  closed R215 §6.

- **Whether the acceptance section is scored at column granularity.** Its four
  criteria are worded about columns; the metric family and the kill criterion's
  gates read the feature-and-cohort pair. So the label gap of TB-07 blocks the
  second and not obviously the first. Reading it either way is a choice about a
  scoring key made after the detectors ran, which is why it is recorded here and
  put to the author rather than settled. Raised R188 §3.2, framed R189 §3.

## TB-15 — *(3 September 2026)* The wrong prediction is the one that pays; a correct one would have told nobody anything

A manifest regeneration was predicted at plus one line for one added file. It
came back at zero. Re-predicted against the script's own stated population, it
came back at plus two. Both misses were defects, and neither would have surfaced
from a run that matched.

**Zero, because the append population is the COMMITTED set.** The regenerator
enumerates with `git ls-files evidence`, so a file that exists on disk and is not
staged is invisible to it. The prediction was made against "files present"; the
script's docstring says "one line per COMMITTED file under evidence/". The
docstring was right and unread.

**Plus two, because appending after a trailing empty element writes below a blank
line.** `text.split("\n")` on a file ending in a newline yields a final `""`. It
lands in the output list, and every appended digest goes after it. One stray
blank per append, accumulating silently in an attestation file, in a script whose
whole job is to keep that file honest.

**Neither is visible from a passing run.** The manifest verified clean both
times: `0 line(s) disagree with the file on disk`. The blank line is not a hash
line, so the verifier skips it; the missing entry is not a wrong entry, so
nothing disagrees. A self-check that only asks "is what is written correct?"
cannot ask "is what should be written here at all?" — which is the same absence
shape the tool itself exists to report, found in the tooling that attests to the
tool.

**The prediction is the instrument.** Measuring alone would have produced a
manifest, a clean verify, and no information. The number had to be committed to
in advance for the disagreement to exist to be noticed. That is the whole content
of predict-then-measure and this is the clearest case of it in the register:
TB-10 caught a cost claim this way, and here the same discipline caught a latent
defect in an attestation artifact that no test covered.

**The tell to watch for:** a derived-file regenerator whose population is one set
and whose caller is thinking of another. "Present", "tracked", "staged" and
"committed" are four different sets, and a script that means one of them while
its user means another fails silently in exactly one direction — omission, never
error.

## TB-16 — *(3 September 2026)* A declaration can govern by mechanism, and a search for names will report it absent

The question was whether the availability declaration says anything different
from what the probe computes, per column. The probe perturbs sixteen raw frame
columns. The declaration enumerates built feature columns by heading. **It names
none of eight of the eleven trades columns.**

A per-name search is the obvious way to answer, and it would have been
well-formed: a stated population, a complete enumeration, an exact answer. The
answer would have been "the declaration is silent on these columns," and it would
have been wrong. The declaration is not silent. It declares the JOIN MECHANISM —
the merge on a floored second, whose absorbed window ends one second after the
floor — and every one of those columns inherits its rule from that. A mechanism
is not an enumeration, and grep only sees enumerations.

**This is a new shape of the absence-claim failure, and the worst-behaved one so
far.** The earlier instances were sloppy populations: a claim of absence made
over a set narrower than the claim. Here the population is right, the search is
right, the execution is right, and the answer is still wrong — because the thing
being searched for was never going to be written down in the form searched for.
Nothing in the method catches that. The only thing that catches it is asking, of
a null result, *"could this be governed by something that does not carry these
names?"*

**What made it come out right was stating the population TWICE.** P1, what the
probe perturbs. P2, what the declaration enumerates. Writing both down made their
disjointness visible as a fact needing explanation, rather than as a null result
needing reporting. Had only one been written, the gap would have read as an
answer.

**And it was load-bearing.** The same read turned up a docstring stating an
availability formula the code does not compute (D-V30A-43). Answering by reading
that docstring — the other obvious cheap route — would have returned the opposite
answer on eleven columns.

**The tell to watch for:** a null result whose population is disjoint from the
population of the thing that would have governed it. Two sets that never
intersect, and a conclusion drawn from their non-intersection. When the answer is
"the document does not mention X", the next question is always whether the
document mentions the machinery X is made of.

## TB-17 — *(3 September 2026)* An events register can never supply a rate, because non-events do not present themselves for recording

A question was asked of this project's registers: how often does a fix's own
acceptance test find a defect in that fix, compared with how often an original
module's first test found one? Both numerators looked available. Neither
denominator existed, and no amount of care would have produced one.

**`DEVIATIONS.md` scopes itself in its second paragraph:** *"These entries are
disclosures of fact about the tagged state."* A defect caught by a test and fixed
in the same commit is not a fact about the tagged state. It has no reason to
appear, and does not.

**`TRACKB_LESSONS.md` records what was notable.** Sixteen entries, none a
pre-commit catch on an original module.

**Git records what someone chose to mention.** Twenty-five commits touch the
package; three name a catch in their subject.

All three are numerators. **The denominator was never something anyone declined
to write — it was never something that could be written.** A module whose first
test found nothing produces no artifact. There is no line in any file saying "the
test ran and was clean," because nothing happened, and nothing happening does not
present itself for recording.

**The tell:** any "how often" question asked of these registers returns a
numerator and an argument, and the argument will feel like the answer. It will be
made of real entries, correctly cited, and it will still be a rate with no
denominator.

**This is a DIFFERENT failure from the absence-claim discipline, and quieter.**
That discipline covers populations that exist and were not enumerated — the fix
is to enumerate them. Here the population cannot exist in the record's own
design, so there is nothing to go and count. The absence-claim habit ("state your
population") does not catch it, because the population can be stated and is
simply empty on one side.

**What to do instead.** Take the mechanism rather than the rate. At n=2 the
useful finding was not a frequency but a location — see TB-18 — and a location is
actionable immediately where a rate over eight events never would have been.

**And the fix that looks obvious is worse than the gap.** Requiring "nothing
happened" to be written after every fix would be complied with unevenly, and
uneven compliance on non-events produces a wrong rate — which computes,
publishes, and persuades. An absent denominator reports no result. A sloppy one
reports a number.

## TB-18 — *(3 September 2026)* The damage from a fix lands on what the fix was holding constant

Two occasions, and the count is stated here so this is never quoted as a rate:
**n = 2.**

Both times, a fix was verified against the cases it was written to change, all of
which passed, and the defect was in a case it was written to *preserve*.

**Instance one.** A guard was added so a build function returning the wrong type
would be told so instead of crashing inside a module the user has never opened.
The three wrong-type cases all returned one clean line. The damage was to the
case being preserved — a user's own pipeline raising, which must keep a traceback
pointing at *their* file. The guard was applied twice, once by the CLI and once
by the library entry point, and put two frames of this tool's plumbing into that
traceback. Thirteen lines became twenty-two.

**Instance two.** The idempotency fix for instance one used a marker meaning
"some guard is applied". What it was holding constant was the ability of a
*different* guard to apply later. A generic marker would have let a second guard
find the flag set and decline — its check unperformed, nothing said.

**Why the suite could not see either.** Both suites were green. Both fixes
behaved correctly in every respect they were written for. Instance one was
visible only in the *stack* of a case that is supposed to fail, and only by
reading that stack rather than its last line. Instance two was visible only by
constructing a second guard that did not yet exist.

**The practice this earns.** Every fix's acceptance test names what the fix HOLDS
CONSTANT, and tests that directly. Both instances were found because something
incidentally exercised the held-constant case; making it deliberate costs one
assertion per fix. The re-run-the-wrong-turn discipline covers this for free when
the held-constant case is itself a wrong turn — which is how instance one
surfaced — and does not when it is not.

**Two events and a mechanism is not a trend.** It is a place to look, available
now. TB-17 records why the trend is not available and will not become available
by trying harder.

## TB-19 — *(3 September 2026)* A positive that every wrong instrument also fires on is a wiring test, and the discriminating case is often a negative

**A refinement to the known-positive rule, and it belongs beside TB-12 because it
is the next layer down.** TB-12 says a known positive tests the premise and not
only the code. This says: a known positive also has to be chosen to discriminate
between the instrument you built and the instrument you might have built by
mistake.

**The rule as previously written is satisfied by a positive so extreme that every
candidate instrument fires on it.** Such a positive establishes that the
instrument is connected to its input. It says nothing about whether the
instrument measures the intended quantity.

**The proof came from a check that was never built.** The retired shuffle check's
intended known positive was a frame where a feature IS the label. It would have
fired. It fires for a signal test, a leakage test, and anything else anyone would
propose — so it would have confirmed the check was wired, the check would have
been believed, and the check computes the wrong statistic. The positive could not
have caught that, because the positive could not tell the two apart.

**The discriminating case is frequently a NEGATIVE:** an input on which the wrong
instrument fires and the right one is correctly silent. For the shuffle check
that case is a pipeline with strong genuine signal and no leak — the signal test
fires loudly, the leakage test is silent, and one run separates them.

**What this looks like in practice, from the audit it prompted.** The availability
probe's own controls already do it, and say why in prose written before this
lesson existed. Its positive — a builder reading its own second's aggregate —
fires for a plain dependency probe too, so the positive alone is a wiring test.
The discrimination is carried by the negative's *second* limb: a builder reading
the previous second must be silent in-second AND must move the following second's
rows. A dependency probe fails that pair; an instrument that reports movement
without attributing it to a second fails it too.

**PREDECESSOR, linked rather than left as a second name for one idea (TB-21).**
This was already written, months earlier, in `tests/phase1/b6_probe_a_controls.py`:
*"A negative that moves nothing anywhere is a probe testing itself."* Same
lesson, stated well, placed where it governed one control and nothing else.

**The tell:** ask of every known positive, "what else would fire on this?" If the
answer is "anything that is plugged in", the positive is a continuity test and
the validity question is still open.

**And the audit has a bound, recorded so its silence is not read as coverage.**
This was applied to the two runtime detector rows that carry reported claims. The
rest of the project's known positives were not examined, deliberately, and their
status is unexamined rather than confirmed.

## TB-20 — *(3 September 2026)* A defect that makes a thing do nothing is invisible to tests of that thing

Two defects were found in one round, by two different accidents, and neither was
reachable by any test in a 637-test suite. They share one property, and it is
the property that puts them outside testing altogether.

**`AvailabilityModel.available()` had no callers.** So no test of the probe
exercised it — and a test written *for it* would have passed, because the
function is correct. It was merely unreached. The suite could confirm the
comparator computes the right answer and could not notice that nobody asked it.

**`round_reconciliation` scanned a directory that had been dead since August.**
So every run passed, and a test of its logic passes too, because the logic is
fine and the input is empty. A check over an empty population is green forever.

**Neither was found by looking for it.** One fell out of asking *what wrong
instrument can I not rule out?* — which forced a reachability check on the
comparator. The other fell out of asking *is this scan deliberate?* Both were
side effects of asking what a check COVERS rather than whether it PASSES.

**That is the generalisable move: coverage questions find what pass/fail
questions structurally cannot.** A pass/fail question takes the population as
given and asks about the answer. A coverage question asks whether the population
is the one intended — and an empty or unreached population produces a perfect
pass rate.

**And a third instance arrived in the same sweep**, which is why this is a lesson
and not an anecdote: `column_modes` was parsed, validated with four refusals, and
never passed to the probe by the CLI. Every test of the parsing passed. Every
test of the probe passed. Nothing joined them, and a user declaring per-column
modes silently got a different probe path with a measurably different answer.

**The tell:** a component with thorough tests and no caller; a check that has
never once emitted a finding; a config key with careful validation and no
consumer. In each case the tests are about the thing and the defect is about
whether the thing is *connected to anything*, which is a different question that
the tests are not asked.

**What this justifies.** Running a halt list BACKWARDS over existing code. A halt
list stops a failure going forward and does nothing about instances already
resident, and the resident ones are — by this lesson — exactly the ones a suite
cannot see. *"A config key the loader reads and ignores"* had been on this
project's halt list for thirteen deltas while three instances sat in the package.

**SIBLINGS.** The shape is *a component with thorough tests and no caller; a
check that has never emitted a finding; a config key with careful validation and
no consumer* — all enumerable by tracing what a real run reaches. Enumerated
across three populations this round and the last: the config keys (10 accepted,
measured complement, zero unexplained at HEAD); the availability probe's module
path (7 modules, `PROBE_PATH_SET.json`); the registration checks that read source
(8, listed under TB-02). **Not yet enumerated:** defaults taken where a rule says
refuse — the `.get(key, default)` population — which needs a trace this project
does not have and is recorded as unchecked rather than assumed clean.

## TB-21 — *(3 September 2026)* Knowledge written where it governs nothing has to be discovered twice

The refinement recorded at TB-19 — that a positive every wrong instrument fires
on is a wiring test — was **already written down**, months earlier, in the B-6
control file:

> *"A negative that moves nothing anywhere is a probe testing itself."*

Same idea, stated well, and correct. It sat in one file, as an aside, attached to
one control. **So it governed that control and nothing else**, and it had to be
rediscovered from a completely different direction — an audit of the shuffle
check's positive — and written down again under a new name.

**The insight was not missing. Its placement was.** A sentence in a control's
docstring is read by whoever edits that control. A lesson in the lessons file is
read by whoever is looking for lessons. Neither is read by the person writing the
next control, which is who needed it.

**This is the register problem in a different key.** TB-17 records that an events
register cannot supply a rate because non-events are unwritable. This is the
adjacent failure: a project can lose knowledge it *already wrote down*, by
writing it somewhere that governs nothing. The cost is not that the knowledge was
absent — it is that the same thinking was paid for twice, and the second payment
only happened by luck.

**The repair, and it is cheap:** when a lesson is recorded, link the earlier
statement of it rather than leaving two names for one idea. TB-19 now names the
B-6 sentence as its predecessor. The two are one lesson with two dates, which is
what they always were.

**The tell:** discovering that something you just worked out is already written
in a comment somewhere. That is not a pleasant coincidence — it is evidence that
the first writing was placed where it could not do its job.

**SIBLINGS.** The shape is *a lesson stated in one file's prose that governs only
that file*. It is NOT mechanically enumerable — finding it requires reading prose
for insight rather than matching a pattern — so no sweep is claimed and the
exemption is recorded rather than left as silence. **Two instances are known:**
the B-6 control's *"a negative that moves nothing anywhere is a probe testing
itself"*, which preceded TB-19 by months; and TB-02's parsing lesson, which
preceded D-V30A-51's repair by eight. Both were found by arriving at the same
conclusion from a different direction and then noticing it was already written.
**That is the only discovery route observed so far, and it is not a method.**

## TB-22 — *(5 September 2026)* A safety argument is about a layer, and the thing that changes is often at another one

**Two instances of one mechanism, which is this project's standard for recording a
lesson rather than a coincidence.**

**First instance, R220.** `.gitattributes` carried `* -text`, which guarantees git
performs no line-ending conversion. That guarantee was read as "line endings are
safe here." The conversion that happened was performed by a Python edit —
`read_text` then `write_text(newline='')` — *above* git, on a file git then stored
faithfully. **The guarantee was about storage; the change was in the pipeline.**

**Second instance, R227.** Installing CPython 3.11 alongside 3.12 was ruled safe
and reversible: side-by-side installation, the launcher selects by version,
existing installations untouched. **Every one of those statements is true, and
none of them is about the property that changed.** They describe files on disk.
What changed is what a bare *name* resolves to: the installer's *Add to Path*
component prepends its directory to the user `PATH`, so in every shell started
afterwards `python` means 3.11.9 rather than 3.12.10. The safety argument was
about the filesystem; the breakage was in name resolution.

**The tell, and it is askable in advance:** when an action is ruled safe, name the
layer the safety argument is about, then name the layer the thing you care about
lives at. If they differ, the argument has not been made. "Reversible" and
"side-by-side" are claims about installed files. "Byte-exact" was a claim about
git. Neither was a claim about the behaviour that changed.

**Why it is hard to catch.** In both cases the guarantee was *load-bearing for
something* — git really will not convert, the installs really are independent —
so the argument feels checked. What is missing is not rigour about the claim; it
is a question about its scope, and the scope is usually left implicit precisely
because the claim is true.

**And in both cases the failure was silent at the layer that broke.** Git reported
nothing because git did nothing wrong. The 3.11 install reported nothing because
the install was correct. A layer that is behaving correctly does not announce that
something above or beside it now behaves differently.

**SIBLINGS.** The shape is *an action ruled safe on a property of one layer, where
the property that mattered belonged to another*. It is **not mechanically
enumerable** — finding an instance requires reading a past safety argument and
asking what layer it was about, which is judgment rather than pattern-matching —
so no sweep is claimed and the exemption is recorded rather than left as silence.
**Two instances are established** (above). **Three candidates are named without
being adjudicated**, because naming a candidate and calling it an instance are
different acts:

- **The venv builds.** `dod_env` and `floor_env` are isolated by
  `include-system-site-packages = false`, which is a claim about *import*
  resolution. It is not a claim about which interpreter builds the venv, and that
  is chosen by whatever `python` meant at the moment — the same name resolution
  this entry is about. Unadjudicated: both existing venvs record
  `version = 3.12.10`, so nothing has gone wrong, and nothing was checking.
- **The tag operations.** `prereg-v30a`'s guarantee is that the tag message
  carries digests of twenty registered paths. That is a claim about *content at
  the tagged commit*. It is not a claim about the working tree, the manifest, or
  what a later reader's checkout produces. Unadjudicated.
- **The `.gitattributes` reading itself**, as a standing artifact rather than as
  R220's event: it is still in the tree, still guarantees only what it guaranteed,
  and the working rule that now protects line endings is `tools/safe_edit.py`,
  which operates at the layer where the damage occurred. Unadjudicated as a
  *second* failure; recorded because the two mechanisms are still separate and a
  reader could mistake one for the other.

**Two established, three named, and the list is a lower bound** — the same
epistemic position as TB-21's, and for the same reason: the discovery route is
noticing, not searching.

## TB-23 — *(5 September 2026)* Search for what a thing produced, not only for what it was

**Configuration is transient; output is committed.** A virtualenv's `pyvenv.cfg`
dies with its directory. The run it hosted printed its versions into a file that
somebody kept.

**The instance.** Asked whether any environment on this machine had ever been a
3.11 one, the search read every `pyvenv.cfg` under the session temp root, found
two and both recording 3.12.10, and concluded *"no venv was ever built on 3.11."*
Two minutes' worth of evidence to the contrary was sitting in the same tree:
`dod_work/py311_out.txt`, timestamped two minutes after the 3.11 installer
finished, carrying `# python 3.11.9 / # numpy 1.26.4 / # pandas 2.1.4 /
# pyarrow 14.0.2` in its banner. The environment had recorded itself in its own
output while its configuration was deleted with the directory.

**The population was WRONG, not merely narrow, and the distinction is the
lesson.** A narrow population under-covers and knows it. This one was chosen so
that the thing sought could not appear in it: a deleted venv leaves no config by
construction, so searching configs for evidence of deleted venvs can only ever
return the answer it returned. **Ask whether the population is one in which the
thing sought would be visible if it existed** — before running the search, because
afterwards the empty result reads as an answer.

**And the second evidence type was the durable one.** The scratch directory has
been pruned repeatedly; the captured outputs survived because they are what runs
are kept for. That is general: a process's *configuration* is scaffolding and gets
cleaned up, while its *output* is the reason the work was done and gets retained.
So a search for evidence that something existed should look at what it emitted
first, and at how it was set up second.

**A supporting observation from the same round, which is why this is not one
anecdote.** The retired portability digest `15dc83c78950d42b…` failed in the
mirror-image way: the outputs survived — five of them, agreeing byte-for-byte
under every convention tried — and the *procedure* that turned them into the
published number did not. Output outlived configuration there too. The digest was
unusable precisely because the transient half was the half nobody committed.

**The tell:** an absence claim whose search space is made of things that get
deleted. If the answer would be "nothing found" whether or not the thing existed,
the search has not been run yet.

**SIBLINGS — the question this raises is whether any other "no artifact records
this" conclusion in the project was reached by searching only for configuration.**
Not mechanically enumerable: finding one requires reading a past absence claim and
asking what kind of artifact its population was made of. No sweep is claimed, and
the exemption is recorded rather than left as silence.

**One instance established** (above). **Two candidates named and not
adjudicated:**

- **`round_reconciliation`'s residue**, whose population is *files currently in
  the work root*. A file created and deleted within a round is invisible to it by
  construction, and the check's claim is about what is left rather than about what
  happened. Whether that is a gap or the intended scope is unadjudicated.
- **The probe path set**, whose population is *modules a traced run executed*.
  `PROBE_PATH_SET.json` already carries this bound in its own terms — the set is a
  function of which runs measured it — so it may be the case where the discipline
  was applied correctly rather than a sibling. Named because a candidate ruled out
  on inspection is worth more than a candidate never raised.

**Related but distinct, kept separate on purpose (R229 §4).** TB-22 is about a
*safety argument* scoped to the wrong layer. This is about a *search* scoped to
the wrong artifact type. Both are scope failures and they fail at different
moments — one before an action, one during an investigation — and merging them
would give one entry that names neither precisely.
---

# THE CLASSIFICATION — made by hand, with its membership list

*(3 September 2026, R224 §4 item 3.)*

**Why by hand, and what the machine version got wrong.** A crude classifier over
these entries groups them by the words they share, and the words these entries
share are the vocabulary the whole project is written in — *population*, *silence*,
*positive*, *declared*. It put TB-05 with TB-17 because both say "rate", and it
separated TB-19 from TB-12, which are the same lesson one layer apart. Grouping by
shared vocabulary in a corpus with one vocabulary is grouping by nothing.

**The rule for membership.** All **23** entries are in **exactly
one** family, and the families **jointly cover** all twenty-one — the same totality
shape the probe path set and the config-key complement use, and for the same
reason: a classification with an unassigned entry has not classified anything.
Where an entry genuinely touches a second family it is cross-referenced, and the
cross-reference is not a second membership.

---

## F1 — Something present that governs nothing

*Declared, cited, documented — and connected to no consumer. The class the config
complement was built to close, recurring at four different levels.*

**Members: TB-02, TB-14, TB-20, TB-21.** Four of twenty-three.

- **TB-02** — an invariant asserted and cited, enforced by nothing.
- **TB-14** — an extraction that replaced nothing: a third implementation wearing
  the word "extracted".
- **TB-20** — a defect that makes a thing do nothing is invisible to tests *of that
  thing*, because they exercise the thing and not its wiring.
- **TB-21** — knowledge written where it governs nothing has to be discovered twice.

*Cross-reference:* TB-16 is the near-miss of this family and is deliberately not
in it — there the declaration **did** govern, by mechanism, and the search for its
name reported it absent. That is a claim-side failure, so it sits in F2.

## F2 — A claim without its population or its frame

*The absence claim and the bare number. The two halves of one discipline: say what
you looked at, and say what the figure rests on.*

**Members: TB-04, TB-05, TB-09, TB-16, TB-17, TB-23.** Six of twenty-three.

- **TB-04** — an absence claim about a registered document needs a population too.
- **TB-05** — a ceiling is a property of the frame, not of the tool.
- **TB-09** — a frame can be interpretive, and TB-05 applies to it unchanged.
- **TB-16** — a declaration can govern by mechanism, and a search for names will
  report it absent. *(The population of the search was names; the population that
  mattered was mechanisms.)*
- **TB-17** — an events register can never supply a rate, because non-events do not
  present themselves for recording. *(The denominator is the missing population.)*
- **TB-23** — search for what a thing produced, not only for what it was.
  *(The population was one in which the thing sought could not appear.)*

**TB-23 is F2's sharpest case and it belongs here rather than with TB-22.** The
others under-cover a population; this one selects a population in which the
answer is fixed in advance, so the search returns "nothing found" whether or not
the thing exists. TB-22 is a *safety argument* scoped to the wrong layer, which
fails before an action; this is a *search* scoped to the wrong artifact type,
which fails during an investigation.

## F3 — A control that does not discriminate

*The positive fires, and the firing establishes less than it appears to.*

**Members: TB-12, TB-15, TB-19.** Three of twenty-three.

- **TB-12** — a known positive tests the premise, not only the code.
- **TB-15** — the wrong prediction is the one that pays; a correct one would have
  told nobody anything.
- **TB-19** — a positive every wrong instrument also fires on is a wiring test, and
  the discriminating case is often a negative.

**These three are one lesson at three depths and the ordering is the content.**
TB-12 asks whether the positive tests the *premise*. TB-19 asks whether it
separates the instrument built from the instrument nearly built. TB-15 is the same
question turned on a prediction rather than a test: a prediction that comes true
distinguishes nothing, and its value was entirely in being falsifiable.

## F4 — A registration or instrument that cannot be run as written

*It is internally consistent, it is signed, and it does not survive contact with
execution.*

**Members: TB-03, TB-07, TB-08, TB-10, TB-13.** Five of twenty-three.

- **TB-03** — a registration can be internally consistent and still unscoreable.
- **TB-07** — signed, consistent, and with an acceptance gate that cannot be run.
- **TB-08** — when a registration enumerates a closed scope, the first question
  about any artifact is which row it occupies.
- **TB-10** — a one-point model cannot see which term it omitted.
- **TB-13** — a detection that arrives as a library's exception is a detection
  nobody reads as one.

## F5 — A change that damages what it was not aimed at

*The collateral, and it lands on whatever the change was holding constant.*

**Members: TB-01, TB-06, TB-18, TB-22.** Four of twenty-three.

- **TB-01** — a merge can resurrect a defect that was deliberately removed.
- **TB-06** — backticks in a commit message, and a heredoc in a file edit: content
  passing through a quoting layer becomes something else.
- **TB-18** — the damage from a fix lands on what the fix was holding constant.
- **TB-22** — a safety argument is about a layer, and the thing that changes
  is often at another one.

**TB-22 is this family's DIAGNOSIS rather than a fourth instance of it**, and it
arrived last for a reason: collateral is what you notice, and the scope of the
safety argument is what you would have had to ask about first. TB-06 was already
layer-shaped — content passing through a quoting layer becomes something else —
and nobody read it that way until there were two more.

## F6 — The reading is biased by what it would cost

**Member: TB-11.** One of twenty-three — and the family of one is the finding.

- **TB-11** — claims that could be unfavourable were verified; claims that flatter
  the process were accepted.

**THE REASON, SAID OUT LOUD, because leaving it implied is the failure itself
(R226 §4).** A lesson about not flattering yourself is one you do not write down
at the moment you are being flattered. F6 is the single family whose membership
cannot be trusted to be complete, because **the failure it names suppresses its
own recording** — and no amount of diligence fixes that, since diligence is the
faculty the failure disables. The counter has to be external or mechanical.

**What was adopted, and it is external rather than mine.** Every round's
strongest positive result gets its flattering reading named and a falsifier
stated, as a standing item in the delta that receives the round — not as
something I remember to do. R212 §0 and R215 §0 did it by hand and both times it
changed the conclusion, which is the evidence that the item is worth its place.
Anything I could add here would be a resolution to notice, and a resolution to
notice is what F6 records failing.

**A family of one is normally a sign the classification is too fine. Here it is a
sign the register is incomplete.** The shape has recurred at least twice since
TB-11 was written — an audit of my own halt lists that found fourteen dropped
rules, and a round where the flattering framing was taken over the accurate one
and had to be corrected from outside. **Neither was written down as a Track B
entry**, and the reason is visible from inside the family: an entry about one's own
asymmetric scrutiny is exactly the entry asymmetric scrutiny does not write. It is
recorded here as a gap in the register rather than as a lesson with one instance.

---

## TB-19, at length — the membership this classification asks for

**SIBLINGS — enumerated by hand, 3 September 2026 (R224 §4 item 3).** The shape is
*a known positive so strong that every candidate instrument fires on it, so it
establishes connection and not validity.* Enumerated by reading each control's
positive and asking "what else would fire on this?", which is not mechanical, so
no sweep is claimed and the population is the controls examined rather than all of
them.

**Three instances found, and one clean counter-example:**

1. **The retired shuffle check's intended positive** — a feature that IS the label.
   It fires for a signal test, a leakage test and anything plugged in. The check
   computed the wrong statistic and this positive could never have said so. The
   only case that separates them is a **negative**: strong genuine signal, no leak.
2. **The identity control**, audited twice on this ground. Its positive was
   initially an input on which any comparator that runs at all reports a
   difference; the discrimination now comes from a case where a plausible wrong
   implementation is *loud* and the right one is *silent*.
3. **The `ties_available` branch, and this one has a measured cost.** The branch
   was registered, unimplemented, and then implemented with an off-by-one — a tie
   compared against `base_floor + window` rather than `base_floor`. The positive
   that caught it was chosen to fire *only* under the correct comparator; a
   positive built from an obviously-late cell would have fired either way and the
   off-by-one would have shipped.
4. **The counter-example, recorded so the lesson is not read as universal.** The
   availability probe's own controls already discriminate, and say why in prose
   written before this lesson existed: the negative's second limb requires movement
   in the *following* second, which a plain dependency probe cannot produce. A
   positive can be strong AND discriminating; the two properties are independent,
   and the failure is only in mistaking the first for the second.

**And the bound stands.** This was applied to the two runtime detector rows that
carry reported claims, and to the three controls above. Every other known positive
in the project is **unexamined, not confirmed.**

## TB-21, at length — and the reason its list cannot be completed

**The shape:** *a lesson stated in one file's prose that governs only that file.*
Not mechanically enumerable — finding it requires reading prose for insight rather
than matching a pattern — so no sweep is claimed and the exemption is recorded
rather than left as a silence.

**Four instances now known, up from two:**

1. **The B-6 control's** *"a negative that moves nothing anywhere is a probe
   testing itself"*, which preceded TB-19 by months and governed one control.
2. **TB-02's parsing lesson** — *"a docstring is a string constant, so it simply is
   not a reference, and there is nothing to exempt"* — which preceded D-V30A-51's
   repair by eight lessons. The citation checker learned it; its neighbour, the
   installability checker, did not, and was defeated by a docstring eight lessons
   later.
3. **The `mask` / `cell_mask` conversion.** The comment beside the integer branch
   already explained that the frame-level path is the special case of the
   per-column one. The prose was right and the line below it was not converted, so
   the knowledge governed the comment and not the code. *(D-V30A-53.)*
4. **`bar_duration`'s "carried forward at the final row"** — stated in three
   documents and implemented correctly, while the *ordering* the same sentence
   implies by the word "successive" was implemented nowhere. Part of a rule can be
   the part that governs. *(D-V30A-54.)*

**Why the list cannot be completed, stated rather than left implied.** Every
instance above was found the same way: by arriving at a conclusion from a different
direction and then noticing it was already written down. That is not a search
procedure — it requires having the insight first, which means the method can only
ever confirm instances and never bound them. **The count is a lower bound and
nothing else**, and it is recorded that way so a later reader does not mistake four
for four-of-four.
