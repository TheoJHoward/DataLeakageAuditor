# §9.2 — DISCHARGE ASSESSMENT AGAINST `AVAILABILITY_DECLARATION.md` §D.5(i)

**What this file is.** §D.5(i) records the §9.2 cross-tool comparison as a named open obligation
and states the terms on which it discharges. This file maps those terms onto what already exists,
names what remains, and supplies the recording format the terms require. **It does not run
anything and it changes no verdict.**

**Why now.** §D.5(i) makes the obligation due *before any Phase 1 result is published*, and Probe
B's column dependency map (`evidence/phase1/probe_b_merged.json`) is exactly such a result. The
obligation therefore sits on the critical path rather than ahead of it.

---

## 1. THE DISCHARGE TERMS, QUOTED

> **DISCHARGE:** each named comparator has been run against the acceptance fixture with its own
> positive control (W2b) and its findings recorded per tool. A comparator that cannot run is
> recorded could-not-run with the reason and counts as covered-with-exclusion, never as a pass.
> **Zero comparators run is not a pass** (SC-11a).

Four requirements: a **named** comparator set; a run against **the acceptance fixture**; a
**positive control per tool**; and a **per-tool record** with a could-not-run disposition.

---

## 2. WHAT ALREADY EXISTS — and it is most of the apparatus

| term | where | state |
|---|---|---|
| named comparator set, with eligibility declared **before** any run (§9.2 item 1) | `CROSS_TOOL_COMPARISON.md` §2.3 | **9 included, 6 excluded with reasons**; per tool × case eligibility matrix |
| versions and configuration (item 2) | `CROSS_TOOL_COMPARISON.md` §2.4, `k6/PRE_RUN_RECORD.md` §2.1, §2.3 | recorded, with install channel and dependency pins |
| label mapping fixed before running (item 3) | `CROSS_TOOL_COMPARISON.md` §2.5 | committed |
| abstention and crash scoring (items 4, 5) | `CROSS_TOOL_COMPARISON.md` §2.6 | committed |
| manual setup recorded (item 6) | `k6/PRE_RUN_RECORD.md` | four dependency pins recorded for `deepchecks` alone |
| no case excluded after results are seen (item 7) | `CROSS_TOOL_COMPARISON.md` §2.3 | committed, with a scope flag raised for the author on whether it binds *tool* exclusions too |
| **positive control per tool** | `W2B_PROTOCOL.md` steps 1–2 | **protocol written, NOT executed** |
| licence determination | `LICENCE_CHECK.md` row 2 | `deepchecks` **AGPL-3.0-or-later**, sourced from the PyPI classifier |

**The apparatus §9.2 requires be fixed before running is fixed.** What is missing is execution, and
one precondition.

---

## 3. WHAT REMAINS

**3.1 The executed run is against the wrong surface for this discharge.** `CROSS_TOOL_COMPARISON.md`
§2.1 names two surfaces and states they are not interchangeable: the **acceptance fixture**
(`fixture_contaminated` / `fixture_corrected`), and the **prior-art comparison set** (the eight
hand-written cases C1–C8). The k6 run executed the **comparison set**. §D.5(i)'s discharge names
the **acceptance fixture**. The existing run therefore does not discharge §D.5(i), whatever its
quality.

**3.2 The existing run's evidence is under repair, and its own protocol says so.**
`W2B_PROTOCOL.md` records five known defects and rules that fixing them is *not* the task: the task
is positive controls first. Its step 4 is the load-bearing one — **no null is reported without its
control result on the same line, and a null whose control is absent or failing is reported
uninterpretable, not negative.** Until W2b completes, no per-tool null from the first run may be
cited load-bearing.

**3.3 The precondition on the fixture surface has NOT cleared.** `PREREG.md` line 448 orders
reconstruction before the comparison, and §2.1 reads the declaration's own DRAFT header as the
blocker. **That header is still present** — see §5.

---

## 4. THE PER-TOOL RECORDING FORMAT

One row per tool per case. **A null is never recorded without its control on the same row**, which
is W2b step 4 made structural rather than remembered.

| field | values | note |
|---|---|---|
| `tool`, `version`, `install_channel` | — | item 2 |
| `case` | fixture side, or C1–C8 | the surface is named, never inferred |
| `eligible` | `E` / `I` | from the pre-declared matrix only; never re-decided after a result |
| `control_result` | `fired` / `did_not_fire` / `absent` | W2b step 2 |
| `outcome` | `detected` / `null` / `abstention` / `could_not_run` / `uninterpretable` | see below |
| `reason` | free text | **required** for `could_not_run` and `uninterpretable` |
| `coverage` | `covered` / `covered_with_exclusion` | `could_not_run` ⇒ `covered_with_exclusion`, never a pass |

**Outcome selection, in order:**

1. `control_result` is `did_not_fire` or `absent` → **`uninterpretable`**, regardless of what the
   tool reported on the case. A tool whose adapter does not fire on its own documented positive is
   NOT RUN (W2b step 2), and a null from it is evidence about the adapter.
2. eligibility `I` → **`abstention`** (§9.2 item 4).
3. the tool crashed → **`abstention`**, counts published (item 5).
4. the tool could not be installed or invoked at all → **`could_not_run`** with the reason;
   `coverage = covered_with_exclusion`.
5. otherwise **`detected`** or **`null`**.

**SC-11a is a floor on the whole table, not a per-row rule:** zero comparators run is not a pass.
A table in which every row is `could_not_run` discharges nothing.

---

## 5. FINDING — RECORDED, NOT FIXED

**The declaration's own status header still reads DRAFT, in the tree the tag attests.**

`AVAILABILITY_DECLARATION.md` line 29–31, on `main` at the tag target:

> **## DRAFT — AUTHOR REVIEW REQUIRED**
>
> Status: DRAFT. **Nothing in this file is a registered declaration.** Every element below is a
> reconstruction from archive evidence …

Nothing later in the file lifts it. The only nearby statement about draft-ness — "after the
author's review the file is not a draft, and its name still …" — is about the **fixture manifest's
filename**, not this file's header.

**Why it matters here.** §2.1 cites exactly this header as what blocks a fixture-surface run, so
§9.2's discharge is blocked by it.

**Why it matters beyond here.** The same file carries §D.1's freeze, §D.2's hash enumeration,
§D.5's named open obligations and §D.6's disclosures, and the tag hashes it. SC-7(a) gives a
detector "the availability declaration's **declared elements**"; SC-8(f) calls it the file that
"carries the scoring key". A reader with only the signed object finds those sections under a header
saying nothing in the file is declared.

**An asymmetry worth naming.** SC-4(k2) required the *fixture manifest's* recorded status not be
`DRAFT` at the tag, and that was enforced and cleared. No equivalent check existed for the
**declaration's own** status — the file that carries the scoring key.

**This is NOT fixed here, and that is deliberate.** The registration closed to pre-tag fixes when
the ceremony's final pass reported green. This is a disclosure, not a repair. It cannot be entered
in `DEVIATIONS.md` before the tag either: that file is one of the paths the tag message enumerates,
so editing it would invalidate the hash set the final pass verified. **The entry lands after the
tag is signed and pushed.**

---

## 6. WHAT WOULD DISCHARGE §D.5(i)

In order, none of it startable before the header question above is ruled on:

1. Author ruling on the DRAFT header — it gates the fixture surface by §2.1's reading.
2. W2b steps 1–2: a positive control per tool, verified **through the same adapter and invocation
   path the real run uses**.
3. The fixture-surface run, one side at a time — SC-7(d) makes that a hard sequencing rule, and a
   single run given more than one side satisfies no criterion however its outputs are partitioned
   afterwards.
4. The per-tool table of §4, with every null beside its control.
5. A `DEVIATIONS.md` entry if any comparator is `could_not_run`, naming it and its reason.
