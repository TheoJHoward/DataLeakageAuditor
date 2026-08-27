# W2b STEP 3 — THE DISCHARGE TABLE. §D.5(i) **DISCHARGED**.

> **B-3, 28 August 2026 — the controls were re-run through the FINAL adapter path and all four
> hold.** R149 §1.2: the step-2 controls each called their tool directly, and three adapters were
> then rebuilt, so those controls no longer tested what the measurement does. A positive/negative
> pair was pushed through `b2_run_one.py` itself — same CLI, same adapters, same CSV transport and
> dtype sidecar the fixture rows used.
>
> | tool | positive | negative | |
> |---|---|---|---|
> | leakage-buster | **fires** | silent | holds |
> | leakfence | **fires** | silent | holds |
> | temporalcv | **fires** | silent | holds |
> | deepchecks | **fires** | silent | holds |
>
> **The first attempt did NOT hold, and the defect was in the CONTROL.** temporalcv HALTed on the
> clean frame — correctly and with no leakage present: the negative used an **iid** target, and for
> an iid series the mean predictor alone beats persistence by **~29%** (E|y−μ| = 0.798σ against
> E|y_t − y_{t−1}| = 1.128σ), tripping the gate's own 20% threshold on arithmetic. **A control must
> be drawn from the regime the measurement operates in**; the fixture's target has lag-1
> autocorrelation **0.794**, so the control was rebuilt at φ = 0.79 and now holds.
>
> **Two things came out of that.** The adapter now **measures the gate's precondition and declares
> its own domain**: if the mean predictor already beats persistence past 0.20, any HALT is
> arithmetic rather than evidence and the tool is recorded `unsupported` on that target. On the
> fixture the precondition is **−1.195** — persistence is far stronger than the mean predictor — so
> the gate is in its intended regime and the row stands. **The fixture sweep was re-run through the
> final adapter and every verdict below is unchanged.**
>
> **`gate_suspicious_improvement` is only interpretable where persistence is a strong baseline.**
> That is a real limit of the tool, found by controlling it, and it is recorded here rather than
> discovered later by someone trusting a HALT.

---


**28 August 2026. `phase1`.** Adapters rebuilt to R148 §1.3's standard — each tool's best shot —
and re-run against both sides of the acceptance fixture. **This table states what each row is
evidence OF.** Four tools now pose a real question; two cannot be posed at all.

**Headline: no tool distinguishes the contaminated side from the corrected side.** That is not the
same as "no tool reported anything" — one reports on both.

---

## THE TABLE

| tool | version | channel | vendor negative | contaminated | corrected | separates? | what the row is evidence OF |
|---|---|---|---|---|---|---|---|
| **leakage-buster** | 1.0.2 | pip/PyPI | no | **finding=True** — 2 HIGH | **finding=True** — same 2 HIGH | **NO** | its HIGH risks (`Target Encoding leakage risk`, `WOE leakage risk`) are **identical on both sides**, so they describe encoding structure the fixture has throughout — **not** the contamination |
| **leakfence** | 0.5.0 | pip/PyPI | no | dup 0; group **unposable** | dup 0; group **unposable** | **NO** | the **duplicate** check ran on 84 numeric columns and its zero is a real result; the **group** check is unposable and contributes nothing either way |
| **temporalcv** | 2.3.0 | pip/PyPI | no | improvement **−2.04** → PASS | **−2.07** → PASS | **NO** | armed and answering: a Ridge fit on 80 features **does not beat persistence** on either side, so there is no suspicious improvement to flag |
| **deepchecks** | 0.19.1 | pip/PyPI | no | max PPS **0.023** | max PPS **0.046** | **NO** | no single feature predicts the 5s target above 0.05 — and the **corrected** side scores *higher*, the opposite of a leakage signal |
| **Leakly** | 0.1.2 | pip/PyPI | **YES** | `unsupported` | `unsupported` | — | detects by varying **pipeline order**; a built table has no pipeline to reorder. **The question is not posed by this input.** |
| **leak-detect** | 0.0.1 | pip/PyPI | no | `could_not_run` | `could_not_run` | — | **applicable in principle** — `builder_for()` is exactly the data-creation function it instruments — but the `ld` venv's pandas pin cannot import the builder. **A limit of this harness, not of the tool.** |

Both `unsupported`/`could_not_run` rows map to **`covered_with_exclusion`, never a pass.**

## WHAT CHANGED FROM THE INTERIM, AND WHY IT MATTERS

The interim reported **one** interpretable run of six. Three adapters were fixed to R148 §1.3:

| tool | the defect | the fix, and what it cost |
|---|---|---|
| **leakage-buster** | its `target_leakage` detector **errored** (`Input y contains NaN`, then `Input X contains NaN`) and the error was folded into a severity count that read `finding=False` | **complete-case on all 87 columns, no feature removed.** Dropping the NaN-heavy columns would have been easier and is **refused** — dropping a feature could drop the leaky one. Cost: **93,646 of 338,159 rows** survive (28%), so its verdict is about the complete-case subset |
| **leakfence** | `audit_split` called with **no subject**, which its docstring says skips the group check | armed with `ts_floor` — **and that was a second vacuous zero**: `ts_floor` is unique per row, so every row was its own group. **The fixture has no subject grouping**, so the group check is now recorded **unposable** rather than reported as a clean zero |
| **temporalcv** | fed a **mean-predictor-vs-persistence** comparison, which contains no leakage question | a **Ridge model fit on 80 features**, chronological 80/20, scored as MAE against persistence — the shape its own fired control used. Sibling `fwd_move_ticks_*` columns are **excluded**, since leaving them in would manufacture leakage the fixture did not put there |

**A verdict that hinges on a dtype the transport changed is a verdict about the transport.** The CSV
round-trip turns `timestamp` and `ts_floor` into strings — which is why leakage-buster reported
`Time parse errors`. Datetimes are now restored on read from a sidecar **derived from the parquet**.
The only other dtype movement is `minutes_since_open` int32→float64 on the **corrected** side, and
that is **not** a transport artifact: `apply_universal_lag` produces exactly one null at the head.

## CAVEATS THAT BEAR ON READING THIS TABLE

- **The tools did not all see the same rows.** leakage-buster and temporalcv ran on the
  complete-case subset (~93.6k); deepchecks and leakfence saw the full frame. A cross-tool
  comparison of *counts* would be invalid; a comparison of *contaminated vs corrected within one
  tool* is what this table makes.
- **One target, one horizon.** `fwd_move_ticks_5s`, per the registered Phase 5 ZC pairing. Other
  horizons are not run.
- **Zero comparators run is not a pass (SC-11a), and neither is this.** Four armed questions and no
  separation is a *result*, not a clearance.

## AGPL-3.0-or-later — deepchecks, recorded

deepchecks is **AGPLv3+ by classifier** (its `License` metadata field reads `UNKNOWN`; the
classifier is the authority). **Interoperation is not vendoring**: it is invoked as a separate
program in its own virtualenv, no source is copied into this repository, none is modified, nothing
is redistributed, and §13's network clause is not engaged. **The determination lapses if any of that
changes.**

---

## WHAT THIS DISCHARGES, AND WHAT IT DOES NOT CLAIM

**§D.5(i) IS DISCHARGED.** Every runnable comparator was shown to fire on a documented positive
(step 2), run against the acceptance fixture through an adapter that poses its question (step 3),
and — decisively — **its control re-run through the final adapter path** (B-3), because three
adapters were rebuilt after step 2 and a control that does not exercise the measurement's path has
not tested the measurement. The nulls are therefore **interpretable**: they are misses, not unfired
instruments. **The publish-block on B8/B9's results lifts.**

**Three failure modes, one conclusion.** A tool that fires identically on both sides
(leakage-buster) fails the pair exactly as one that passes both (temporalcv, leakfence) or points
the wrong way (deepchecks). **Constant firing is not detection**, and no row here should be read as
one tool having found the contamination.

**The empirical case, stated as carefully as it deserves.** Probe B found the fixture's
contamination by NaN propagation. Four independent shipping tools, each demonstrated to fire on its
own documented positive, **do not separate the contaminated side from the corrected one** — and a
fifth would be applicable if a pandas pin allowed it.

**The claim is only as strong as the adapters are fair.** Three of them were wrong in the first
sweep and produced a plausible, publishable, false result; they were corrected toward the tools'
best shot, and the corrections are in the table above rather than in a footnote. **A reader who
thinks a fairer adapter exists for any row should say so — that is the row's real error bar.**

## THE ROW THAT IS MISSING — this project's own tool

**Six external tools, none separating the pair, and no row showing that ours does.** The comparison
is asymmetric until that row exists, and a reader will ask for it first. It is **not** filled in
here: what "separates" means for our tool is a design question, not a measurement — the dependency
map may look alike on both sides, the difference living in availability verdicts, and SC-7
constrains what the tool may be given (never the map).

**Proposed before built**, on the `aggressor_side` precedent. Until that row exists, this table
establishes what the external tools do **not** do, and claims nothing about what ours does.
