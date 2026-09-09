# What the next pre-registration needs to declare that this one did not

**Forward-looking, and about a future registration rather than this one.** It
states nothing about how `PREREG.md` v30a is scored, adds nothing to it, and
changes nothing in it. Every item below was produced by an attempt to execute
this registration's acceptance gate, and each names the round and the disclosure
that produced it so a reader can go and disagree with the evidence.

**Why it exists.** The §6.2 archaeology cost about fifteen rounds and produced one
criterion that cannot be run. The findings underneath that are worth more than
the number they replaced, and they are perishable: they live in a ledger of
forty-one entries and in commit messages, where the next author would have to
already know what to look for. This is the short version, written while it is
fresh.

---

## 1. The correspondence between the ground-truth artifact's key and the scorer's unit

**Declared before any detector runs, and regenerable from declared inputs.**

This registration declares a ground-truth map whose cells are keyed
`(side, instrument, month, class)`, and a scoring machinery whose events are
keyed on a feature together with an affected output cohort. **Nothing declared
crosses between them.** The metric machinery intersects the labels' cohort
strings with identifiers the detector itself emitted, so the labels' cohort
component lives in the detector's own namespace — and no declared object is in
that namespace.

The gap is invisible from either side. Each half is complete and internally
consistent on its own terms; it is the join that does not exist, and a document
this careful would not think to look there.

**The consequence here:** the acceptance gate's criterion 3 cannot be executed.
Closing it after the detectors have run would mean authoring a correspondence by
someone who has seen how the detector behaves, which is what the withholding
clause exists to prevent.

*Produced by R186–R188; recorded at `D-V30A-28`; ruled at `D-V30A-40`.*

## 2. Which detector row each criterion is evaluated on, named explicitly

The coverage table enumerates eleven detector rows and closes itself. The
acceptance criteria adjudicate "runtime findings", and the chain from that phrase
to two specific rows runs through four sections — the tier section's boundary,
the metrics table's assignment of both runtime rows, the coverage section's
promotion-status property, and the kill criterion's naming of both combinations.
**It is derivable, and it was never stated.**

The identifier the machinery keys its records on appears in the registration zero
times.

**The consequence here:** eight rounds of field-level work went into an
instrument that is none of the eleven rows and that the criteria do not score —
including a repair, a pre-commitment frozen on it, and a two-hour run launched
against it.

**The rule that generalises, and it is cheap:** where a registration enumerates a
closed scope, the first question about any artifact is which row of that scope it
occupies — before what it does, before what it emits, before any question about
its fields. If the answer is *none*, that outranks everything downstream.

*Produced by R188 §3.1; recorded at `D-V30A-27` and `TB-08`.*

## 3. The scoring unit's identifier namespace, stated — not only the unit

The registration locks the scoring unit and does not say what space the
identifiers live in. That is not a detail: the machinery **intersects** the
labels' identifiers with the detector's, so two objects that agree on the unit
and disagree on the namespace do not meet.

The same registration defines a cohort in terms of output rows sharing a decision
time, while one instrument in this package emits cohorts that are columns of a
frame. Both are called cohorts. Only one of them is the registered notion, and
the tool's own module header said so from the day it was written — which nobody
read for eight rounds, because nobody was asking the question it answers.

*Produced by R187 §2.3; recorded at `D-V30A-26`.*

## 4. A pre-run executability check, actually run

The registration already asks that every declared object the gate consumes be
regenerable and checkable from the declared inputs alone, before any detector
runs. **What was missing was anyone executing that.**

The check is cheap and it is mechanical: take each declared object the gate
consumes, regenerate it from the declared inputs, and confirm the scorer can
consume it. Items 1 and 3 above would both have surfaced from it, years earlier
in project time and before any detector existed to be shaped by.

*Produced by the whole of R177–R188; the clause it enforces is already
registered.*

## 5. The ground-truth artifact's scope relative to the evaluation frame's columns

The declared map and the fixture manifest describe one column set; the frame the
criteria are evaluated on carries another and larger one. In this fixture,
twenty-one columns moved under the probe that appear in neither the required list
nor the clean list, because the built frame carries eighty-seven columns while
the manifest describes a thirty-five-column fed set.

Those columns enter no criterion. For them a correct detection and a false
positive are indistinguishable, so they are named in the output and left
unclassified — **they are never coverage and are never corroboration.** Whether
the ground-truth artifact's scope ought to reach them is a live question this
registration does not answer, and the next one can settle it in one sentence
either way.

*Produced by R190–R192; recorded at `D-V30A-32` and `D-V30A-34`.*

---

## 6. A display state for "not run, and would have passed" — §8.2's vocabulary has a case it cannot express

**What §8.2 requires.** Every non-finding outcome carries a state, and *none may
be displayed in a way mistakable for a pass*. The registered vocabulary is
`not_applicable`, `unsupported`, and `could_not_run(reason)`.

**The case it cannot express.** A check that is applicable, supported, and
deliberately **not run in the default configuration because running it is
expensive**. Four such tests exist in this project's own suite: the fixture
adapter's opt-in set, gated behind an environment variable for about five
minutes of rebuild. They are not `not_applicable` — the fixture's code is
present and they apply. They are not `unsupported` — they are supported and they
pass. They are not `could_not_run` — they can run, and do, on request.

**Why this is a registration finding and not a registration edit.** §8.2 is
registered vocabulary in a closed registration, and it is not amended for the
convenience of an artifact that discovered a gap in it. The gap is recorded here,
which is what this file is for, and the difference between recording it and
amending it is the difference between a closed registration and a convenient one.

**Why it matters beyond a test summary.** The rule that no outcome may be
displayed as a pass was written about detector outcomes, and there is no
principled reason it stops at the package boundary — the same argument applies to
the suite that certifies the package. A cost-deferred passing test and a
genuinely inapplicable one displayed in the same word is exactly the confusion
§8.2 exists to prevent, one level above where §8.2 was written.

**What a next registration would have to decide, and it is not obvious.** A
fourth state is one answer; another is that the third state's `reason` is
sufficient and the requirement is that the reason be *displayed* rather than
merely recorded. A third is that deferral is a property of a RUN rather than of
an outcome, and belongs in the run's description rather than in the outcome
vocabulary. This item registers the gap; it does not pick.

**What was done here instead, since the registration is closed.** The suite is a
tool artifact and not a registered detector, so it uses tool-level wording
without claiming registered vocabulary — the same route R203 settled for config
keys. Its summary now reads *"N deferred (opt-in), passing as of `<commit>`"*
with a content-keyed currency check behind the claim, rather than *"N skipped"*.
The wording is deliberately not one of §8.2's three words, so it cannot be
mistaken for one.

*Found by asking what four green-adjacent numbers in a suite line actually were.
The count had been reported unexamined in every round of Phase 2.*

## 7. What L2a needs and the registration does not determine — five, from R258's establish

**Produced by reading L2a's registered row before building it**, not by running
it. The argument for each is in `evidence/session/L2A_ESTABLISH.md`, which states
its structural population; these are the one-line forms so that the findings live
where they govern rather than only in a round report.

- **(i) How "labels built inside the pipeline" is established.** §4.2 makes L2a
  return `unsupported` naming L3.1 as covering detector in that case, and states
  no test for it. It is mechanically derivable — the declared label is absent
  from the raw frames and present in the built output — and the registration
  does not say so, so a builder must either invent the test or refuse.
- **(ii) The non-temporal path has no scoring unit.** §7.2's unit is *feature ×
  affected output cohort*; a cohort is the output rows sharing one decision time;
  the non-temporal path has no decision times. §7.2 does not say what replaces
  the cohort there, and §6.5 nonetheless requires non-temporal cases under both
  settings of §2.5's policy in the corpus.
- **(iii) §2.5 routes a supplied, valid value to `unsupported`.**
  `labels_available_during_feature_construction = true` is neither missing nor
  impossible, and §8.2's boundary sentence covers only missing or impossible
  inputs. The routing is registered in terms; the boundary sentence does not
  reach it. **Related to item 6 above:** both are §8.2 vocabulary that a real
  case falls outside of.
- **(iv) The cohort is defined in the design document, not the registration.**
  §2.6 and §7.2 use "cohort" as a settled term and neither defines it; the
  definition is `DESIGN.md` §2.3. **The registration's scoring unit therefore
  depends on a term the registration does not carry**, and `DESIGN.md` is not
  part of the registration.
- **(vi) A declaration supplied IN PART has no registered outcome.** §2.7 reads
  *"If the required declaration is neither supplied nor defaulted, L3.1, L2a, and
  L3.1b return `unsupported` (§8.2), naming the missing element."* It covers
  supplied and not-supplied, and a user who declares `label_availability` and
  omits the tool-level locator — or the reverse — is in neither state. **L2a
  refuses there**, on the ground that half a declaration is evidence the row was
  meant to run and a run that quietly skips it returns an audit that looks like
  the one the user asked for. That is a tool-level tightening, which R203
  permits, and it is recorded here because the registration does not reach the
  case rather than because it disagrees. **Related to item 6 and to (iii)
  above:** three distinct real cases now fall outside §8.2's vocabulary.
- **(v) §6.2's criteria adjudicate "runtime findings" and name no row.** This is
  **item 2 above**, recorded there from R188. It is repeated here only to note
  what makes it bite: with one runtime row built the phrase identifies a row by
  accident, and building the second makes criterion 1 satisfiable by either.

## 8. The attested set admits a file that binds nothing and excludes the file that binds the work

**The manifest's scope is the evidence tree**, and repository-root files enter
only through an enumerated `../` set, admitted by a limb of §11 item 8 as the
ceremony's commit set. `PRACTICES.md` is in it, described there as explicitly
non-normative — it binds nothing, no gate verdict depends on it — and listed *for
coverage, not for authority*. `OPERATING_RULES.md` is outside it, and it carries
the durable rules that govern how every artifact in the tree was produced.

**That is a coverage rule doing exactly what it says, and the result still reads
backwards**: a reader can verify that the non-binding practices file is the one
its pointers were written against, and cannot verify the same of the rule set.
The next registration decides whether the attested set is *what the ceremony
commits* or *what a reader needs to check a claim*, because those two are not the
same set and this one chose the first without the question being put.

*Not acted on in this tree: a seventh `../` entry touches the ceremony's own set
and the frozen checker's counts sit on it. Git history is the rules file's
attestation meanwhile. Recorded at R261 §6.*

## Two habits, not requirements, that paid for themselves

**Predict before measuring, including the boring things.** Every regeneration of
the evidence manifest in the last twenty rounds was predicted first. It caught a
staging gap that would otherwise have been invisible — a prediction of four
appended lines against an actual zero, because the population being regenerated
is tracked files and the new ones were unstaged.

**A cost model fitted at one point cannot see which term it omitted.** At a single
point every term is confounded with every other. One such model interpolated its
own fitting point to within four per cent and missed the population by a factor
of 2.35, and the quality of the interpolation read as evidence for the model. A
model built from one measured point per unit of the population came in at 0.95,
1.05 and 0.96 on its three terms.

*Recorded at `D-V30A-37` and `TB-10`.*

---

## And the one that is about the process rather than the protocol

**Claims that could be unfavourable were verified; claims that flatter the
process were accepted.**

In this project every claim that could have embarrassed the record was checked
hard — an instrument change that reverted, the provenance of a set of
dispositions, the correspondence gap, the detector allocation. The one claim
nobody examined was the one that could only make the record look good: an
assertion that a cost forecast had been "right about where it was unreliable",
written in the same act that committed the file refuting it.

The asymmetry is the most dangerous one available, because it silently inflates a
record and because nothing in a review process is motivated to catch it. An
adversarial reviewer attacks what would embarrass the author; nobody is assigned
to attack what pleases everyone.

**What follows in practice:** a claim about the method's own performance carries
the same evidence standard as any other and in practice a higher one; a
favourable self-assessment is checked against the artifact before it is repeated;
and a prediction is assessed term by term from the measured output, never against
its total.

*Recorded at `TB-11`.*


---

## A frozen check whose PASS prints "this is not a pass"

*Recorded at R248 §2. Not repaired here, deliberately.*

`round_reconciliation` reads its population from `LEAKAUDIT_WORK_ROOT`. With the
variable unset it reconciles nothing and emits:

> *COVERAGE IS ZERO: LEAKAUDIT_WORK_ROOT is unset, so no working directory was
> reconciled. **This is not a pass.***

**And then returns PASS**, because that finding is emitted as a NOTE and a note
does not fail a check. **The verdict and the message contradict each other**, and
the verdict is what gates, so the message is advice a runner reads after already
having their answer.

**THE COST OF THE CONTRADICTION, MEASURED.** Every gate result reported across an
entire session ran without the variable. The check was zeroed each time and each
time reported PASS, and the reported figure — *"23 of 24 checks pass"* — was
produced by a command that had silently emptied one check's population. The
instrument was working the whole time; it fails when given its population.

**WHY IT IS NOT FIXED NOW.** The verdict lives in `tools/check_registration.py`,
which is verdict-frozen against the tagged instrument: every difference is ruled
against a ceiling of four, currently at two, and R223 §1 fixed that ceiling
before there was pressure on it. Changing a check's verdict spends a slot on
something a sibling makes unreachable — `tools/certify_preconditions.py` refuses
certification when the variable is unset, so the contradicting branch is never
entered.

**WHAT THE NEXT REGISTRATION IS ASKED TO DO.** Make the verdict match the
message at the source: a check that cannot see its population reports
`could_not_run`, never `PASS`. `PREREG.md` §8.2 already says an empty population
is reported as `could_not_run` rather than as a result; this is that rule applied
to the checker itself, which is the one place it was not.

**THE GENERAL FORM, worth more than the instance.** A check has three outcomes,
not two: it looked and found nothing, it looked and found something, and **it
could not look**. Collapsing the third into the first is the same defect this
tool exists to find in other people's pipelines — `observed_silence` where the
honest answer is `none`.


---

## The work root now contains harness infrastructure, and certifying grows it

*Recorded at R248 §4. Not repaired here.*

R248 widened the declared work root from the session's `scratchpad/`
subdirectory to the session directory, because 49 files of round work sat above
the narrower root and never entered the reconciliation's population. That was the
right widening for the work; it also pulled in `tasks/`, the harness's
background-command log directory.

**`tasks/` is not round work.** It is infrastructure the harness writes, in the
same category as `.claude/` -- present in the directory, not produced by the
round. **And it grows when certification runs**: each backgrounded command leaves
a log, so `round_reconciliation` reports a new file immediately after the very
sequence that was supposed to end clean. The increment is self-referential, and
accepting it creates the next one.

**Why it is not fixed now.** The exclusion belongs in the `_EPHEMERAL` list
inside `tools/check_registration.py`, which is verdict-frozen with a ceiling of
four ruled differences, currently at two. `tools/clean_tree.py` solved the same
problem inside its own scope with an `IGNORED_PREFIXES` constant, because it is a
sibling and free to; the reconciliation's equivalent is in the frozen file.

**What the next registration is asked to do.** Give the reconciliation an
infrastructure exclusion -- `tasks/` and anything else the harness owns -- so its
population is the round's work rather than the directory's contents. Until then
each such file is accepted into the baseline, which records that it was reported
and read and asserts nothing about whether it belongs.

**The narrower reading to resist.** "Set the root back to `scratchpad/`" removes
the log noise and puts the 49 work files back outside the population, which is
the defect this widening fixed. The infrastructure is the thing to exclude, not
the work.
