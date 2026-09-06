> **Reader's note.** This file describes a defect class — *a document about a
> defect class exhibits that class* — which by its own subject makes it a
> candidate. Its check on itself is the last row of the table below, and it was
> run like the others.

# The eight documents, each checked against its own subject

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures.

**The ask.** R233 §4, promised to open R234, and executed here after §0 and §1's
live defect: **eight documents that describe a defect class, each checked against
that class, concretely.** Not a judgment — a specific check, with `found`, `clean`
or `not mechanically checkable` and the reason.

**Why it waited a round, and why waiting was the point.** TB-25's reason for
deferring was exact: *a sweep in the same breath as the listing is the same act of
attention and inherits the same blind spot.* So this is a different act — reading
each file as somebody hunting the defect, not as the author who is sure it is
absent.

---

## The sweep

| # | document | the class it describes | the concrete check | result |
|---|---|---|---|---|
| 1 | `OPERATING_RULES.md` | durable rules that get dropped when nobody carries them; provenance for each | does its own self-description cover its own rows? Its scope section says the file is *"the fourteen rules a mechanical extraction across R119–R220 found"* — count the rows whose `first stated` is later than R220 | **FOUND.** Three rows are from R226, R227 and R229 and are from no such extraction. The document about rule provenance had stale provenance about itself. **D-V30A-71** |
| 2 | `COST_FIGURES_SWEEP.md` | durations from stopped runs quoted as costs | does it quote any duration of its own without saying whether that run finished? Every duration in the file, in the table and in prose | **CLEAN.** 4 table rows carry durations, every one with a completed/stopped column; **0 durations appear in prose outside the table** |
| 3 | `GUARD_COST_CRITERION.md` | thresholds chosen after the number they bound is read | was its own limit set before or after? | **CLEAN, and deliberately so.** Its first section is headed *"this is stated AFTER the measurement, and that is a defect in the ordering"* — it discloses its own instance rather than exhibiting it silently |
| 4 | `LABEL_SCREEN_CASES.md` | screens whose bounds go unstated | does it state its own screen's bounds — seed, row count, statistic, blind spot? | **CLEAN.** Seed, 2,000 rows, interpreter and dependency versions on the R231 table; the non-monotone blind spot and the single-column bound both stated. *(Its earlier table names no interpreter — it predates the R226 rule, and a dated measurement is not rewritten.)* |
| 5 | `WORK_ROOT_RESIDUE.md` | populations declared by count rather than by content | does it describe its own population or only count it? | **CLEAN.** A 9-row table of classes with what each *is*; the title is *"what they are"* |
| 6 | `PRACTICES.md` | practices that bind nothing | does it say that it binds nothing? | **CLEAN.** Line 5: *"This file binds nothing."* |
| 7 | `DEVIATIONS.md` + its applier | disclosed defects; the file is append-only | does the applier ever rewrite? Read every write in `append_disclosure.py` | **CLEAN.** One write, `existing.rstrip + fragment`; the existing text is read and never parsed, edited or reordered |
| 8 | `probe_path_guard.py` / `PROBE_PATH_SET.json` | populations that are a function of which runs measured them | does it name the runs its own path set came from? | **CLEAN.** `runs` records three, each described — A the whole-frame path, B the per-column path, C the reported-figures path |
| — | **this file** | *a document about a defect class exhibits that class* | does it? Its subject is the check-your-own-document rule; it applies it to itself in this row, and its counts (8 checked, 1 found) are stated rather than left implied | **CLEAN as of this writing**, and it is the most likely of the eight to go stale — its table is a hand-typed set of results, which is #4 on `HAND_TYPED_FIGURES.md`'s open list |

**Eight checked. One found. Seven clean, each with the specific check named
rather than a verdict.**

---

## What the result means, and what it does not

**A 1-in-8 rate is not a refutation of TB-25.** The four instances that produced
the lesson were found by accident, over five rounds, one at a time — this sweep
looked at eight documents in one pass with the class in mind, which is a much
easier condition. The honest reading is that **deliberate checking is cheap and
finds things**, not that the class was overstated.

**And three of the eight were clean because somebody had already been bitten.**
`GUARD_COST_CRITERION.md` opens by disclosing its own ordering defect;
`PRACTICES.md` states that it binds nothing in its fifth line;
`WORK_ROOT_RESIDUE.md` is titled *"what they are"* because R224 refused a count.
Those are not accidents of good writing — each is a repair from a round where the
class had just bitten somewhere else.

**The one found is small and is the kind §2 permits fixing:** a stale figure in a
scope sentence. It is corrected in the same commit and disclosed.

## THE AXIS THIS SWEEP COVERED

**A sweep result carries the axis it swept**, exactly as a count carries its
invocation and an absence claim its population. *"The eight documents were swept"*
is the sentence that will be quoted, and it claims a whole matrix. The true
sentence is narrower.

> **THE DIAGONAL ONLY.** Each document was checked against **the class it names**.
> Eight documents × one class each = **eight checks**, of a matrix that is eight
> documents × the enumerable class list.

**THE OFF-DIAGONAL IS NOT SWEPT** — a document checked against a class it does
*not* describe. `COST_FIGURES_SWEEP.md` was checked for stopped-run figures and
not for hand-typed ones; `PRACTICES.md` was checked for binding and not for stale
provenance; and so on for all eight.

**It is not swept deliberately, and R215 §2 is why: the case for the work starts
from a demonstrated need.** Every measured instance of this class — the four that
produced TB-25 and the one this sweep found — has been a document exhibiting **its
own** class. Not one has been a document exhibiting a class it does not name.
Sweeping a matrix on the strength of a shape nobody has observed is the work this
project declines everywhere else.

**THE TRIGGER THAT OPENS IT**, recorded so the gap is bounded rather than open:
**the first instance of a document exhibiting a class it does not describe.** One
such instance turns the off-diagonal from speculation into a population with a
reason, and the sweep above becomes the template for it.

**So the honest status is "unexamined on a named axis, with the trigger
recorded"** — not "unexamined, not clean", which says less, and not "swept",
which says more.

**Three documents are outside this table entirely.** `TRACKB_LESSONS.md`,
`ROUND_STATE.md` and `HAND_TYPED_FIGURES.md` had their instances found and
recorded before the sweep; they are **not re-cleared here**, on the diagonal or
anywhere else.
