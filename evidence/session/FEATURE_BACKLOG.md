# The feature backlog — enumerated from the repository, not from memory

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures.

**Why enumerated rather than recalled.** R254 §2(a): the planning layer offered
the shuffle establish as a live option and it has been retired since R215, and
offered "the D2 subsystem" — **`D2` does not occur in `DESIGN.md` or
`PREREG.md`**, so it is not findable by that name. Two items from recollection,
two wrong. After this many rounds recollection is not a source, so this is read
off the tree.

**Sources read:** `PARKING_LOT.md`, `evidence/session/DEFERRED_ITEMS.md`,
`DESIGN.md` §§1–5, the shipped modules under `src/leakaudit/`, the CLI's own
subcommand table, and one live run of the tool.

---

## What a stranger can do today

`leakaudit` ships four subcommands — `run`, `check`, `draft`, `schema` — over
sixteen modules. Measured by running it:

    leakaudit run --pipeline mod:build --frame a=x.csv --model m.json

prints the verdict, each finding with the perturbed second and the detector that
produced it, the frames **NOT PROBED** with why their silence is `none` rather
than `observed_silence`, and an **ABOUT THIS RUN** block carrying the comparator
and the corruption count. So `DESIGN.md` §39's *publish the detection domain* is
substantially built for the availability probe.

**BUILT** — availability probe (L3.1) with its identity control and per-column
modes; Layer 1 column dependency (`probe.py`); the B9 value/null detectors;
four model-free checks (split validity, duplicates across the split, constant
columns, pairwise label correlation); draft/inference; the model file and its
schema; determinism, corruption, findings, contract, trace, fixture adapter.

---

## The backlog

### A. `DESIGN.md` §2.7 — the label probe (L2a)
**Status: NOT STARTED.** `checks.py` has `check_pairwise_label_correlation`,
which is a model-free *check*, not this probe. §2.7 specifies the same machinery
as L3.1 with the mask intersected with the label column, using `a(y_j)` from
`label_availability`.
**What it would take:** a `label_availability` field on the model (a second
clock, refused-not-defaulted like `decision_column`), the mask intersection, and
the temporal corruption case. The cost model already reserves its `C × S` term.
**Value:** high — label leakage is the failure most users come looking for, and
the tool currently cannot probe it.

### B. `DESIGN.md` §2.8 — L1.2's split-specific confirmation
**Status: NOT STARTED.** Needs the split, not the availability model, so it sits
beside `checks.py` rather than the probe.
**What it would take:** hold the declared training population byte-identical and
confirm the split-specific claim. Reuses the split the checks already parse.
**Value:** medium — model-free, so it costs a stranger nothing, which is the
argument `checks.py` was built on.

### C. `DESIGN.md` §5.2 — `quick` mode as a first-class CI default
**Status: BUILT (R267, R268) — and ruled other than §5.2 wrote it.** `quick`
is not a mode. L2a rebuilds once per cohort, so its budget is a COHORT COUNT,
derived from a measured build time and printed as a default: 16, where the
shipped 25 was over the ten-minute target with no arithmetic written down. L3.1
batches, so its budget is PASSES, printed as `L3.1 PASS BUDGET`.
**Coverage is three states** — probed, eligible but unprobed, ineligible under
the model — for cohorts and for rows, never thresholded, and checked to cover
its population. **A subsampled run is not treated as complete**, the reverse of
§5.2's sentence (overridden at `DESIGN.md` §10.8): a default run exits
`EXIT_INCOMPLETE_SILENT`, 4. The two routes to a clean exit are a declared
`--accept-partial-coverage`, printed beside the verdict, or `--complete` —
`stride` passes at different offsets for L3.1, every eligible cohort for L2a.
`assert_audit_complete` holds the same rule at the library door.
**What complete costs, measured on the acceptance fixture (R268):** reach 14 s,
so stride 15 and 15 passes; one pass 202.0 s; the run 54.7 min with the reach
measured once. **That is the contaminated side.** The guard's run measured the
corrected side's reach at 15 s, so its complete run takes stride 16 and 16 passes
— about 58 min at the same pass cost, an estimate, since that side's pass was not
timed.
**Value:** medium-high for adoption — it is the difference between a tool run
once and a tool run in CI.

### D. `DESIGN.md` §5.3 — auditing a slice, with padding
**Status: BUILT at R255.** `src/leakaudit/slicing.py`, `--slice-from` /
`--padding`, `tests/phase1/test_slicing.py` (24 tests).

**What was established before anything was refused.** R255 §1 required deriving
the padding threshold from the availability model *first*. Measured: the model
has four fields and one duration among them, so it founds a **floor**
(`window`, or a **declared** `bar_duration` where larger) and does **not**
determine the requirement — the binding quantity is the *builder's own
lookback*, and `build` is an opaque callable. An inferred `bar_duration` is
per-row and contributes nothing. So the primary refusal is a **presence test**
(padding not declared), which needs no threshold and cannot rest on an invented
one. That is `DESIGN.md` §5.3's own answer, not a gap.

**The known positive is an edge positive, both halves measured — and its figures
were superseded twice.**

| when | unpadded cut | padded | stride |
|---|---|---|---|
| R255 (2026-09-07) | `observed_silence`, 0 over 30 cohorts | `finding`, **30/30** | 1 |
| R263–R265 | `none(…)`, 0 over 15 cohorts | `finding`, **15/15** | 2 |
| **R268, standing** | `none(no perturbed cell reached the pipeline)`, 0 findings, 1 cohort | `finding`, **1** finding, 1 cohort | 97 |

**30/30 and 15/15 are kept as dated figures and are SUPERSEDED: both were
produced at a stride thirty times under the builder's measured reach, and each
finding overlapped the next.** (Exactly: the reach is 59.5 s, so 15/15 at stride 2
was ~30× under and 30/30 at stride 1 was ~60× under.) The R255 fixture control
(`min_periods=1` "finds all 30") belongs to the same superseded run.

**What the standing pair shows, with the reach printed.** The padded side finds
the leak in its one cohort (liveness 1) with reach measured at **59.5 s** (one
usable sample, two censored by the frame's end). **The cut side does NOT show it
even in one cohort**, and the reason is total rather than edge-shaped: the cut
frame carries 30 rows and the builder's window needs 60, so the builder emits
**zero** non-NaN features from it. One cell is perturbed and no output value
exists that could move — so the verdict is `none`, not `observed_silence`, and
the reach on that side is **not measured** (all three samples: nothing moved),
which the run states is not a reach of zero.

**Known limit, pinned as a test.** A padding that clears the model-founded floor
can still be far below the builder's lookback: 2s of padding clears the 1s floor
and the run is still fully masked. No refusal can close this — only the
declaration can. `test_THE_RESIDUAL_HOLE_...` fails if a future change closes it.
**Also out of scope:** a caller who truncates their frames *before* calling. The
tool cannot distinguish that from data that starts late.

### E. `DESIGN.md` §1.2 — domain profiles
**Status: NOT STARTED.** A table of profiles (`generic` and others) supplying
default `column_roles`, `label_availability` and `ties`.
**What it would take, and the tension to resolve first:** profiles are defaults,
and R236 removed a default that turned a real leak into `observed_silence`. A
profile that silently supplies `column_roles` is that defect with a nicer name.
**Value:** high for §139's adoption surface, **conditional on** the defaults
being declared-and-visible rather than assumed.

### F. `align_key`'s timezone cases, enumerated
**Status: PARTIALLY BUILT.** The function ships and refuses the aware/naive
mismatch with a message naming both sides. What is missing is the **cases
document** its siblings have — `LABEL_SCREEN_CASES.md`, `FORK_VOCABULARY_CASES.md`
— enumerating the zone situations before the vocabulary is fixed.
**Value:** low-medium; the refusal already prevents the silent-wrong-answer.

### G. The export/submodule shadowing repair
**Status: DESIGNED, PARKED.** `evidence/session/EXPORT_SUBMODULE_COLLISION.md`
carries three repair shapes with their blast radii. R238 parked it as an API
decision; probed again at R252 from the import-failure angle without escalating.
**Value:** low as a feature, non-zero as a trap.

### H. `DEFERRED_ITEMS.md` §173 — the fourth direction (untracked, unattested,
unlisted)
**Status: SPECIFIED, NOT STARTED.** A file that is untracked, in no manifest and
on no ephemeral list. The entry notes a known positive available today.
**Value:** instrument work, not a feature — and the sweep is banked.

---

## Banked, visible, not worked

Theo ruled the sweep banked at R254. These stay in the map and are not worked:
the **67 unverified** coverage assertions, a **fixture-emptying probe** for the
51 the current mechanism cannot reach, instruments for the **value-coincidence**
and **wrong-input** vacuity subclasses, and — recorded here per R254 §3 — the
**validation the `out_of_scope` criterion is owed if the sweep resumes**:
on the assertions the probe *can* reach, does the criterion's coverage/content
call agree with whether the probe found them emptiable? Disagreement bounds the
criterion's error. **Not run now.**

---

## The mandate's own test

*What can a stranger with their own pandas pipeline still not do that "easy and
useful" implies they should?*

1. **Probe label leakage** (A) — the thing most users arrive for.
2. ~~**Audit a slice safely** (D)~~ — **closed at R255.** A slice is now refused
   without declared padding, the padding rows are reported as `not_applicable`
   rather than audited-clean, and the edge leak the rule exists to stop masking
   is a measured pair in the suite.
3. **Run it in CI without deciding what "complete" means** (C).

Everything else on the list is either an instrument, a parked API question, or a
document.
