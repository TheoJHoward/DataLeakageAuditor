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
