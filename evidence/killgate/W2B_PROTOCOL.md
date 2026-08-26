# W2b — THE RE-RUN PROTOCOL. Positive controls first, not bug fixes.

**DELTA R58, 21 August 2026. This supersedes "fix the five harness bugs and re-run".**
W2b does not gate the tag; **W2a (re-scoping every C6 citation) did, and is done.**

---

## THE RULE THIS ROUND ADDS

> **A NULL IS UNINTERPRETABLE WITHOUT A POSITIVE CONTROL.**
>
> Before any tool's non-detection on any case is recorded, **that tool's adapter must be
> demonstrated capable of producing a hit** — on a case the tool is documented to catch, run
> through **the same adapter, the same harness, the same invocation path**. A tool that has never
> been shown to fire through its adapter **has not been tested; it has been mishandled**, and its
> silence is evidence of nothing in either direction.

**Leakly is the pure case.** It fired on **0 of 8** cell-sides, including C2 contaminated where its
own `load_example_leakage_config()` was used and the observed AUC was 0.989. No positive control
was ever established for it. That result carries **no information**, and it was reported as a null.

---

## WHY FIXING THE FIVE KNOWN BUGS IS NOT THE TASK

The defects were **not random**. Every one is a different way an adapter can silently disable the
tool it wraps, and **all of them lean toward the answer this project wants**:

| # | defect | how it disabled the tool | direction |
|---|---|---|---|
| 6 | `gate_temporal_boundary` recorded in the config for all 16 cells, **never called** | a mapped T6 gate that never ran | flatters |
| 7 | `gate_suspicious_improvement` fed **accuracy** where the gate's formula expects an **error** metric | a mapped T6 gate that **cannot fire** | flatters |
| 8 | the leakage-buster adapter alone omits `.dropna()`; **C6 is the only case with NaN** | the flagship cell became a crash | flatters |
| 9 | C6's feature is named `win5`; the sole T6-mapped leakage-buster detector gates on a hardcoded substring list `win5` misses | the detector skipped the column | flatters |
| — | Leakly wired into `DATA_IS_THE_CASE`, holding its leakage mechanism constant across sides | the mechanism under test never varied | flatters |

**Fixing these five reproduces the class with different bugs.** The common cause is that nobody
ever asked whether an adapter *could* register a hit — only whether it *did*.

---

## THE PROTOCOL, IN ORDER

**Step 1 — build a positive control per tool.** For each of the eleven, a case the tool's own
documentation or test suite says it catches. Where the tool ships an example (Leakly's
`load_example_leakage_config()`, deepchecks' own test fixtures), use it.

**Step 2 — verify each adapter fires on its control**, through the same adapter, harness and
invocation path the real run uses. **A tool whose adapter does not fire on its own documented
positive is NOT RUN**, and is recorded as NOT RUN — never as an abstention and never as a miss.
This distinction is what §10.1 criterion 2 is about.

**Step 3 — only then run C1–C8**, with the five known defects fixed.

**Step 4 — record every null beside its control.** No non-detection is reported without the
control result on the same line. A null whose control is absent or failing is reported as
**uninterpretable**, not as a negative.

**Step 5 — adversarial adapter read (D3), by an agent that did not write them**, with exactly one
question per tool-case pair: **could this adapter register a hit if the tool found one?** That is
the question nobody asked the first time, and four of the five defects would have fallen out of it
immediately.

---

## WHAT THIS CHANGES ABOUT THE HEADLINE

**Nothing, and that is worth stating.** The kill-gate verdict survives independently: §10.1 is a
five-way conjunction, **criterion 1 fails for all eleven tools** on coverage grounds, and criterion
3 is unevaluated because the acceptance-fixture surface was never run. None of that depends on C6,
on any cell of the matrix, or on any count. **What W2b repairs is the evidence, not the verdict** —
and the evidence is what a hostile reader opens.

**Until W2b completes, no C6 result and no per-tool null from the first run may be cited
load-bearing.** W2a has already re-scoped the three citations that existed.
