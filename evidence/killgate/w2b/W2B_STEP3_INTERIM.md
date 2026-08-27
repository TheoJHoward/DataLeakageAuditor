# W2b STEP 3 — INTERIM. **NO DISCHARGE TABLE. THE RESULTS ARE NOT YET INTERPRETABLE.**

**28 August 2026. `phase1`.** The acceptance fixture is materialised and all twelve runs completed.
**They do not discharge §D.5(i), and publishing a table from them would be wrong** — three of the
four adapters that "ran" did not pose a leakage question at all.

---

## What is solid

**Both sides materialised, one at a time per SC-7(d)** — build, write, drop, `gc.collect()`, then the
other. The harness **halts if the two sides come out byte-identical**, which would mean it built one
side twice.

| side | shape | parquet sha256 | csv sha256 |
|---|---|---|---|
| contaminated | 338,159 × 87 | `b62f5c16…` | `9217e348…` |
| corrected | 338,159 × 87 | `91102e67…` | `383021a7…` |

**The two sides differ**, same 87 columns. Target `fwd_move_ticks_5s`, time column `timestamp`.

## Two tools are `unsupported`, and the two reasons are different

| tool | status | why |
|---|---|---|
| **Leakly** | `unsupported` | it detects by varying **pipeline ORDER** — where `data_split` sits. The fixture is a **built table with no pipeline to reorder**. The tool's question is not posed by this input. |
| **leak-detect** | `could_not_run(compatibility)` | **applicable in principle** — `builder_for()` is exactly the data-creation function it instruments — but the `ld` venv's pandas pin cannot import the fixture builder. A limit of this harness, not of the tool. |

Both map to **`covered_with_exclusion`, never a pass.**

---

## ⚠️ THREE OF THE FOUR "ran" RESULTS ARE ADAPTER DEFECTS, NOT COMPARATOR MISSES

Every tool that ran reported `finding=False` **on the contaminated side** — the side that carries
leakage by construction. That looks like a headline. **It is not, because three of the four adapters
never asked about leakage.**

| tool | what it reported | why it is not a null |
|---|---|---|
| **leakage-buster** | 5 risks, 0 `high`, finding=False | **its risk list contains `Detector error: target_leakage`.** The one detector that would have found target leakage **ERRORED**. A detector error inside a completed run is a `could_not_run` for that detector — **not an absence** — and my severity mapping counted it as neither. It also reports `Time parse errors`. |
| **leakfence** | 0 violations, finding=False | `audit_split` was called with **no `subject` and no `session`**. Its own docstring: *“subject: per-window subject id. **Omit to skip the group check.**”* **The group check was skipped, so the zero is vacuous.** |
| **temporalcv** | improvement −111%, PASS | I compared a **mean predictor** against persistence. That measures whether a trivial model beats persistence — **it poses no leakage question**. The gate is fine; the quantity handed to it was not a leakage signal. |
| **deepchecks** | max PPS **0.0095**, finding=False | **This one did pose a real question.** Feature-label predictive power against `fwd_move_ticks_5s`; the strongest single feature is `fwd_move_ticks_10s` at 0.0095. A genuine, interpretable low result — with the caveat that single-feature PPS is not the only shape contamination can take. |

**So the honest count is one interpretable run out of six tools, not four.**

## What this is an instance of

**It is the W2b thesis applied to my own harness, for the fifth time in this sweep.** A run through an
adapter that does not ask the question is not a null — exactly as a tool fed the wrong quantity never
fires, and never-fired reads as clean. The controls established that these tools *can* fire; they
said nothing about whether *this* invocation asks them to.

**And the first sweep made the same point louder:** all twelve runs returned `could_not_run` on one
shared cause — **none of the three virtualenvs carries a parquet engine**, so `read_parquet` raised
before any tool was reached. **Twelve agreeing failures were one failure.** Installing an engine was
**refused**: the W2b inventory pinned those versions on 14 Aug 2026 **before any result was read**,
and adding packages would alter the environment the record attests. The inputs were rewritten as CSV.

## What step 3 still needs

1. **leakage-buster** — establish why `target_leakage` errors, and record it as `could_not_run` for
   that detector rather than folding it into a severity count.
2. **leakfence** — supply a grouping the fixture actually has (a session or time-bucket key), or
   record that the tool's group check is **unposable** on this input and say so.
3. **temporalcv** — hand it a model error that could plausibly reflect leakage, or record the gate as
   **unposable** on a fixture with no model attached.
4. **leak-detect** — either serve the builder across a process boundary or record the compatibility
   exclusion as final.
5. Only then a discharge table.

**`could_not_run` → `covered_with_exclusion`, never a pass. Zero comparators run is not a pass
(SC-11a) — and neither is four comparators run through adapters that asked nothing.**
