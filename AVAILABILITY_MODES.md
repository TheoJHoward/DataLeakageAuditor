# The availability modes, and what each one computes

**Written before the parser that reads them, deliberately.** A mode whose
arithmetic is settled after its key name exists is a mode whose arithmetic gets
settled by whatever the parser happened to do. The bar each entry below has to
clear is that **two readers get the same availability instant from the same
data** — anything looser produces silent wrong answers, which is the failure
this whole phase is about.

The vocabulary is not invented here. It is the `column_roles` vocabulary of the
registration, and each mapping below is quoted from `DESIGN.md` §2.1 with the
supporting rules cited to the sections that own them.

## The two quantities

For a cell at row *j* of column *c*, and an output row *i*:

- **`a(j, c)`** — the availability time of that cell: the instant its value
  became knowable.
- **`d(i)`** — the decision time of output row *i*.

Whether a cell is available to a row is settled by the comparator registered at
`PREREG.md` §2.3 and is not restated here. What this document fixes is only the
left-hand side: **what `a(j, c)` is, per mode.**

`ts[j]` below means row *j*'s value in the frame's timestamp column, read under
the declared `timestamp_semantics` — whether that column holds observation,
event, or availability time is itself declared (`PREREG.md` §2.3), and every
mode below inherits whatever that declaration says.

## The six modes

| mode | `a(j, c)` |
|---|---|
| `at_timestamp` | `ts[j]` |
| `at_bar_close` | `ts[j] + bar_duration(j)` |
| `at_source_timestamp` | the named source column's value at row *j* |
| `always` | negative infinity |
| `explicit` | the named column's value at row *j* |
| `availability_fn` | whatever the user's callable returns for `(j, c)` |

### `at_timestamp`

`a(j, c) = ts[j]`.

The cell became knowable at the instant the row is stamped. This is the right
mode for a value observed at the moment the row records — a book snapshot at
event time, a price at the tick that carries it.

### `at_bar_close`

`a(j, c) = ts[j] + bar_duration(j)`.

The cell summarises a bar that opens at `ts[j]`, so it is not knowable until
that bar closes. **`bar_duration(j)` is the declared bar length, or, under
`inferred`, the gap to the next timestamp; at the final row the last known
duration is carried forward**, since there is no successor to measure against
(`DESIGN.md` §2.1, `PREREG.md` §2.3).

**The trap this mode exists for.** A rolling window computed on bar values and
read at bar open is the modal error in this domain. Under `at_timestamp` such a
column looks available; under `at_bar_close` it does not.

**And the trap this mode itself sets.** Where a value's true instant is a join
key rather than a bar boundary, `at_bar_close` is an *approximation* of it and
scoring against the approximation can find a contaminated pipeline clean. The
acceptance fixture's own declaration says so in terms about its own data. If a
column's availability follows something carried in the data, `at_source_timestamp`
is the mode, not this one.

### `at_source_timestamp`

`a(j, c) = src[j]`, where `src` is the column named with the mode.

**Not `ts[j]`.** That is the whole point of the mode: a macro figure published
on its own schedule, joined onto a fast frame and forward-filled, is knowable
when it was *released*, not when the row that carries it is stamped. The release
instant travels in the data; this mode reads it.

### `always`

`a(j, c) = -∞`.

The cell was knowable before any decision this frame contains. Static metadata:
a tick size, an instrument's sector, a contract multiplier. Nothing that varies
with time belongs here, and a column placed here is a column exempted from every
availability comparison the tool makes.

### `explicit`

`a(j, c) = col[j]`, where `col` is the column named with the mode.

**Arithmetically identical to `at_source_timestamp`, and that is worth stating
rather than hiding.** Both read an availability instant out of a named column at
row *j*. The difference is what the declaration is *saying*:
`at_source_timestamp` says "this column's availability follows a source whose
release time is carried in that other column"; `explicit` says "I have computed
this column's availability myself and put it there".

**Consequence, and it is reported rather than papered over: no data can
distinguish these two modes.** They compute the same instant from the same
column, so a test that claims to tell them apart is testing nothing. Where §4 of
the plan asks for a neighbouring-mode negative, these two are neighbours with no
gap between them, and the honest answer is that the distinction is documentary,
not computational.

### `availability_fn`

`a(j, c)` is whatever the user's callable returns.

The escape hatch, and it is the only mode this document cannot pin down, by
construction. A tool cannot state what a user's function computes. What it can
do is refuse the failure modes: a callable that returns the wrong length, or
values that are not timestamps, is refused rather than broadcast into a mask.

**It is not available from the config file.** A file format cannot carry a
function, and a mode that could only be declared by writing Python does not
belong in a document that a user is invited to hash into their own
pre-registration. It is reachable from the library.

## What is not settled here, and is not pretended to be

- **The comparator.** `PREREG.md` §2.3 owns it, including which branch a tie
  takes. This document computes only the left-hand side.
- **The label's rule.** The label column takes `label_availability`, never a
  generic role (`DESIGN.md` §2.1). That is a separate declared element with its
  own section, and none of the six modes above applies to it.
- **Which mode a column should take.** That is the user's declaration to make.
  Inference proposes; it does not choose (see below).

## Inference proposes; it does not pick

When inference arrives it will read timestamp columns and suggest a mode. It
will not apply one.

**A mode inferred and applied without confirmation is a declared availability
model the user did not declare** — and every result computed under it carries an
assumption they never made and cannot see. So: propose, with the evidence for
the proposal, and either take a confirmation or refuse. There is no third
branch where the tool decides quietly.
