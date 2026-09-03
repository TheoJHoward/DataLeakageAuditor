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
