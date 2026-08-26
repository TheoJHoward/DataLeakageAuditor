# RESULTS_MATRIX.md -- item K6, PREREG.md 9.2 cross-tool comparison

Computed by `harness/score.py` from `raw/`, using only the eligibility and label
mapping fixed in `PRE_RUN_RECORD.md` before any tool ran.

| Tool | C1 T1 | C2 T2 | C3 T3 | C4 T4 | C5 T5 | C6 T6 | C7 T7 | C8 T8 | H | M | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `leak-detect` | abst | abst | abst | abst | miss | miss | abst | abst | 0 | 2 | 6 |
| `deepchecks` | **HIT** | abst | abst | **HIT** | **HIT** | miss | abst | **HIT** | 4 | 1 | 3 |
| `leakage-buster` | miss | abst | abst | miss | **HIT** | abst | miss | abst | 1 | 3 | 4 |
| `Leakly` | abst | miss | miss | abst | miss | miss | abst | abst | 0 | 4 | 4 |
| `leakage-analysis` | abst | abst | abst | abst | abst | abst | abst | abst | 0 | 0 | 8 |
| `LeakageDetector2.0` | abst | abst | abst | abst | abst | abst | abst | abst | 0 | 0 | 8 |
| `OMDS` | miss | **HIT** | abst | abst | abst | abst | abst | abst | 1 | 1 | 6 |
| `temporalcv` | miss | abst | abst | abst | abst | miss | abst | abst | 0 | 2 | 6 |
| `leakfence` | **HIT** | miss | abst | miss | abst | abst | **HIT** | abst | 2 | 2 | 4 |
| `leakr` | abst | abst | abst | abst | abst | abst | abst | abst | 0 | 0 | 8 |
| `bioLeak` | abst | abst | abst | abst | abst | abst | abst | abst | 0 | 0 | 8 |

**Totals (strict reading): 8 hits, 15 misses, 65 abstentions, 88 cells.**

### The one ambiguous cell, scored both ways

`leakfence` x **C4 (T4)**. Its `duplicate_rows` violation fires on **both** sides, so the strict
reading of rule 6.1 makes it a MISS with a false alarm. But the violation TEXT differs:

- contaminated: `2 rows share identical content: (24, 224), straddles train/test`
- clean:        `2 rows share identical content: (24, 124)`   <- no straddle marker

PRE_RUN_RECORD 5.1 declared `leakfence duplicate_rows -> T4` with the note that
`check_duplicates` is called *with* `train_idx`/`test_idx` and "is a cross-split test" -- so the
declared mapping's own subject was the cross-split violation. Reading the straddle marker as the
T4 label is therefore arguably the faithful application of the declared mapping rather than a new
one, and it yields a **HIT**.

Per rule 6.2 the reading that credits the competitor is taken as the headline:

| Reading | leakfence C4 | Totals |
|---|---|---|
| **Conservative (adopted, credits the competitor)** | **HIT** | **9 hits, 14 misses, 65 abstentions** |
| Strict (label-level only) | miss + false alarm | 8 hits, 15 misses, 65 abstentions |

**Neither reading changes any kill-gate verdict** -- leakfence covers T1/T7 (+T4) and does not
reach T6 under either.

### Abstention reasons, per cell

| Tool | Case | Reason |
|---|---|---|
| `leak-detect` | C1 | ineligible (declared before run, item 4) |
| `leak-detect` | C2 | ineligible (declared before run, item 4) |
| `leak-detect` | C3 | ineligible (declared before run, item 4) |
| `leak-detect` | C4 | ineligible (declared before run, item 4) |
| `leak-detect` | C7 | ineligible (declared before run, item 4) |
| `leak-detect` | C8 | ineligible (declared before run, item 4) |
| `deepchecks` | C2 | ineligible (declared before run, item 4) |
| `deepchecks` | C3 | ineligible (declared before run, item 4) |
| `deepchecks` | C7 | ineligible (declared before run, item 4) |
| `leakage-buster` | C2 | ineligible (declared before run, item 4) |
| `leakage-buster` | C3 | ineligible (declared before run, item 4) |
| `leakage-buster` | C6 | crash: internal detector exception Detector error: target_leakage |
| `leakage-buster` | C8 | ineligible (declared before run, item 4) |
| `Leakly` | C1 | ineligible (declared before run, item 4) |
| `Leakly` | C4 | ineligible (declared before run, item 4) |
| `Leakly` | C7 | ineligible (declared before run, item 4) |
| `Leakly` | C8 | ineligible (declared before run, item 4) |
| `leakage-analysis` | C1 | crash: IR generation failed (irgen.py:373 visit_Subscript AssertionError) |
| `leakage-analysis` | C2 | crash: IR generation failed (irgen.py:373 visit_Subscript AssertionError) |
| `leakage-analysis` | C3 | crash: IR generation failed (irgen.py:373 visit_Subscript AssertionError) |
| `leakage-analysis` | C4 | crash: IR generation failed (irgen.py:373 visit_Subscript AssertionError) |
| `leakage-analysis` | C5 | ineligible (declared before run, item 4) |
| `leakage-analysis` | C6 | ineligible (declared before run, item 4) |
| `leakage-analysis` | C7 | ineligible (declared before run, item 4) |
| `leakage-analysis` | C8 | ineligible (declared before run, item 4) |
| `LeakageDetector2.0` | C1 | not programmatically runnable (VS Code extension, no headless entry point) |
| `LeakageDetector2.0` | C2 | not programmatically runnable (VS Code extension, no headless entry point) |
| `LeakageDetector2.0` | C3 | not programmatically runnable (VS Code extension, no headless entry point) |
| `LeakageDetector2.0` | C4 | not programmatically runnable (VS Code extension, no headless entry point) |
| `LeakageDetector2.0` | C5 | ineligible (declared before run, item 4) |
| `LeakageDetector2.0` | C6 | ineligible (declared before run, item 4) |
| `LeakageDetector2.0` | C7 | ineligible (declared before run, item 4) |
| `LeakageDetector2.0` | C8 | ineligible (declared before run, item 4) |
| `OMDS` | C3 | ineligible (declared before run, item 4) |
| `OMDS` | C4 | ineligible (declared before run, item 4) |
| `OMDS` | C5 | ineligible (declared before run, item 4) |
| `OMDS` | C6 | ineligible (declared before run, item 4) |
| `OMDS` | C7 | ineligible (declared before run, item 4) |
| `OMDS` | C8 | ineligible (declared before run, item 4) |
| `temporalcv` | C2 | ineligible (declared before run, item 4) |
| `temporalcv` | C3 | ineligible (declared before run, item 4) |
| `temporalcv` | C4 | ineligible (declared before run, item 4) |
| `temporalcv` | C5 | ineligible (declared before run, item 4) |
| `temporalcv` | C7 | ineligible (declared before run, item 4) |
| `temporalcv` | C8 | ineligible (declared before run, item 4) |
| `leakfence` | C3 | ineligible (declared before run, item 4) |
| `leakfence` | C5 | ineligible (declared before run, item 4) |
| `leakfence` | C6 | ineligible (declared before run, item 4) |
| `leakfence` | C8 | ineligible (declared before run, item 4) |
| `leakr` | C1 | R toolchain could not be installed (machine-wide install requires administrator elevation; user-scope installer not published) |
| `leakr` | C2 | ineligible (declared before run, item 4) |
| `leakr` | C3 | ineligible (declared before run, item 4) |
| `leakr` | C4 | R toolchain could not be installed (machine-wide install requires administrator elevation; user-scope installer not published) |
| `leakr` | C5 | R toolchain could not be installed (machine-wide install requires administrator elevation; user-scope installer not published) |
| `leakr` | C6 | ineligible (declared before run, item 4) |
| `leakr` | C7 | ineligible (declared before run, item 4) |
| `leakr` | C8 | ineligible (declared before run, item 4) |
| `bioLeak` | C1 | ineligible (declared before run, item 4) |
| `bioLeak` | C2 | ineligible (declared before run, item 4) |
| `bioLeak` | C3 | ineligible (declared before run, item 4) |
| `bioLeak` | C4 | ineligible (declared before run, item 4) |
| `bioLeak` | C5 | R toolchain could not be installed (machine-wide install requires administrator elevation; user-scope installer not published) |
| `bioLeak` | C6 | ineligible (declared before run, item 4) |
| `bioLeak` | C7 | ineligible (declared before run, item 4) |
| `bioLeak` | C8 | ineligible (declared before run, item 4) |

### Miss reasons, per cell

| Tool | Case | Type | Reason |
|---|---|---|---|
| `leak-detect` | C5 | T5 | fired on BOTH sides (false alarm on the clean control) |
| `leak-detect` | C6 | T6 | silent on the contaminated side |
| `deepchecks` | C6 | T6 | silent on the contaminated side |
| `leakage-buster` | C1 | T1 | silent on the contaminated side |
| `leakage-buster` | C4 | T4 | silent on the contaminated side |
| `leakage-buster` | C7 | T7 | fired on BOTH sides (false alarm on the clean control) |
| `Leakly` | C2 | T2 | silent on the contaminated side |
| `Leakly` | C3 | T3 | silent on the contaminated side |
| `Leakly` | C5 | T5 | silent on the contaminated side |
| `Leakly` | C6 | T6 | silent on the contaminated side |
| `OMDS` | C1 | T1 | silent on the contaminated side |
| `temporalcv` | C1 | T1 | silent on the contaminated side |
| `temporalcv` | C6 | T6 | silent on the contaminated side |
| `leakfence` | C2 | T2 | fired on BOTH sides (false alarm on the clean control) |
| `leakfence` | C4 | T4 | fired on BOTH sides (false alarm on the clean control) |
