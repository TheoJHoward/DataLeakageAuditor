# Is `moved_in_second` the registered comparator? Measured, on both selection paths

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures. This is a Phase 1 **instrument** report.

**The question, R260 §3(c), asked before any L2a code:** does every cell the
availability probe perturbs have `a(j) = F + 1` exactly, where `F` is the
corrupted second and `a(j)` is the cell's declared availability instant? If yes,
`moved_in_second` **is** the registered comparator written as a special case, and
the label probe may be built as the general case of one rule. If no, the cells
and inputs where it is not are named and nothing is repaired.

**Answer: NO.** It holds on one of the two selection paths the shipped probe
carries, and fails on the other, which is reachable from a declared version-3
config file.

**Tree state.** Measured at `cea7414`, working tree clean. `py -3.12`, CPython
3.12.10, numpy 2.4.2, pandas 3.0.1. The script is
`identity_probe.py` in the round's work root; it imports the shipped modules and
recomputes the selection with the shipped expressions rather than paraphrasing
them.

---

## The two selection paths, and why they are different arithmetic

Both live in `run_probe_a`, a few lines apart.

| path | selection | the cell's declared instant | so `a(j) − F` is |
|---|---|---|---|
| **frame rule**, no `column_modes` | `floor(key).isin(picked)` | `floor(key) + window` | **exactly `window`** |
| **per-column mode**, v3 `column_modes` | `floor(a − window).isin(picked)` | the column's own `a(j)` | **anywhere in `[window, window + 1s)`** |

The frame rule selects by the *key's* second and the declared instant is defined
off that same floored key, so the two agree by construction. The per-column path
selects by `floor(a − window)` and the instant is `a` itself, so the floor throws
away up to a second of the instant and the identity is lost to that remainder.

**Measured on one frame set** — twelve aggregate rows keyed at `T0 + n s + 500 ms`,
one decision row per second, the registered default comparator:

| path | cells perturbed | `a(j) − F` observed |
|---|---|---|
| frame rule | 12 | `0:00:01` |
| `at_timestamp` column mode | 11 | `0:00:01.500000` |

**A mid-second key is not a contrived input.** The acceptance fixture's own
`trades.ts_event` is one on 397,408 of its 397,457 rows, median offset 467.83 ms —
measured earlier and recorded in `AvailabilityModel`'s docstring, where it was
found as a different defect (D-V30A-43).

---

## The consequence: a real leak reported as `observed_silence`

Same frames, same builder, **one** probed cohort so that exactly one cell is
corrupted and exactly one output row moves — attribution is then unambiguous and
the batch cannot supply the answer.

The leak: output row *m* decides at `T0 + m s` and reads the aggregate row keyed
`500 ms` later. Under the per-column declaration that cell's instant is
`d + 500 ms`; under the frame rule it is `d + 1 s`. **Both are after the decision,
so the registered comparator `a(j) > d(i)` says unavailable, and both say
finding.**

| path | cohort `F` | `a(j)` | `moved_in` | `moved_next` | verdict |
|---|---|---|---|---|---|
| frame rule | `T0` | `F + 1s` | 1 | 0 | **`finding`** |
| `at_timestamp` mode | `T0` | `F + 1.5s` | 0 | 1 | **`observed_silence`** |

The moved row decides at `F + 1s`. The cell's declared instant is `F + 1.5s`.
`F + 1.5s > F + 1s` is unavailable, so the row is a finding under the
registration. `moved_in_second` puts it in the *next* bucket and the cohort is
reported silent.

**`observed_silence` is this tool's affirmative claim** — *I looked over a stated
population and found nothing; this is evidence* — and here it is produced over a
leak the registration's own comparator flags. That is the R236 shape in a new
place, and R236's instance was the reason `decision_column`'s default was removed.

**The direction is one-way, and that was checked rather than assumed.** For every
row in the `in_sec` bucket, `d(i) < F + window ≤ a(j)`, so the cell is unavailable
to it under both tie branches. **The divergence can therefore only lose findings,
never invent them.** No figure this project has published can have been inflated
by it.

---

## The second input: a declared window other than one second

`nxt` is computed as `base_floor == f_sec + model.window`, and `in_sec` as
`base_floor == f_sec`, so the two buckets are one second wide and `window` wide
apart. `window_seconds` is a registered version-1 key with no constraint on it.

- **`window = 2s`.** Rows deciding in `[F + 1s, F + 2s)` are unavailable, because
  `a(j) = F + 2s` is after them. They fall in neither bucket: not a finding, not
  a silence, **not counted at all**.
- **`window = 1.5s`.** `f_sec + 1.5s` is never a second boundary and `base_floor`
  always is, so `nxt` can never match. Measured: `moved_next_second` totalled 0
  across every cohort, on frames where the one-second run reports movement there.

Neither input is exotic and neither is refused.

---

## Scope, stated so the disclosure is not read wider than it is

**No published Phase 1 figure moves.** The per-column path requires
`column_modes`, and the frame-rule path is identical to the comparator at the
default window.

    grep -rlc "column_modes" evidence/phase1/ | wc -l     ->  0

at `cea7414`; and `VALIDATED_CONFIG.toml` is still a placeholder carrying no
value under any of its four tables. So the exposed population is **runs a user
makes with a declared version-3 `column_modes` block, or a `window_seconds` other
than 1.0** — not the acceptance runs.

**What this does not establish.** It does not say the per-column path is wrong to
produce fewer findings than the frame rule. D-V30A-49 records R205's measurement
of 25 cohorts with a finding under the coarse rule against 0 under the per-column
rule, on a frame whose column was published half an hour before the row carrying
it, and reads the 0 as a false positive correctly suppressed. That reading may
well be right on that data. **What the measurement above establishes is narrower
and is about evidence rather than about that case: a 0 under the per-column path
is not by itself evidence that the coarse path was wrong, because the bucket
geometry can produce a 0 with the comparator saying otherwise.** Separating the
two on R205's data was not attempted here.

**Nothing was repaired.** R260 §3(c) directs that a divergence is recorded and
the probe waits for a ruling. `availability.py` is untouched.

---

## What the label probe cannot now do

`DESIGN.md` §2.7's "probes cohorts exactly as L3.1 does" cannot be read as
licence to reuse the buckets. Under a declared label horizon `H`, a corrupted
label cell in second `F` is unavailable to every output row deciding in
`[F, F + H)`, and a two-bucket geometry one second wide describes that only when
`H` is one second. R260 §3(a) states the rule the label probe implements instead:
per perturbed cell and moved row, a finding when `d(i) < a(y_j)` and not a
finding when `d(i) >= a(y_j)`. That is the same comparator this file measured
L3.1's buckets against.
