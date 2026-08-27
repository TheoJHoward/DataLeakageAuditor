# W2b STEP 2 — CONTROLS, SEEN TO FIRE. SIX OF SIX DISCRIMINATING.

**27 August 2026. `phase1`.** Step 1 established **reachability** — the packages import and their
entry points are intact. That says nothing about whether they detect anything. **Step 2 asks whether
each tool fires on a documented positive and stays silent on a documented negative.** Until both
limbs pass for a tool, its acceptance-fixture result is **`uninterpretable`, not a null.**

**All six runnable comparators now discriminate.** This discharges §D.5(i)'s precondition. It does
**not** publish any Phase 1 result, and it does not block the tag.

---

## THE COVERAGE TABLE

| tool | version | install channel | vendor negative? | POSITIVE | NEGATIVE | verdict |
|---|---|---|---|---|---|---|
| **Leakly** | 0.1.2 | pip / PyPI index | **YES — the only one** | leaky ordering median AUC **0.635** | clean **0.519** | **DISCRIMINATING** |
| **temporalcv** | 2.3.0 | pip / PyPI index | no | MAE improvement **+0.980 → HALT** | **+0.012 → PASS** | **DISCRIMINATING** |
| **leakfence** | 0.5.0 | pip / PyPI index | no | `group_overlap`; `duplicate_rows` | silent on both | **DISCRIMINATING** |
| **leakage-buster** | 1.0.2 | pip / PyPI index | no | 2 × `high` naming `target_copy` | 0 × `high` | **DISCRIMINATING** |
| **leak-detect** | 0.0.1 | pip / PyPI index | no | returns **True** | returns **False** | **DISCRIMINATING** *(NaN-only mode)* |
| **deepchecks** | 0.19.1 | pip / PyPI index | no | index **1.0000**; corr **1.0000** | **0.0000**; **0.0000** | **DISCRIMINATING** |

**Only Leakly supplied a vendor pair.** For the other five both limbs were constructed here, and
that difference is recorded rather than smoothed over: **a negative we wrote ourselves is weaker
evidence than one the vendor supplied**, because we chose what "clean" means and could have chosen
something the tool does not look at.

## LABEL MAPPING, per tool — the part that decides whether a null means anything

| tool | what counts as a finding | the trap |
|---|---|---|
| Leakly | test AUC above chance **on permuted labels** | on unpermuted data a high AUC is ambiguous — it could be signal |
| temporalcv | `GateStatus.HALT` from an **error** metric | **fed an accuracy, the gate cannot fire** — see below |
| leakfence | a non-empty `Violation` list | `audit_split` returns an object, `check_duplicates` a **tuple** |
| leakage-buster | `severity == "high"` | the clean frame still returns **2 advisory risks**; "any risk" makes every frame positive |
| leak-detect | the **bool return** — `True` | `False` is an *answer*, not an absence |
| deepchecks | `CheckResult.value` above threshold | `FeatureLabelCorrelation` is a **SingleDatasetCheck** — different call signature |

**leakage-buster's `detail` strings are in Chinese.** An adapter keying on English substrings matches
nothing, and an empty match set reads as *no leakage* — the never-fired-reads-as-clean failure.
Severity keys are ASCII and are what the control uses.

---

## TWO FINDINGS ABOUT THE TOOLS

**temporalcv — k6's mapping made the gate unable to fire, and this is now demonstrated.**
`gate_suspicious_improvement` computes `improvement = 1 − (model_metric / baseline_metric)` and its
docstring pins the units: *"model_metric : Model's error metric (lower is better)"*. k6 fed it an
**accuracy**. Fed the identical leakage that way, the gate reports:

> **Improvement −76.4% is reasonable**

Higher-is-better inverts the ratio, so a dramatically better model reads as no improvement at all.
**k6's null was an unfired instrument, not a clean result.** Recorded as a finding about the earlier
run.

**leak-detect — its vendor default is broken against the installed NumPy.** `only_nan=False`, the
default, adds a complex-number pass using `np.complex`, removed in NumPy 1.24; the installed NumPy
is **1.26.4**. It raises `AttributeError` after printing a correct NaN-pass result. The tool works in
**NaN-only mode** and is recorded as discriminating there, with the default's breakage kept as its
own limb — because the default is what an adapter written from the signature would use.

---

## AGPL-3.0-or-later — the deepchecks determination

**deepchecks 0.19.1 is AGPLv3+**, by classifier: `License :: OSI Approved :: GNU Affero General
Public License v3 or later (AGPLv3+)`. *(Its `License` metadata field is literally `UNKNOWN`; the
classifier is the authority.)*

**Determination: interoperation is not vendoring.** deepchecks is invoked **as a separate program in
its own virtualenv**. No deepchecks source is copied into this repository, none is modified, and
nothing is redistributed; the project reads its results as data. **AGPL §13's network clause is not
engaged**, because nothing here offers deepchecks to users over a network.

**This determination lapses if any of those change** — if a later round vendors, modifies or
redistributes it, it must be redone.

---

## FOUR ADAPTER DEFECTS OF MINE — every one would have produced a wrong finding about someone else's software

**Each was caught by checking my own call before recording anything about the tool.** That is the
discipline W2b applies to vendors, turned inward, and it is the reason this section exists rather
than four confident, plausible, false entries in the coverage table.

| tool | what my adapter did | what it would have gone into the record as |
|---|---|---|
| leakfence | read `.violations` off a plain **tuple** | *"`check_duplicates` does not fire on identical rows"* — it had detected them |
| leak-detect | ran the **vendor default**, which crashes | *"leak-detect does not discriminate"* — its default mode is broken, a different fact |
| leak-detect | `ret is not None` on a **bool** return | *"fires on the clean case too"* — `False` is an answer, not an absence |
| deepchecks | passed `train_dataset=` to a **SingleDatasetCheck** | *"the positive did not fire"* — the call never happened |

**A raise is never evidence about a tool; it is evidence the call did not happen.** Every shape
resolver in these controls now **raises on an unrecognised shape** rather than returning empty,
because an empty result reads as *clean*.

---

## WHAT THIS DOES AND DOES NOT ESTABLISH

**Establishes:** each tool's adapter reaches the tool, and the tool separates a documented leak from
a documented clean case **through the same invocation path a real run would use**.

**Does not establish:** anything about the acceptance fixture itself. The fixture results are now
**interpretable where they were not** — reading them back against these controls is the next action
and has not been done here. `could_not_run` → `covered_with_exclusion`, **never a pass**. Zero
comparators run is not a pass (SC-11a).

**Not runnable, not re-litigated:** `leakr` and `bioLeak` need R; `leakage-analysis` needs `souffle`;
`LeakageDetector` is a VS Code extension. All four recorded at k6.
