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
derived from measured cost and printed as a default: **13** (R269), from 67.0 s
fixed + 40.5 s per L2a cohort against a 600 s target. R267's 16 had priced an L2a
cohort at a clean build's 34.9 s, and the shipped 25 was over the target with no
arithmetic written down; both exceed 600 s at the measured cost. L3.1
batches, so its budget is PASSES, printed as `L3.1 PASS BUDGET`.
**Coverage is three states** — probed, eligible but unprobed, ineligible under
the model — for cohorts and for rows, never thresholded, and checked to cover
its population. **A subsampled run is not treated as complete**, the reverse of
§5.2's sentence (overridden at `DESIGN.md` §10.8): a default run exits
`EXIT_INCOMPLETE_SILENT`, 4. The two routes to a clean exit are a declared
`--accept-partial-coverage`, printed beside the verdict, or `--complete` —
`stride` passes at different offsets for L3.1, every eligible cohort for L2a.
`assert_audit_complete` holds the same rule at the library door.
**What complete costs on the acceptance fixture, CURRENT (R271, corrected side):**
61 passes at stride 61 — the block reach and the single-second reach each 60 rows,
plus one — setup 1,241.9 s, pass one 175.1 s, **~198.7 min predicted**, not run to
completion (D-V30A-116).

**SUPERSEDED, 2026-09-14 (R272 §2(f)): the figures in the rest of this paragraph
and the next two were produced by a reach that corrupted one frame of two.** They
are kept as the dated record of what was measured, not as costs.

~~What complete costs, measured on the acceptance fixture (R268):~~ reach 14 s,
so stride 15 and 15 passes; one pass 202.0 s; the run 54.7 min with the reach
measured once — **SUPERSEDED**. **That is the contaminated side.** **The corrected
side was run complete end to end at R269, after the round's commit:** reach 15 s,
stride 16, 16 passes, **3,671 s = 61.2 min** — **SUPERSEDED**. Pass one took 209.1 s and printed about 52.3 min
for the 15 passes left, so sixteen passes at pass one's cost are 3,346 s; the 325 s
between that and the whole run holds the baseline, determinism check and reach
measurement made before pass one, plus any drift in the later passes — **not timed
apart, so not split here.** The prediction covers only the passes.

**AND ITS VERDICT WAS `finding`.** The corrected side is the fixture with its leak
removed, and its stride-997 sample reads `observed_silence`. Probed over every
cohort (338,159, 15 of them head), it reports a finding. **That is not explained
here, and nothing is claimed from it.** Either the corrected builder carries a
leak the sampled cohorts never touched, or the complete run produces findings the
builder does not: its stride of 16 comes from a reach that is a lower bound from
three samples, and interference below the true reach is the D-V30A-106 shape. The
measurement script recorded the verdict and not the count or location of the
findings, so the establish that would tell these apart has not been run. **This
is a Phase 2 instrument observation, not a `PREREG.md` §6.2 result, and it is not
comparable to the Phase 1 corrected-side silence without a ruling.**

**R270: THE FINDING IS INTERFERENCE, AND COMPLETE MODE AS SHIPPED PRODUCES IT.**
Re-run with its records kept (reach at k = 10: 15.9997 s, stride 16, 3,803 s =
63.4 min — **the reach and the stride SUPERSEDED, 2026-09-14: produced by a reach
that corrupted one frame of two**; the run's finding count below stands as what
that stride produced), the corrected side reported **163,143 finding cohorts of 338,159**,
one row each, almost all on `net_delta_60s`, filling whole sessions (median gap
1 s). Twenty chosen by rank were re-probed alone and **all twenty vanished**; the
reach measured at them is 15.9997 s, the run's own. Re-probed beside only their
EARLIER same-pass neighbours the findings return (four of five with one
neighbour, five of five with eight); beside only their LATER neighbours they
never do. Earlier cells are available to the row, so this is interference and
not a leak in the corrected builder. **So `--complete` on a builder with no leak
reports tens of thousands of findings and exits 1.** Its stride is
`int(reach) + 1` = 16 s against a reach of 15.9997 s, a clearance of 0.3 ms; that
this boundary is the cause is one reading and not established. The shipped
default (stride 97, 400 cohorts) on the same side reads `observed_silence`, 0
findings, liveness 328. D-V30A-114. **Phase 2 instrument observations; no
`PREREG.md` §6.2 result and no Phase 1 figure moves.**

**R271: THE REACH CONTROL NEVER SAW THE TRADES FRAME, AND THE BLOCK REACH NOW
SETS THE FLOOR.** Counting cells to find which neighbour moved the row showed
`reach._corrupt_one` compared a UTC-aware trades key against naive decision
seconds, which pandas answers with all-False: zero trades rows at all ten of
R270's reach samples. **Every reach printed for the fixture (14 s, 15 s,
15.9997 s) was the MBO frame's alone, and every `--complete` stride derived there
(15, 16, 16) rested on it.** With keys aligned, one second of trades reaches
`net_delta_60s`'s full 60 s. The block reach — the history before a position
corrupted in one rebuild — reads 55 s, 60 s and 59 s at three positions. The
stride floor is now `max(model floor, block reach + 1 s)` on every run; a
complete run takes the largest measured floor rounded up, and refuses where no
stride the frame can hold would clear it. `--confirm` splits a vanished finding
by later and earlier cohorts, and an INTERFERENCE class refuses the run.
D-V30A-115.

**R271 §2(d)(f), measured after that commit.** On the corrected side both
measured floors are 61 s, so `--complete` is 61 passes: setup 1,241.9 s, pass one
175.1 s, **~198.7 min predicted** and not run to completion. Pass one at stride 61
probed 5,544 cohorts and found nothing, liveness 4,355; stride 16, R270's, is
refused against the block reach. A default run there resolves a 61 s floor and
keeps stride 97. The pair is an opt-in test with its record. D-V30A-116.

**R272: ONE CORRUPTION ENTRY POINT, ROWS AGAINST POSITIONS, AND A COMMIT GATE.**
Every instrument that selects cells by time — probe A, L2a, both reaches,
isolation and its split, the identity control — now goes through
`availability.select_cells`, and every one that perturbs through `corrupt_cells`:
one alignment (`to_decision_clock`), an aware/naive comparison that RAISES, and
cells counted per declared frame, with a frame that no sampled position corrupted
getting no reach at all. A totality test over tracked and untracked `src/` fails
on any other site. Reach is reported in rows as well as seconds; the stride counts
positions in the sorted decision seconds, and both reach floors compare rows plus
one against it, so a 60-row window across an overnight gap cannot hold two
cohorts. The head of the frame reads the block reach. `--confirm` runs isolation
and then the split as two predicted stages, and interference exits 5, below
refused and above findings. The commit route refuses a tree no whole-suite run
fingerprinted, and a probe-path change no guard run fingerprinted. D-V30A-118,
D-V30A-119.

**NEXT PROBE-PATH BATCH, ruled R273 §1(f):** `ReachResult.note()` counts every
unusable sample as "censored by the frame's end", including one where nothing
moved; its spread already reports the two apart.
**R270 §0 rulings, recorded.** *"Under an hour" is retired:* it was a
build-or-stop line and never a specification — the cost is measured, printed
and predicted, and nothing is held to a figure. *The prediction prints both
numbers:* time elapsed so far (setup, reach, pass one) beside the passes
remaining at pass one's cost, and a total; "not a promise" covers drift in later
passes and not time already spent. *A complete run measures reach at k = 10*
(`reach.COMPLETE_SAMPLES`), spread across the frame, with every sample printed;
a default run stays at 3. INSTALL's `## Contributing` section is ratified as it
stands: one measured requirement.
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
**Status: NOT STARTED — and its tension is RULED (R269 §3), recorded here with
its substance so the next establish needs no ask.** A profile is a **named
declaration, not a default**. The user names it — `--profile <name>` — and every
value it supplies is printed in ABOUT THIS RUN as `from profile <name>`, **per
key**. Nothing fills silently: the user's act is naming the profile, and the
per-key print makes each filled value theirs to see. **A profile never supplies a
decision column or a decision frame**; those stay required. Built next round,
establish first.
**Why that resolves the tension this item carried:** R236 removed a default that
turned a real leak into `observed_silence`, and a profile silently supplying
`column_roles` would have been that defect with a nicer name. A profile the user
names, whose every filled value is printed, is not silent — and the two values
that decide what a silence even refers to cannot come from one.
**Value:** high for §139's adoption surface, on the terms above.

### F. `align_key`'s timezone cases, enumerated
**Status: PARTIALLY BUILT.** The function ships and refuses the aware/naive
mismatch with a message naming both sides. What is missing is the **cases
document** its siblings have — `LABEL_SCREEN_CASES.md`, `FORK_VOCABULARY_CASES.md`
— enumerating the zone situations before the vocabulary is fixed.
**Value:** low-medium; the refusal already prevents the silent-wrong-answer.
**R273 §1(a) moved the rule, and the status above predates it.**
- R272 §1 made `to_decision_clock` the one alignment, and it converted the
  aware-key/naive-decision case on an unstated UTC assumption.
- R273 ruled the zone a declaration: `decision_timezone`, schema version 5.
- An aware key against naive stamps now converts under a declared zone and is
  refused without one, naming the key.
- A naive key against aware stamps is refused either way.

The cases document is still not written. `tests/phase1/test_decision_timezone.py`
holds the cases built so far: undeclared, declared, a non-UTC zone and the wrong
zone, naive against aware, and both aware.

### G. The export/submodule shadowing repair
**Status: DONE, R273 §1(h).** The modes function is renamed
`column_availability`, with no alias, so `from leakaudit import availability`
returns the module. `tests/phase1/test_export_names.py` checks that every
submodule resolves as a module on the package. The rename is in INSTALL.md's
Changes section. The design record stays at
`evidence/session/EXPORT_SUBMODULE_COLLISION.md`. *Before R273:* designed, and
parked at R238 as an API decision; probed again at R252 from the import-failure
angle.
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
