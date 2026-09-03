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
