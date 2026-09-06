# The fork's answer vocabulary — its cases, reported before any word is fixed

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures.

**The ask.** R235 §2(a): report the distinctions the vocabulary must carry
**before** fixing its words, as `align_key`'s cases and the label screen's
threshold cases were reported. **No word is chosen in this file.**

**The rule that decides the shape**, and it is tighter than "document it":

> **The fork `draft` states and the answers `accept()` takes are one contract,
> and they must be the same set of options.** A user reads a fork with named
> branches and must be able to express exactly those branches back, in the words
> the fork used.

That is the figure-and-its-frame rule applied to a question and its reply.

---

## What exists today, in both halves

**The fork text**, per frame with one datetime column:

> *THE FORK, AND ONLY YOU CAN TAKE IT: if this frame **AGGREGATES an interval**,
> `aggregate_frames[f] = k` fits and its cells become knowable at floor(key) +
> window. If it carries the **DECISION INSTANT** — the clock your output rows are
> built on — it is not an aggregate at all and belongs in `decision_column`
> instead. The two look identical here.*

**The answers `accept()` takes:** `"aggregate:<col>"`, and anything else — which
falls through to *not an aggregate*.

**They have already diverged.** The fork names **two** branches and `accept()`
recognises **one string plus a fallthrough**, so *"decision instant"* and
*"neither of those"* are the same answer to the code and different answers in the
prose. **A user cannot express, in the words the fork used, the difference between
"this is my decision frame" and "this is neither".**

---

## The cases — how many fork outcomes are there really?

Enumerated from what a frame can actually be, with the observable that would make
each arise.

| # | the case | what it means for availability | can a user produce it? |
|---|---|---|---|
| 1 | **aggregates an interval** keyed on column *k* | cells knowable at `floor(k) + window` | **yes** — the fixture's `magg` and `trades`, and the `scans` frame in every walk |
| 2 | **carries the decision instant** | not an aggregate at all; it is the clock others are compared against | **yes** — the station frame, which is what made R234 §0 a defect |
| 3 | **neither: a source frame read at its own stamp** | cells knowable at the stamp; `at_timestamp`, no frame-level aggregate entry | **yes** — a tick frame joined on event time. Distinct from 2 because it is *not* the decision clock, and distinct from 1 because there is no window |
| 4 | **neither: no time semantics at all** | a reference or dimension table; availability is `always`, or the frame is out of scope | **yes** — the `tick_size`/`country_code` shape already in the draft's own tests |
| 5 | **more than one candidate clock**, no basis to choose | unresolved; the user names which column, then one of 1–4 | **yes** — `ts_recv` beside `ts_event`, S3's wrong case, live in the fixture |

**Five cases. Two are expressible today; three are not.**

**Case 3 is the one that matters most and is missing from both halves.** The fork
text says *"aggregate, or decision instant"* and offers no third branch — so a
user with a tick frame read at its own stamp is told to pick between two things
neither of which is true. **The fork itself has a missing case**, which is a
defect in the question rather than in the answer space, and it is the one that
would have been papered over by fixing only `accept()`'s words.

**Case 4 is expressible by silence and that is not the same as expressible.**
Leaving a frame out of `aggregate_frames` produces the right *behaviour*, and the
user cannot say *why* — so a reader of the finished file cannot tell "not an
aggregate, deliberately" from "nobody got to it".

**Case 5 is already handled correctly** in the draft's `unresolved` list, and is
included here because a vocabulary that cannot express it would regress it.

---

## What the enumeration says about the vocabulary's shape

**A single string per frame cannot carry cases 1 and 5 together.** Case 1 needs a
column name; case 5 needs a column name *chosen from several* and then a case.
Any settled vocabulary is at least `(case, column?)`, not a bare token — which is
the same shape `column_modes` already uses for `at_source_timestamp`, where the
mode and the column it names travel together.

**No case here is one nobody can produce.** R235 §2(a) warns against a vocabulary
with a case nobody can produce; each of the five is named with a frame this
project has actually handled.

**And the reverse check is the one that failed:** the fork states two cases and
the world has five. **A vocabulary missing a case the fork states is a defect; a
fork missing a case the world has is a bigger one.**

---

## What is NOT decided here

**No words.** R235 §2's order is cases first, generation-or-testing second,
documentation third — and picking the tokens now is the "ad hoc string becomes a
contract by inertia" failure the section exists to prevent.

**Whether the fork text and `accept()` are generated from one source or tested
against each other.** §2(b) requires one of the two; which is a design question
that follows from the settled cases, and the cases are what this file delivers.

**Whether case 3 belongs in the frame-level fork at all**, or is properly a
per-column `column_modes` answer with no frame-level entry. That is the first
question the settled vocabulary has to answer, and it is not answered here.
