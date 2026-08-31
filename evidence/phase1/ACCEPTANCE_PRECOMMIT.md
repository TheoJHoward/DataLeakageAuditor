# §6.2 ACCEPTANCE RUN — THE PRE-COMMITMENT

**Committed before the harness is executed.** Nothing below is adjusted once a
number is visible. If the harness turns out to be wrong that is a finding, it is
recorded, its fix is a separate commit, and the re-run is a second and separately
labelled result with the first still in the record.

Probe A's precedent governs: it was committed before it was run, so whatever it
showed would be published.

---

## 1. THE INVOCATION, EXACTLY

```
ACC_SYM=zc ACC_MONTH=2025-01 ACC_SIDES=corrected,contaminated \
LEAKAUDIT_FIXTURE=1 PYTHONPATH=<repo> \
python tests/phase1/harness_acceptance.py
```

**Harness:** `tests/phase1/harness_acceptance.py`, committed with this file.
**Output:** `evidence/phase1/acceptance_run.json`, checkpointed after each side.
**stdout / stderr / exit status:** captured to files and committed unmodified.

## 2. THE INPUTS

| input | what it supplies | read by |
|---|---|---|
| the f2 rebuild pair via `fixture_adapter` | Artifact A, both sides | the tool |
| `AVAILABILITY_DECLARATION.md` §A.6.1 | the REQUIRED list and each unit's governing map class | the harness only |
| `evidence/fixture_spike/f3/fixture_manifest_DRAFT.json` | the column classes | the harness only |
| `evidence/fixture_spike/n1/declared_map.csv` | the declared map's cells | the harness only |

**The tool receives none of the last three.** SC-7(b)/(c) withhold the map from
it, and `tests/phase1/sc7c.py` states that executably: the package neither
imports, names, constructs nor reaches the label type, checked by parsing every
module, with one violating copy per route and a negative control.

**Ground truth is derived, not transcribed.** The REQUIRED list is parsed from the
declaration's table and the parse **checks itself against the declaration's own
stated N**: a first version of it returned ten units for a denominator of eleven,
having silently dropped the one row whose class cell carries a parenthetical, and
a denominator short by one scores a different criterion. It now raises.

## 3. THE SCOPE, AND WHAT IT BOUNDS

**One instrument-month — zc 2025-01 — both sides.** Measured cost, before
committing to it: input capture 39.4 s, one build 34.2 s, 47 source columns, so
95 builds for a full preserving pass per side, about 54 minutes, and roughly two
hours for both sides with the promoted combinations.

This is **not a gate result and is not published as one.** §6.2's criteria as
amended are the whole gate; this run covers one of forty-eight instrument-months,
scores three of four criteria, and criterion 3's cells in scope are 20 of 960.
The output file carries all of that as data.

## 4. THE NUMERIC THRESHOLDS, REGISTERED

| threshold | value | registered at |
|---|---|---|
| clean-case finding gate | fail at k ≥ floor(0.20 × N) + 1 | §10.2 item 3 |
| completion floor | 60% of the same N reach `completed` | §10.2 item 3 |
| reference-AUC anchor | ±0.010 absolute **per entry**, not widenable, `full` mode | §6.2, SC-2(d) |
| anchor near-tolerance | a deviation approaching the tolerance is **stop-and-report, not a pass** | §6.2 |

The anchor is not exercised by this run: it is a property of the stored
predictions, and this run scores the rebuild pair.

## 5. THE EXPECTATIONS — one per criterion, falsifiable, written before the run

A result differing from any of these is reported as a finding. It is never a
reason to adjust the harness, the threshold, the inputs, or the expectation.

### Criterion 1 — every ground-truth leaking source column receives at least one primary runtime finding

- **Registered denominator: 11.** The REQUIRED list of §A.6.1. No other quantity
  is N, and the denominator is never adjusted to what happens to be reachable.
- **Observable in this artifact: 8.**
- **Remainder: 3** — `trade_volume_1s`, `trade_count_1s`, `dollar_volume_1s`.
  Their state is **`unsupported`** under §8.2, whose boundary reads *"missing or
  impossible inputs are `unsupported`"*, on the ground that each is one of the
  nine columns Phase 7 adds and the Phase 5 set does not carry, so the column is
  absent from the artifact the criteria are evaluated on. §8.2: none of these
  states is displayed in a way mistakable for a pass, and that governs this file
  and the result file equally.
- **EXPECTATION: all 8 observable units receive at least one primary finding on
  the corrected side.** The ground is prior published evidence, not hope: B8's
  dependency map moved exactly those 8, and the declaration's as-built defects
  section records five `net_delta_*` and `sell_volume_10s` among seven columns
  the classifier defect reaches.
- **What falsifies it:** any of the 8 receiving no finding. That is a miss, and
  criterion 1 fails over this scope.

### Criterion 2 — no manifest-clean source column receives any finding, any tier, on the contaminated side

- **Clean population: 4** — `minutes_since_open`, `session_open`, `session_mid`,
  `session_close`.
- **Reachable in this artifact: 1** — `minutes_since_open`. The other three are
  Phase-7-added and take **`unsupported`**, same ground as above.
- **Stated plainly: the reachable clean population is one.** The criterion is
  therefore **thin, not vacuous.** It can fail, and what would fail it is a probe
  moving `minutes_since_open` on the contaminated side.
- §C.4(b) disposes of the session flags separately: they are lagged deterministic
  clock functions, which is **staleness and not unavailability** under SC-1(e),
  declared as an as-built property and licensing no corrected-side finding. That
  disposes of a finding on them; it is not why they are unreachable here.
- **EXPECTATION: `minutes_since_open` receives no finding on the contaminated
  side**, because it is a deterministic function of the row's own timestamp and
  no probed input feeds it.
- **What falsifies it:** any finding naming it. That is a false positive and
  criterion 2 fails over its reachable population.

### Criterion 3 — findings scored against the declared ground-truth map

- **The map's cells: 960.** Every one is dispositioned before any detector runs:
  **288** by §A.6.1's governing-class column, **576** by §13(j) — no fed column
  is MBO-fed, so the six MBO classes attach to none — and **96** by §C.4(a),
  `trades_buy` being a degenerate unit excluded pre-run.
- **In scope for this run: 20** — one instrument-month × two sides × ten classes.
- **EXPECTATION:** every finding maps, through the governing-class column, to a
  `trades_*` class; **no finding maps to an `mbo_*` class**, since no fed column
  is MBO-fed; **no finding maps to `trades_buy`**, which is zero strict and zero
  equal in all 96 of its cells on both sides.
- **What falsifies it:** a finding whose governing class is `mbo_*` or
  `trades_buy`. Either is a false positive under SC-3(b).

### Criterion 4 — silent under the identity control on both sides

- **UNSCOREABLE IN THIS RUN. The identity control is not implemented.** The
  probe's strategy order is shuffle, sentinel, nan and sentinel-ood; there is no
  identity strategy. An accidental identity permutation is handled as a
  `control_artifact` failure, which is the detection of a degenerate perturbation
  and not a control run.
- **EXPECTATION: none is stated**, because the criterion cannot be exercised.
  Recording it as passing on the strength of no findings from a control that
  never ran would be exactly the conversion of silence into a pass that §8.2 and
  SC-3(g) forbid.

## 6. THE IDENTIFIER FORM — a free choice, recorded as one

`affected_output_cohort` carries `col:out.<column>`, where `out` names the built
frame. **The registration fixes the unit — feature × affected output cohort — and
not the identifier's string form**; its own fixtures use abstract ids. So this is
a convention chosen freely, and it is written down here rather than left to be
mistaken later for a requirement.

The reason: it keeps `col:out.net_delta_1s` distinguishable at a glance from
`col:trades.size`, which is the distinction the field lost while it carried the
probed input. `probe_columns` refuses a caller frame named `out`, because a
collision would print two different things identically. The one sanctioned way
back from the field to a column name is `output_column_of`, a named and tested
function rather than string surgery repeated at call sites.

**Which field the criteria read:** criterion 1 requires attribution *"to the
labelled source"*, the labelled sources are the manifest's columns, and a
finding's `feature` carries the output column that moved. The criteria are scored
from `feature`. **`affected_output_cohort` is an input to none of them**; it is
reported and not scored on.

## 7. WHAT THE OUTPUT FILE CARRIES AS DATA

`criteria_scored: [1, 2, 3]` · `criterion_4:
UNSCOREABLE_NO_IDENTITY_CONTROL_IMPLEMENTED` · `criterion_3_scope:
THIS_INSTRUMENT_MONTH_ONLY_20_OF_960_CELLS` · `gate_result:
NOT_A_GATE_RESULT_PARTIAL_SCOPE` · and the repository's own gate status with the
disclosure that closes it as a known false positive, so a reader seeing a red
gate beside these numbers can tell which it is.
