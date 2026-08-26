# PHASE 1 BRIEF — what exists, quoted

**Scope.** Gathered and quoted only. **Nothing here designs anything**; every substantive statement
is a quotation or a measurement, and where the corpus is silent that silence is reported rather than
filled.

---

## (a) `DESIGN.md`'s Phase 1 section

**There is no Phase 1 section in `DESIGN.md`.** A search for a Phase 1 heading returns nothing; the
only two mentions are in passing:

- l.78 — *"The comparator and its default are `PREREG.md` §2.3 and are not restated here; this file
  specifies where the mask is built and cached."*
- l.192 — *"Expected calibration, **to be checked at Phase 1** (`PREREG.md` §0.3 Claim B): a
  trailing window including the decision bar → **one bar**…"*

**This is what the deferred item §39 exists to fix.** `evidence/session/DEFERRED_ITEMS.md` records a
Phase 1 requirement for `DESIGN.md` — publish the detection domain and what the tool cannot see —
together with §72.2 (a documented lesson is not a control) and §139 (the declaration is the adoption
surface). **All three are recorded, none executed.** So Phase 1's design surface is, at this moment,
three recorded requirements and no section to put them in.

Phase 0's own definition lives in `PREREG.md` §10's phase table, not in `DESIGN.md`.

---

## (b) `protocol/runtime_reference.py` — what it is

**A reference implementation of the runtime protocol's reducers. Not a stub, not a spec, and not a
detector.** 871 lines. Its own docstring:

> Reference reducers for the leakaudit runtime protocol.
>
> Normative source: PREREG.md v30. This module is built FROM that file and is checked AGAINST it
> (PREREG §6.6.1). It is pure protocol tooling: **no I/O, no randomness, no pandas, no detector
> implementation.** Where this module and the prose disagree, the disagreement blocks the tag and is
> routed per the build protocol — **the reducer detects, it does not adjudicate.**

**Public surface**, by kind:

| kind | members |
|---|---|
| exception | `ProtocolViolation` |
| enums | `PromotionStatus`, `RunContext`, `FailureReason`, `ScheduleStateKind`, `EvidenceOutcome` |
| records | `ScheduleState`, `FindingRecord`, `ExecutionRecord`, `CombinationTrace` |
| reducers | `resolve_schedule_state`, `resolve_evidence_outcome`, `check_pair_legal`, `resolve_state_pair`, `derive_evidence_events`, `derive_reported_findings`, `compute_runtime_metrics`, `apply_runtime_gates`, `evaluate_runtime_assertions` |

It carries **fifteen requirement IDs** mapping PREREG clauses onto functions — `R6.6-SCHEDULE-RESOLUTION`,
`R7.2-PROOF-YIELD`, `R10.2-RUNTIME-GATES`, `R8.3-PROVEN-ASSERTION` and eleven more — and the gate's
`requirement_ids` check asserts that set is exactly present.

**What it means for Phase 1:** the measurement semantics are already implemented and test-covered.
What does not exist is anything that *produces* the findings these reducers consume.

---

## (c) §6.2's criteria, as amended — the acceptance spec

From the applied `PREREG.md`:

> 1. **Every** ground-truth leaking source column receives at least one **primary runtime finding**,
>    whether its promotion status makes the reported tier PROVEN or REVIEW.
> 2. No **manifest-clean** source column receives **any runtime finding of any tier, primary or
>    secondary**, on `fixture_contaminated`.
> 3. *(replaced by SC-3)* **Runtime findings on every fixture side are scored against the fixture's
>    DECLARED GROUND-TRUTH MAP — v30a, operative.** The map is *"an enumeration of expected
>    findings, declared in the fixture's availability declaration, stated per side, per declared
>    violation class, and per declared cell."* Its three dispositions are **mutually exclusive and
>    exhaustive**: a finding the map predicts is **REQUIRED** (absence is a miss); a finding the map
>    excludes is a **FALSE POSITIVE** (fails the gate, any side, any tier); a cell the map does not
>    cover is **UNSCORED** — *"never reported as a pass."*
> 4. Silent under the identity control on both.

**Criterion 3 is the one that changed, and it changed direction.** Before v30a it required *silence*
on the corrected side; it now requires findings to **match the map**, and *"a tool silent where the
map declares a violation is silent where it should fire."*

---

## (d) Tool code that exists today

| path | lines | what it is |
|---|---|---|
| `protocol/runtime_reference.py` | 871 | the reference reducers — §(b) above |
| `protocol/__init__.py` | 0 | package marker |
| `tools/check_registration.py` | 2,635 | the registration gate: 23 checks, D1–D16 |
| `tools/control_char_scan.py` | 166 | standalone control-character scanner, superseded by D12, declared ephemeral |
| `tests/registration/traces.py` | 657 | the exhaustive trace suite's trace constructors |
| `tests/registration/test_checker.py` | 434 | tests over the gate itself |
| `tests/registration/test_invariants.py` | 376 | protocol invariants |
| `tests/registration/generate_expected_outputs.py` | 186 | expected-output generator |
| `tests/registration/test_traces.py` | 147 | trace-suite tests |
| `tests/registration/test_expected_outputs.py` | 15 | golden-output comparison |
| `tests/registration/conftest.py` | 7 | pytest fixture wiring |
| **`evidence/killgate/k6/harness/case_defs.py`** | 320 | the C1–C8 case table, both sides, as executable cases |
| **`evidence/killgate/k6/harness/score.py`** | 253 | HIT/MISS/ABST scoring, fixed before the run |
| **`evidence/killgate/k6/harness/run_general.py`** | 183 | generic tool runner |
| **`evidence/killgate/k6/harness/make_scripts.py`** | 182 | per-tool script generation |
| **`evidence/killgate/k6/harness/run_deepchecks.py`** | 122 | deepchecks adapter |
| **`evidence/killgate/k6/harness/run_leakly.py`** | 105 | Leakly adapter |
| **`evidence/killgate/k6/harness/run_leakdetect.py`** | 82 | leak-detect adapter |
| **`evidence/killgate/k6/harness/materialize.py`** | 65 | writes the cases to CSV + hashes them |

**Total: ~6,400 lines, and none of it is a detector.** The gate, the reducers, the tests and the
cross-tool harness all exist; the thing they are built to check does not.

---

## (e) What the fixture offers to develop against

**Two sides.** `fixture_contaminated` and `fixture_corrected`. Per SC-3(g), *"a side the declaration
characterizes is **CHARACTERIZED, never clean**, and no report describes it as clean."*

**The declared ground-truth map** — `evidence/fixture_spike/n1/declared_map.csv`:

| | |
|---|---|
| rows | **984** |
| columns | `side`, `instrument`, `month`, `class`, `boundary`, `strict_count`, `equal_count`, `rows`, `scored_flag` |
| `SCORED` | **888** |
| `UNSCORED_FOR_LACK_OF_DATA` | **72** |
| `SCORED_DIAGNOSTIC_11TH_CLASS` | **24** |

**888 + 72 = 960 cells of the declared scored population**; the 24 diagnostic rows are *"not cells of
the map"* per SC-3(a) — they *"are adjudicated by no criterion, enter no denominator and no rate."*
SC-3(a) is explicit that a count taken from the artifact without excluding them *"counts a different
population."*

**How a candidate is scored:** against criteria 1–4 above, on the frozen default configuration, under
the reconstructed declaration. Criterion 3 is the map comparison; criterion 1 has its denominator
constituted by SC-4's scored-set partition rather than inferred.

**What is NOT available to a developer:** the fixture itself. §AC item 5 — *"The map ships; the
fixture does not."* It is **64 stored-prediction parquets per side, outside the repository**, and *"a
third party can read the map, the declaration and any published reconciliation, and cannot
independently run a candidate against `fixture_contaminated` / `fixture_corrected`."*

---

## (f) How the k6 harness hands the fixture to each tool

**This is the closest thing in the repository to a real user's setup**, and it is worth reading
before designing an interface, because it is eleven recorded attempts at exactly that problem.

`case_defs.py`'s own docstring states the contract. Every case exposes, **for each of two sides**:

> - `raw`            : the raw input frame a feature builder consumes
> - `build(raw)`     : the feature-construction callable (**leak-detect's `data_creation_func`
>   surface**)
> - `full`           : the built frame (features + target + any group/time columns)
> - `train_idx/test_idx` : positional index arrays into `full`
> - `meta`           : feature cols, target col, group col, time col, ground truth

**So the answer to "paths, a loaded frame, or a callable" is: all three, deliberately.** The harness
offers a raw frame, a built frame, index arrays, *and* a construction callable, because the eleven
tools do not agree on what to accept — and `run_leakdetect.py` exists separately precisely because
`leak-detect` takes the callable while the others take frames.

**Two properties of the setup worth carrying into Phase 1:**

- **Materialisation is once and hashed.** `materialize.py`: *"Run ONCE, before any tool is executed.
  The hashes fix the case set for item 7 (**'No case excluded after results are seen'**)."*
- **Scoring was fixed before the run.** `score.py`: *"using ONLY the eligibility and label mapping
  fixed in `PRE_RUN_RECORD.md` before any tool ran"*, with **HIT** = fires on contaminated **and**
  silent on clean; **MISS** = silent on contaminated, or fires on both; **ABST** = ineligible or
  crashed, with a recorded reason.

**The ground-truth convention, verbatim:** *"side 'contaminated' → the leakage of the case's type IS
present. A tool eligible for the case SHOULD fire."*

**Determinism:** *"every case seeds its own numpy Generator. No global seed state is relied on."*
