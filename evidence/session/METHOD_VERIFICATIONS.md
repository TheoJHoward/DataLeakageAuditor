# Method verifications — measured, not assumed

A method assumption behind a published number is not verified by having been
believed for a long time. This file records the ones that have been MEASURED,
with the population, the direction and the magnitude, so that "we checked" is a
citation rather than a memory. An assumption absent from this file is not
thereby false; it is UNVERIFIED, which is a different word from clean and is the
distinction the tool itself exists to preserve.

Nothing here is a PREREG.md §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures.

---

## MV-1 — the frame-key-plus-window path against the declaration, per column

**Asked (DELTA R206 §1):** Phase 1's entire evidence base was produced through
the frame-level availability path. Does `AVAILABILITY_DECLARATION.md` declare,
for any column of the fixture's frames, an availability rule that the
frame-key-plus-window path computes differently? Criterion 1's zero misses is
the result an over-reporting probe would also produce, so the question is not
answerable from the result.

**Measured on** `zc 2025-01`, the acceptance fixture instrument-month, captured
through `fixture_adapter.read_inputs` — definitionally the frames the builder
reads. Configuration as Phase 1 ran it:
`aggregate_frames = {"magg": "ts_floor", "trades": "ts_event"}`,
`window = 1s`, `decision_column = snap.timestamp` (naive).

**Population, stated twice because the two are not the same set.**

- **P1 — the columns the probe actually perturbs: 16.** `magg`, 464,199 rows,
  5 numeric columns of 6 (`bid_adds`, `ask_adds`, `bid_cancels`, `ask_cancels`,
  `total_events`; `ts_floor` is the key). `trades`, 397,457 rows, 11 numeric
  columns of 17 (`rtype`, `publisher_id`, `instrument_id`, `price`, `size`,
  `channel_id`, `order_id`, `flags`, `ts_in_delta`, `sequence`,
  `is_buy_aggressor`). The raw MBO parquet is captured and deliberately outside
  the probe surface, and `snap` is not a declared aggregate frame.
- **P2 — the columns the declaration enumerates by heading:** §4's `column_roles`
  table over the Phase 5 45-column set, the T2 addendum's nine Phase-7-added
  columns, and §C.1(A)/(B)/(C)'s trade- and MBO-derived families. These are BUILT
  feature columns, downstream of P1. The declaration names none of `ts_event`,
  `rtype`, `publisher_id`, `instrument_id`, `channel_id`, `order_id`,
  `ts_in_delta`, `sequence` or `is_buy_aggressor` anywhere.

P1 and P2 are disjoint as name sets. The declaration nonetheless governs P1,
because §3 and §C.1 declare the JOIN MECHANISM every P1 column reaches a feature
through, not a per-name rule — see the fourth finding below.

**Answer: NO column of P1 differs.** VERIFIED, not assumed. Per column:

| frame | columns | declared instant (§3, §C.1) | what the path computes | differs |
|---|---|---|---|---|
| `magg` | all 5 | `floor(T) + 1s` | `floor(ts_floor) + 1s` | no |
| `trades` | all 11 | `floor(T) + 1s` | `floor(ts_event) + 1s` | no |

**The four measurements the answer rests on.**

1. **`magg.ts_floor` is already floored — 464,199 of 464,199 rows on a
   wall-clock-second boundary, 100.0000%, zero exceptions.** So for that frame
   `key + window` and `floor(key) + window` are the same number and no reading
   of the path can distinguish them.

2. **`trades.ts_event` is not — 49 of 397,457 rows on a boundary, 0.0123%.**
   The sub-second offset has median 467.83 ms and maximum 999.999 ms. This is
   the frame where the two readings of the path are separable, and it is the one
   the fixture actually carries.

3. **The path as it RUNS floors.** `run_probe_a` selects cells with
   `key.dt.floor("s").isin(picked_seconds)` — the instant `floor(key) + window`.
   It does not compute `key + window`. That matches the declaration for both
   frames.

4. **Nothing bypasses the second-floor aggregate.** Every trade cell reaches a
   feature through `groupby("ts_floor")` at `phase5_ml_fixture.py` line 240,
   whose key is `trades["ts_event"].dt.floor("1s")` (line 233), merged at line
   251. There is no path from a raw trade column to a built feature that skips
   it. So `floor(ts_event) + 1s` is the availability instant of every P1 trades
   column as fed, which is what §C's post-lag framing requires and what §C.1's
   "every column built from those merged aggregates inherits the violation"
   states.

**What the read found that it was not looking for, recorded as D-V30A-43.**
`AvailabilityModel`'s own docstring says the declared availability instant is
`key + window`. That is not the arithmetic that runs, and on `trades` it is
LATER than the running instant on 397,408 of 397,457 rows — 99.9877% — by a
median of 467.83 ms, never earlier. The running rule is the declared one, so no
recorded number moves; the docstring is the artifact that is wrong. Had this
verification been answered by reading the docstring instead of measuring, it
would have returned the opposite answer on eleven columns.

**Bearing on the open timezone question (D-V30A-42).** The fixture builder's own
rule for `trades.ts_event` is `tz_localize(None)` at `phase5_ml_fixture.py` line
231 — it DROPS the zone. The probe's inline rule is
`tz_convert("UTC").tz_localize(None)`. On the fixture's actual dtype,
`datetime64[ns, UTC]`, those two are the same operation, verified on both
endpoints of the fixture's range; on a non-UTC zone they diverge by the offset.
So on this fixture the probe agrees with the pipeline it is auditing, and it is
`align_key`'s refusal that stands apart from both. That narrows the open
question without answering it: what the fixture licenses is not what an
arbitrary user's frames would.

**Not measured, and therefore not claimed.** This is `zc 2025-01` only. The
100%-floored property of `magg.ts_floor` and the 0.0123%-floored property of
`trades.ts_event` are facts about this instrument-month's captured frames, not
about all 48. The population run's eligibility counts are consistent with the
same structure elsewhere, but consistency is not the measurement and the other
47 were not read.

> **SUPERSEDED BY MV-2, and left standing rather than edited.** The paragraph
> above was correct when written and is no longer the state of the evidence. The
> other 47 have now been read. What it says about scope is retained because the
> useful part of this file is the record of what was known when, and a scope
> caveat that is quietly deleted once it becomes inconvenient teaches the reader
> that caveats here are provisional. MV-2 states the extension.

---

## MV-2 — MV-1 extended to the whole declared population, 48 of 48

**Asked (DELTA R207 §4):** an absence claim over one instrument-month, when 48
are on disk and the check is a parquet read, is the population problem this
project exists to notice. MV-1 was honest about its scope; the scope was a
choice, not a cost.

**Measured** on all 48 declared instrument-months — 8 instruments
(`cl es gc he le nq zc zs`) × 6 months (`2025-01`, `2025-08` … `2025-12`) —
by reading ONE COLUMN per file. No probe run, no build, no capture. **8 seconds
for the whole population**, against roughly 245 s per instrument-month for a
capture-and-probe, which is the measurement behind calling it cheap.

`magg` is not a file, so it is handled by the three-way branch in
`load_mbo_aggregated` rather than by a data read, and all three branch
conditions are measured: the cached-aggregate file's existence, the source
file's existence, and the source row count. Two of the three code paths derive
`ts_floor` by flooring (ns integer truncation above 50M rows, `.dt.floor("1s")`
below) and cannot emit an unfloored key. The third reads a **cached** aggregate
and takes its `ts_floor` as-is — that is the only path on which the property
could fail, so its file was checked for all 48.

### The answer: MV-1's properties hold across the whole population

| property | zc 2025-01 | all 48 |
|---|---|---|
| `trades.ts_event` zone | UTC | **UTC, 48 of 48** |
| `snap.timestamp` zone | naive | **naive, 48 of 48** |
| `trades.ts_event` on a second boundary | 0.0123% | **max 0.0188%** (`he 2025-12`), min 0.0002% |
| `trades.ts_event` median sub-second offset | 467.83 ms | **440.26 – 486.69 ms** |
| cached-aggregate file present | no | **0 of 48** |
| months where `trades.ts_event` is mostly floored | 0 | **0** |

So no instrument-month's declared key is floored where `zc 2025-01`'s is not, or
the reverse. The frame-key-plus-window verification of MV-1 stands over the
population, not over one month of it.

**And the mixed-zone case is universal, not a fixture quirk.** An aware
`trades.ts_event` against naive `snap.timestamp` holds in **all 48**. D-V30A-42's
open question is therefore not about one file: whichever timezone rule is right
is right for every number this project has published.

### Two things the sweep turned up that one month could not show

**(1) Six instrument-months have no MBO source at all — every `nq` month.**
`nq 2025-01`, `-08`, `-09`, `-10`, `-11`, `-12` have snapshots and trades on disk
and no `nq_mbo_<month>.parquet`, so `load_mbo_aggregated` returns `None`, `magg`
is absent from `raw`, and five of the sixteen probed columns do not exist to be
perturbed.

**The recorded evidence already carries this, and correctly.** The committed
population run holds `frames_absent: ["magg"]` on exactly those six, and 12
probe notes — one per side — reading *"aggregate frame 'magg' absent from raw;
not corrupted"*. The effect is visible in the results: `nq 2025-01` contaminated
attributes findings to **13** features against `zc 2025-01`'s **29**, the
difference being the MBO-derived family that could not be reached. This is the
`none`-versus-`observed_silence` distinction doing its job on real data, unasked.

**And criterion 1 is structurally untouched by it.** All eleven required units
are governed by `trades_all`, `trades_sell` or `trades_large`; **no `mbo_*` class
appears in the denominator at all**. `nq`'s scored contexts return the same
8 satisfied / 3 unsupported split as every other instrument-month. Across the
whole population: **528 satisfied, 198 unsupported, 0 missed** over 726 unit
contexts. The 198 are the three Phase-7-only columns absent from the Phase 5
built frame, declared unsupported under §8.2 rather than passed.

**(2) The decision column's second-boundary fraction spans nearly the whole
range, and the fixture is not near either end.** `snap.timestamp` sits exactly on
a wall-clock second for between **0.000000** (`es 2025-01`, `es 2025-08`,
`gc 2025-12`, three `nq` months — zero rows of 1.6–1.9 million) and **0.862450**
(`he 2025-12`, 310,475 of 359,992). The acceptance fixture, `zc 2025-01`, sits at
**0.345640**.

That is a five-order-of-magnitude spread in a property of the decision lattice
across the population whose sides Phase 1 scored. **What it does to any scored
quantity is NOT measured here and is not claimed.** It is recorded because it is
the kind of population variation a single-instrument-month verification is
constitutionally unable to see, and because §C.2's cohort predicate reads the
same column.

**Not measured, and therefore not claimed.** Whether the boundary-fraction spread
moves the cohort predicate's coverage, the overhang magnitude, or any scored
count. Whether the six `nq` months' `magg` absence changes criterion 2 or 3
(criterion 1 is shown untouched; the others were not examined). And this is the
declared 48 — the wider set of instrument-months on disk was not read.

---

## MV-3 — does `timestamp_semantics` cover timezone handling? A structural read

**Asked (DELTA R207 §3):** a declare-or-refuse shape for the open timezone
question needs a declaration key to hang on. `timestamp_semantics` is the
candidate, on the reading that "ts[j] is read under the declared
`timestamp_semantics`, which every mode inherits." Before wiring a refusal, does
that key's registered definition actually cover zone handling?

**Population of the read: the whole registration.** `PREREG.md`, 2,228 lines, at
the working copy. Not a section, not a table — the file. Both directions are
enumerated: every occurrence of the key, and every occurrence of any vocabulary
that would carry the concept if it were registered anywhere else.

**Occurrences of `timestamp_semantics`: exactly one, at line 251**, a row of the
`AvailabilityModel` element table, reading in full:

> whether the timestamp column is observation, event, or availability time, plus
> the mapping if not the last

**Occurrences of zone vocabulary in the registration: none.** Case-insensitive,
whole file:

| term | hits | what they are |
|---|---|---|
| `timezone`, `time zone`, `tzinfo`, `tz_convert`, `tz_localize`, `naive`, `wall-clock`, `wall clock` | **0** | — |
| `UTC` | 38 | **all 38 are inside "outcome"/"outcomes"** — 35 and 3. Zero are the zone. |
| `aware` | 3 | all "tier-aware" (§7.7 termination). Zero are timezone-aware. |
| `offset` | 1 | `decision_time`'s "bar open, bar close, offset, or a column" — a time offset from a bar, not a UTC offset. |

### Answer: NO. `timestamp_semantics` does not cover zone handling — R207 §3's second branch.

**What it does cover, exactly, and nothing beyond it.** A *kind* question about
what a stamp MEANS: is this column recording when a thing was observed, when it
happened, or when it became knowable — and if it is not the last, how to map to
the last. That is a question about the semantics of the quantity. A timezone is a
question about the REPRESENTATION of the quantity: two columns with identical
`timestamp_semantics` — both availability time, no mapping needed — can still be
one aware and one naive, which is precisely the case the acceptance fixture
carries in all 48 of its instrument-months (MV-2). The key cannot distinguish
them because it was never asked to.

**Consequence, and it is a refusal to act rather than an action.** `align_key` is
NOT wired into `run_probe_a` this round. The declare-or-refuse shape may well be
right — the argument for it is sound and is recorded in R207 §3: a probe that
converts where the pipeline drops is auditing a different pipeline, and it cannot
learn which from the build callable alone. But that shape needs a declaration key
to refuse *against*, and the registered vocabulary does not contain one. Wiring a
refusal whose licence is unestablished would put the tool in the position of
demanding a declaration the registration never defined.

**Two notes on line numbers, stated because this file is cited.** (i) The
declaration's §4 cites `column_roles` at "PREREG.md line 205" and this read finds
it at 252; `AVAILABILITY_DECLARATION.md`'s own opening section on which
registration version a line reference means is the governing note, and the
citation is to content, not to a line. (ii) **The read is of the tagged text.**
`git diff prereg-v30a -- PREREG.md` is empty: the working copy is byte-identical
to the registration at the tag, so the line numbers and the zero counts above are
statements about the registered document and not only about a working file.

**Not measured, and therefore not claimed.** Whether some OTHER registered
element covers zone handling was searched for by vocabulary and not by reading
every element's definition in full — the vocabulary sweep returning zero across
the whole file is the evidence, and it is a strong absence rather than a proof.
Whether a new key is warranted, and what it would be called, is not decided here.

---

## MV-4 — does `AVAILABILITY_MODES.md` over-claim what `timestamp_semantics` does?

**Asked (DELTA R208 §2):** MV-3 established that `timestamp_semantics` carries no
zone meaning. The modes document, written days earlier, is remembered as saying
"`ts[j]` is read under the declared `timestamp_semantics`, which every mode
inherits." If so it attributes to that key something the key does not do, and
would be a fourth instance of the description-versus-fact class.

**Population: the whole document.** `AVAILABILITY_MODES.md`, 140 lines. Every
occurrence of the key, and a vocabulary sweep for anything that would carry the
zone concept.

**Occurrences of `timestamp_semantics`: exactly one, at line 27.** Quoted in
full, with the clause the remembered version omits:

> `ts[j]` below means row *j*'s value in the frame's timestamp column, read under
> the declared `timestamp_semantics` — **whether that column holds observation,
> event, or availability time is itself declared** (`PREREG.md` §2.3), and every
> mode below inherits whatever that declaration says.

### Answer: NOT a fourth instance. The sentence is accurate, and it is accurate because it restricts itself in its own clause.

The em-dash clause spells out what `timestamp_semantics` means — *"whether that
column holds observation, event, or availability time"* — which is the
registration's definition in substance, and the same three-way distinction MV-3
read at `PREREG.md` line 251. It claims the modes inherit **that** declaration,
which they do. It does not claim the key covers anything else.

**The citation is also correct.** `PREREG.md` §2.3 spans lines 233–264 and
contains both the comparator and the `AvailabilityModel` element table in which
`timestamp_semantics` is defined. §2.4 begins at 265.

**Zone vocabulary in the modes document: zero.** `timezone`, `time zone`, `tz_`,
`naive`, `aware`, `UTC`, `zone`, `offset` — no hits, in 140 lines.

**What is true instead, and it is a silence rather than an error.** The document
fixes `a(j, c)` per mode and explicitly leaves the comparator to `PREREG.md` §2.3.
It therefore never addresses what happens when the frame's timestamp column and
the decision column are in different representations — which is the case the
acceptance fixture carries in all 48 instrument-months (MV-2). That is an
unstated precondition, not a false statement, and it is exactly the gap R208 §1's
tool-level key would fill. **It is reported and not resolved by editing the
document**, because the document was written before the parser deliberately and
amending it to cover a question the registration does not carry would make it
something other than the mapping it was written as.

**Not measured, and therefore not claimed.** Whether any OTHER sentence in the
modes document over-claims about some other registered key — only
`timestamp_semantics` was audited, because only it was asked about.

---

## MV-5 — what a tool-level zone key would have to distinguish, and how many cases that is

**Asked (DELTA R208 §1):** before building such a key, report what it would have
to distinguish — *convert then drop*, *drop the zone*, *require naive throughout*
— and whether those are three cases or two. A value nobody can produce data for
is the `at_source_timestamp` / `explicit` situation again, where the honest
answer was to say so.

**Population: the full cross-product of representations, both directions.** The
probe compares a frame KEY against a DECISION column and either side can carry a
zone, so a key that handled only the fixture's direction would have a hole in it.
Four representations — naive, UTC, US/Central, Asia/Tokyo — on each side, **16
combinations**, one instant carried through both rules.

### Result: `convert` and `drop` disagree on 8 of the 16.

**Every one of the eight carries a non-UTC zone on at least one side.** With
zones drawn only from {naive, UTC}, the two rules are the same rule.

| key tz | decision tz | convert | drop |
|---|---|---|---|
| UTC | US/Central | 0 | +6h |
| UTC | Asia/Tokyo | 0 | −9h |
| US/Central | naive | 0 | −6h |
| US/Central | UTC | 0 | −6h |
| US/Central | Asia/Tokyo | 0 | −15h |
| Asia/Tokyo | naive | 0 | +9h |
| Asia/Tokyo | UTC | 0 | +9h |
| Asia/Tokyo | US/Central | 0 | +15h |

**The fixture's own shape is in the AGREE set.** `key = UTC, decision = naive` —
what all 48 instrument-months carry (MV-2) — is a row where the two rules give
the same answer. That is MV-1's dtype measurement recovered from the general
table instead of from one file, and it settles something that has been open
since D-V30A-42.

### So: two answers and one refusal, on a different axis than the one named

**It is NOT the `at_source_timestamp` / `explicit` situation.** There, two modes
computed the same number on every possible input and no data could separate
them. Here data separates them on half the table. But the separating data is not
the fixture's, and not any user's whose aware columns are all UTC — which is what
parquet with `isAdjustedToUTC=true` yields, the ordinary case.

**And the three names are the wrong axis.** `convert` and `drop` are not two
policies about aware columns. They are two answers to one question about **naive**
ones:

- **convert** — a naive column is UTC wall-clock.
- **drop** — a naive column is local wall-clock, in whatever zone its aware
  neighbour carries.

Once that is the question, *require naive throughout* is not a third value of the
same key. It is a **refusal to answer it** — the right default, because both
other answers silently produce a defensible-looking number from data that
licenses neither.

### The consequence for `align_key`, stated because it is now measurable

`align_key` refuses exactly the `aware key / naive decision` case. That is the
row where **no rule is needed** — the two candidate rules agree there. So it
refuses the one configuration it did not have to, and would pass every
combination that actually separates them, since it only inspects whether exactly
one side carries a zone rather than which zone.

That is why it is right in principle and wrong here, and the sentence can now be
made precise: **the trigger should be the presence of a non-UTC zone, not the
asymmetry of zone-carrying.** Under that trigger the fixture passes without a
declaration, and a user with local-time data is asked one question.

**Not measured, and therefore not claimed.** Whether the key is worth building,
what it would be called, or whether the refusal belongs at load or at the probe
path. Whether any zone pair outside these four behaves differently — the four
were chosen to span naive, UTC, a negative offset and a positive one, and DST
transitions were not exercised at all.

---

## MV-6 — portability UPWARD, on a dependency set no test had seen

**Asked (DELTA R209 §2):** the definition-of-done walk's clean virtual
environment resolved to newer dependencies than the development machine. That is
an accidental portability test sitting there for free; make it deliberate.

**THE HEADING SAYS UPWARD AND THE HEADING IS THE QUALIFICATION.** This measures
the tool against dependencies **newer** than the ones it was written on. It says
**nothing whatever** about the declared floors, and reporting it as though it did
would be the figure-without-its-frame failure this file exists to prevent.

### The two dependency sets

| | development machine | clean venv |
|---|---|---|
| Python | 3.12.10 | 3.12.10 |
| numpy | 2.4.2 | **2.5.2** |
| pandas | 3.0.1 | **3.0.5** |
| pyarrow | 23.0.1 | **25.0.1** |
| pytest | 9.1.1 | 9.1.1 |

The venv was created empty (`pip` only), installed with `python -m pip install .`
— the command `README.md` gives — and resolved these on its own.

### (1) The suite, run in the clean environment

```
582 collected — 577 passed, 4 skipped, 1 failed
```

**Identical on every term to the development machine**, and the single failure is
the same known `hash_set_single_source` assertion, disclosed at D-V30A-11. 577
tests that had never executed against numpy 2.5.2, pandas 3.0.5 or pyarrow 25.0.1
passed unchanged.

### (2) The same pipeline, the same source, two dependency sets

The stronger test, because a passing suite could still hide an answer that
depends on its environment. The **source was held constant** — both interpreters
import `leakaudit` from the repository's `src`, so the dependency set is the only
variable — and both ran the same non-fixture warehouse pipeline over the same
CSVs through `run_probe_a` with the same stride, cap and seed.

Output rendered canonically: verdict, cohort count, finding count, features,
per-combination outcomes, base columns, every finding as
`feature|cohort|detector|promotion|strategies` sorted, and every note sorted —
so nothing depends on dict or set iteration order.

**The two outputs are byte-identical outside the version banner.**

```
sha256 of the comparable body, clean venv        15dc83c78950d42b…
sha256 of the comparable body, dev machine       15dc83c78950d42b…
```

26 findings, 7 cohorts, 4 features, same notes including the flooring report's
0.0567%. **The probe's answer did not depend on its environment across this
step.**

### What this does NOT establish, stated in the same breath

- **Not the floors.** `numpy>=1.26`, `pandas>=2.1`, `pyarrow>=14` remain
  **untested downward**. An upward pass is silent about them. They are still the
  author's second-machine question, and this does not substitute for it.
- **Not a second machine.** One machine, one OS, one Python patch version, two
  dependency sets. A genuine portability test varies the machine; this varies
  only the packages.
- **Not the fixture path.** The comparison ran the synthetic warehouse pipeline,
  not the acceptance fixture, whose producing modules are not packaged and which
  4 skipped tests are gated behind.
- **Not all of pandas 3.** Two patch releases apart within the same major, and
  one numpy minor. This is a narrow interval, not a range.

> **The first and last of these are answered by MV-7**, which tests the declared
> floors downward. The middle two — not a second machine, one OS — are not, and
> stand.

---

## MV-7 — the DECLARED FLOORS, tested downward

**Asked (DELTA R210 §4):** an untested declared floor is a claim in
`pyproject.toml` that nobody has checked, and `pandas>=2.1` against a pandas 3.0
development environment is a **major version gap**. This was expected to find
something.

**The distinction the delta drew, and which governs what follows.** Widening or
pinning a floor to dispose of an untested risk is forbidden — that is changing
the number so the question goes away. Raising a floor to a value that was
*measured* to work, with the measurement recorded, is required if it fails —
that is the floor becoming true. **Neither was needed: nothing failed.**

**The environment.** A fresh venv at a short filesystem path, installed with the
declared floors pinned exactly, then the package on top.

```
python -m pip install "numpy==1.26.*" "pandas==2.1.*" "pyarrow==14.*"
  -> numpy 1.26.4, pandas 2.1.4, pyarrow 14.0.2
python -m pip install . pytest
  -> leakaudit 0.1.0.dev0; NOTHING was upgraded
```

That last clause is itself a result: pip resolved the package's own metadata
against the floors without needing to move any of them, so **the declared floors
are satisfiable and the metadata is consistent with them.**

### (1) The suite at the floors

```
596 collected — 591 passed, 4 skipped, 1 failed
```

**Identical on every term to the development machine**, and the single failure is
the same known `hash_set_single_source`. 591 tests passed against numpy 1.26,
pandas 2.1 and pyarrow 14 — across a pandas **major** version boundary from the
environment they were written in.

### (2) The same pipeline, now across the whole declared range

Same method as MV-6: source held constant, both interpreters importing
`leakaudit` from `src`, output rendered canonically so nothing turns on
iteration order.

| environment | numpy | pandas | pyarrow | sha256 of the comparable body |
|---|---|---|---|---|
| **floors** | 1.26.4 | 2.1.4 | 14.0.2 | `15dc83c78950d42b…` |
| development | 2.4.2 | 3.0.1 | 23.0.1 | `15dc83c78950d42b…` |
| latest resolved | 2.5.2 | 3.0.5 | 25.0.1 | `15dc83c78950d42b…` |

**All three byte-identical.** 26 findings, 7 cohorts, 4 features, the same notes
including the flooring report's 0.0567% — at both ends of the declared range and
in the middle.

### The floors are TRUE, not merely declared. No floor moved.

`numpy>=1.26`, `pandas>=2.1`, `pyarrow>=14` are now measured claims rather than
unchecked ones, and they are unchanged: nothing was widened, nothing pinned,
nothing raised.

**Not measured, and therefore not claimed.**

- **Not a second machine.** One machine, one OS, one Python (3.12.10). The
  dependency set was varied; the machine was not. **This does not substitute for
  the author's second-machine install**, which remains the only test run
  somewhere the code was not written.
- **Not every version in the range.** Three points — the floor, the development
  set, the current resolution. The interval between them is untested, and a
  regression at, say, pandas 2.3 would not have been seen.
- **Not Python.** `requires-python = ">=3.11"` was **not** tested at 3.11; all
  three environments ran 3.12.10. That floor remains unchecked.
- **Not the fixture path.** The comparison ran the synthetic warehouse pipeline;
  the 4 skipped tests are the fixture-gated ones in every environment.

**One environment artifact, recorded so it is not mistaken for a finding.** The
first attempt to build this venv failed with a Windows long-path `OSError` while
unpacking numpy — caused by the depth of the scratchpad directory it was being
created in, not by anything about the floors. Rebuilt at a shorter path and it
installed cleanly.

### `requires-python = ">=3.11"` — DECLARED AND UNTESTED, and it stays that way

DELTA R212 §1 is right that the untested cell is not "Python 3.11 on current
dependencies" but **3.11 with the declared floors — the lowest point of every
declared dimension at once.** Each dimension has been tested alone; the metadata
asserts the conjunction.

**That corner was not built.** No 3.11 interpreter is present on this machine —
`py -0` lists 3.12 and 3.13 only — and installing one is not something to do
unasked. Per R212 §1's third branch, the number is neither raised nor left
looking verified:

> **`requires-python = ">=3.11"` is declared and untested. Every environment
> measured in MV-6 and MV-7 ran Python 3.12.10.**

Nothing was changed to dispose of it. R210 §4's distinction governs: raising a
floor to a measured value with the measurement recorded is the floor becoming
true; changing a number so the question goes away is forbidden, and an untested
number that says so is honest.

### What WAS measured instead, at the other end of the Python range

**Python 3.13.1 with resolved dependencies** — numpy 2.5.2, pandas 3.0.5,
pyarrow 25.0.1:

- suite **601 passed, 5 skipped, 1 failed** — the same known failure; the fifth
  skip is the interning-conditional one described in MV-10, and it is why the
  count differs from 3.12's four.
- the same pipeline, same source: **sha256 `15dc83c78950d42b…`** — identical to
  the floor, development and latest-on-3.12 runs.

**And one fact about the declared space's shape.** The declared floors **do not
install on 3.13**: numpy 1.26.4 publishes no 3.13 wheel and the source build
fails for want of a compiler. That is **not a metadata defect** — `numpy>=1.26`
is a per-dimension minimum, and a 3.13 user resolves a newer numpy, which works.
It is a fact worth recording for what it implies about the corner: **the floors
and the Python range are not jointly satisfiable at every point of the declared
space**, so "the floors work" and "the Python range works" are two claims, and
the conjunction is a third that has been tested at exactly one point (3.12.10)
and is untestable here at the lowest.

| Python | dependencies | measured |
|---|---|---|
| 3.12.10 | declared floors | yes — MV-7 |
| 3.12.10 | development set | yes — MV-6 |
| 3.12.10 | latest resolution | yes — MV-6 |
| 3.13.1 | latest resolution | **yes — here** |
| 3.13.1 | declared floors | **not installable** (no numpy 1.26 wheel) |
| **3.11** | **anything** | **no interpreter available** |

---

## MV-8 — the availability probe's execution path, enumerated so the guard rule has a population

**Asked (DELTA R211 §2):** the whole-frame fixture guard is now a standing rule —
any round that changes a module on the availability probe's execution path
re-runs it before the round is reported done. A rule needs a definite population
rather than a list someone guessed at. **Which modules does the probe's execution
actually reach?**

**Measured, not read off imports.** An import list is not the answer:
`availability.py` imports things it never calls on this path and reaches things
it does not import at module level. A `sys.setprofile` hook recorded the file of
every frame entered during real probe runs, and the answer is the set of files
that were actually on the stack. Synthetic frames, on purpose — the question is
*which modules run*, not what they compute.

**Three runs, because "the path" is not one path.**

| run | what it covers | `leakaudit` modules reached |
|---|---|---|
| A | `run_probe_a`, whole-frame — the path that produced Phase 1's evidence | `availability.py` |
| B | `run_probe_a`, per-column — what the modes wiring added | `availability.py`, `modes.py` |
| C | the whole **reported-figures** path: probe → `eligible_cohorts` → `traces_for` → `resolve_all` → `derive_evidence_events` | `availability.py`, `availability_trace.py`, plus `protocol/runtime_reference.py` |

Run C exists because `run_probe_a` is not where the recorded numbers stop. The
guard compares a **verdict**, an **eligible** count, a **finding-record** count
and a **feature** count, and those pass through the trace builder, the resolver
and the frozen reducer after the probe returns. A module that can move any of the
four belongs in the population.

### The rule's population: four modules

```
src/leakaudit/availability.py          both probe paths, and the reported path
src/leakaudit/modes.py                 per-column path only
src/leakaudit/availability_trace.py    the reported-figures path
protocol/runtime_reference.py          the frozen reducer, on the reported path
```

### Not on it: twelve of the package's sixteen modules

`__init__.py`, `checks.py`, `cli.py`, `contract.py`, `corruption.py`,
`detectors.py`, `determinism.py`, `findings.py`, `fixture_adapter.py`,
`identity_control.py`, `model_file.py`, `probe.py`.

An edit to one of these cannot move a probe result **through `run_probe_a`**.
That is not the same as "cannot move any result": several are on other entry
points — `probe.py` and `corruption.py` carry the column dependency probe,
`checks.py` the four checks, `findings.py` the rendering.

**One qualification the trace cannot make for itself, stated rather than left
implicit.** `fixture_adapter.py` shows as *not on the path* only because these
runs supplied frames directly. In the real guard it **provides** the frames, so
an edit to it changes what the probe is fed and can move the result — as an
input, not as part of the computation. It belongs to the rule for that reason,
and the trace was never going to say so.

**Not measured, and therefore not claimed.** Whether a module unreached by these
synthetic frames is reached by the fixture's — a branch taken only on real data
(a mixed timezone, an absent frame, a dtype these frames do not carry) would not
appear here. The population is a floor on what the rule covers, not a proof of
its ceiling.

> **The set is now DATA, at `evidence/session/PROBE_PATH_SET.json`**, read by
> `tools/probe_path_guard.py`, which refuses rather than returning an empty set
> when the file is missing or unparseable, and which reports any module that
> executes and is not recorded. MV-8 is the measurement; that file is the thing
> the rule reads.

---

## MV-9 — is "the acceptance test keeps finding defects in its own fix" a real rate, or self-congratulation? THE POPULATION IS NOT RECOVERABLE.

**Asked (DELTA R212 §0):** two rounds running, a pre-written acceptance test has
found a defect inside the fix it was written for — the double-wrap in fix 6, and
the generic marker in the idempotency fix. The comfortable reading is that the
discipline works. The competing reading is that **the fixes are lower-quality
code than the original modules and the tests are merely finding what is there.**
The delta asked for a count from artifacts, explicitly forbidding reconstruction
from memory, and named the third branch: *an uncountable comparison is not a weak
result, it is no result.*

### Answer: no count is available. Neither reading is supported.

**Numerator A** — Phase 2 fixes whose own acceptance test found a defect before
commit — is **partially recorded, and not uniformly.** The double-wrap has an
entry (D-V30A-45). The generic marker, caught the same way one round later and
equally before commit, has **no entry**: it is recorded only in a commit message
and in the walk document. Two instances of one category, one disclosed and one
not, on no stated criterion. A numerator whose inclusion rule is "it seemed
notable at the time" is not a numerator.

**Numerator B** — original `src/leakaudit` modules whose first test found a
defect before commit — is **systematically absent, by the register's own design.**
`DEVIATIONS.md`'s header states its scope in its second paragraph: *"These entries
are disclosures of fact about the tagged state."* A defect caught by a test and
fixed in the same commit is not a fact about the tagged state, so it has no
reason to appear, and does not.

**`TRACKB_LESSONS.md` does not carry it either.** All sixteen entries were read.
None records a pre-commit catch on an original module.

**And the git history cannot supply it, for a structural reason rather than a
practical one.** Twenty-five commits touch `src/leakaudit`. Three subjects name a
catch — *"the citation check found two more nobody knew about"*, *"a seed that was
not reproducible"*, *"a frame that was never corrupted"*. But **a module whose
first test found nothing leaves no trace at all.** The record is one-sided:
mentions appear when notable, silence means nothing. A rate needs its
complement, and the complement here is structurally invisible. No amount of
reading commit bodies recovers it — it was never written down, because there was
nothing to write.

### What follows, and what does not

**Not supported: "the acceptance-test-before-fix discipline is catching defects
at a higher rate in fixes than in original code."** No.

**Also not supported: "the discipline is working."** That was the delta's own
comfortable reading and it has the same evidentiary basis as its opposite —
none. Two observations, no denominator, no baseline.

**What IS supported, and it is much smaller:** on two occasions, a test written
before its fix found a defect in that fix that the suite did not catch, and in
both cases the defect was in a case the fix was *holding constant* rather than
one it was changing. That is a statement about two events and a mechanism. It is
not a rate, and it must not be written as one.

**TB-11's shape, recurring.** The claim that could only flatter the record is the
one nobody examines. This one was examined, and it dissolved — not into a
contrary finding, but into the absence of any finding. That is the honest
outcome and it is recorded rather than left as an impression.

**What would make it countable in future** — noted, not built, because it changes
what gets recorded and that is not mine to decide: a per-fix note of whether its
acceptance test fired before commit, recorded whether it fired or not, so the
complement exists. Without the "did not fire" cases there is no denominator, and
that is the whole of why this could not be counted.

---

## MV-10 — the four skips in every reported suite line, named and classified

**Asked (DELTA R212 §5):** a skip is displayed as not-a-failure, one shade from
displayed-as-a-pass. §8.2 exists because *"none may be displayed in a way
mistakable for a pass."* What are the four?

**All four are in one file**, `tests/phase1/test_fixture_adapter.py`, gated on
`LEAKAUDIT_FIXTURE=1`:

| test | what it covers |
|---|---|
| `test_adapter_output_equals_the_fixture_exactly` | the adapter reproduces the fixture's own output |
| `test_known_positive_perturbing_the_served_snapshots_FIRES` | **a known positive** |
| `test_known_positive_perturbing_trades_reaches_the_output` | **a known positive** |
| `test_serving_does_not_let_one_run_alter_the_next` | mutation isolation between runs |

**They were run.** `LEAKAUDIT_FIXTURE=1 python -m pytest
tests/phase1/test_fixture_adapter.py` → **10 passed in 288.49 s** at commit
`47f462f`. Recorded in `tests/phase1/fixture_run_record.json` as
`run_2026_09_03`, beside the earlier runs rather than in place of them, per that
file's own rule.

### Classification under §8.2: none of the three words fits

- **Not `not_applicable`** — the fixture's code is present here, and the skip
  message says so. They apply.
- **Not `unsupported`** — they are supported and they pass.
- **Not `could_not_run`** — they can run. They just did.

They are **deferred by cost**, and §8.2's vocabulary has no term for that. The
gap is the report: displaying a cost-deferred test that would pass alongside a
genuinely inapplicable one, both as "skipped", is the display problem §8.2 guards
against, one level up from where §8.2 was written.

### Two findings the exercise turned up

**(1) Two of the four are known positives, and they had never fired in any
reported suite line.** This project's own rule is that a check whose positive has
not fired is not a check. Two such positives sat behind an opt-in through every
"4 skipped" in every report this phase.

**(2) `fixture_run_record.json` had gone stale again, by the exact mechanism its
own banner describes.** The banner warns that twelve commits had touched the
probe's modules since the 2026-08-26 run. The superseding 2026-09-02 entry
attests commit `8320a20` — and `src/leakaudit/availability.py` has since been
changed by four commits. **Nothing detected the recurrence**, because
`test_every_opt_in_test_has_a_recorded_result`, which does run in the default
suite and passed throughout, checks that every opt-in test **has** a recorded
result and not that the result is **current**. The staleness warning is prose in
a JSON field, and no test reads it.

### A fifth skip exists, and only on Python 3.13

Not visible from any 3.12 run. `tests/phase1/test_digest_stability.py:82` skips
with *"the two strings were interned to one object, so the pointer digest happens
to agree here; it does not across processes."* That one **is** `not_applicable`:
the interpreter interned the two strings, so there are not two objects for the
check to distinguish and it has no subject. Correctly conditioned and correctly
explained by its own message.

**Not measured, and therefore not claimed.** Whether other interpreters or
platforms condition further tests — two Pythons were run, on one OS.
