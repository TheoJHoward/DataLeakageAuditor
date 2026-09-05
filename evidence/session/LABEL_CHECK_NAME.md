# `check_label_under_another_name` — rename or extend, both costs

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures.

**The finding this reports on.** R226 §2: the check's name is a false statement
about its behaviour in the user-facing surface. It tests near-exact **linear**
duplication of **single** columns; its name claims it finds the label under
another name. `evidence/session/LABEL_SCREEN_CASES.md` measured the gap — `y**3`,
a perfect invertible rank-preserving copy of a label, screens at `|r| = 0.762`
and passes at every threshold tried. **The threshold was the wrong dial**, which
is what makes this a naming decision rather than a configuration one.

**This file reports; it does not pick.** R226 §2 puts the choice to the author.

---

## Option A — rename the check to what it does

**What it costs.** The name appears at **21 sites across 5 files**
(`python -c "..."` over `grep -rn label_under_another_name --include=*.py
--include=*.md`, excluding `.git`, `build/` and `__pycache__`):

| file | what the name is doing there |
|---|---|
| `src/leakaudit/checks.py` | the function, the `check=` field that renders, the module docstring's registered-row accounting |
| `src/leakaudit/__init__.py` | **the public API export** — the one genuinely breaking site |
| `tests/phase1/test_checks.py` | six tests naming it |
| `tests/phase1/test_default_sites.py` | the defaults classification key |
| `evidence/session/LABEL_SCREEN_CASES.md` | the cases record |

**The real cost is the export.** Anyone importing `check_label_under_another_name`
from `leakaudit` breaks. The package has no released version and no known
external caller, so today that cost is nominal — and it will not be nominal
later, which is an argument for deciding now rather than deferring.

**A second cost, less obvious.** `checks.py`'s docstring maps each built check to
its registered row, and this one is filed as *"L2b's NEIGHBOURHOOD"*. A rename
has to keep that mapping legible: the new name still has to be recognisable as
the neighbour of the registered row, or the accounting stops being readable.

**Candidate names, and what each would then be true of:** `check_label_copied_linearly`,
`check_feature_correlates_with_label`, `check_near_duplicate_of_label`. Each is
narrower and each is *true*.

---

## Option B — extend the check to do what it says

**Rank correlation catches every monotone copy Pearson misses.** Spearman is
Pearson on the ranks, so a copy under any strictly monotone transform screens at
exactly 1.0.

**Is it cheap on the real frames? YES — measured at the acceptance fixture's
actual shape**, 338,159 rows × 29 features (`evidence/phase1/criteria_12_run.json`,
`declared_map_cells.*.rows`), CPython 3.12.10, numpy 2.4.2, pandas 3.0.1, best of
three:

| what | time |
|---|---|
| Pearson, 29 columns — what ships today | **0.097 s** |
| Spearman, 29 columns, `Series.corr(method="spearman")` | 2.819 s |
| Spearman, ranking each column once then Pearson on the ranks | **1.409 s** |
| the whole check today, end to end | 1.291 s |

**So the extension roughly doubles the check, from ~1.3 s to ~2.7 s, on the
largest frame this project has.** That is cheap by any reading, and R226 §2(b)'s
condition for not shipping a weak version is not met — there is no reason to ship
a weak version, because the strong one is affordable.

**And the discriminating positive already exists and already passes.** On the
same frame:

| | `y**3` against `y` |
|---|---|
| Pearson | 0.76213 — **missed** |
| Spearman | 1.00000 — **caught** |

That is R226 §2(c): a case the current check misses and a correct one catches,
produced by asking about a threshold. It needs no construction.

**What extending would NOT fix, stated so the option is not oversold.** The check
compares **single columns**. A label reconstructed from two features together is
invisible to Pearson and to Spearman alike. So Option B narrows the gap between
the name and the behaviour without closing it, and a check named
`label_under_another_name` would still be overstating — less, but still. Only a
name change makes the name true; only an extension makes the check better; they
are not substitutes.

---

## What was done regardless of the choice

**The silence stopped overstating itself.** R226 §2(d). `CheckResult` carries
`silence_is_about`, and the found-nothing sentence prints it:

> `label_under_another_name: nothing found over 29 column(s) against the label
> 'y', at a Pearson screen of |r| >= 0.999. The check ran.`
> `THIS SILENCE IS ABOUT NEAR-EXACT LINEAR DUPLICATION OF ONE COLUMN, and
> nothing wider. …`

**The field is not decoration and a test enforces that.** It is set only where a
check's name is broader than its test; `tests/phase1/test_silence_frame.py`
asserts the accurately-named checks carry none, which is the discriminating
negative — if every check acquired one, the field would stop marking a specific
known gap.

**And a `finding` does not carry it.** The scope qualifies a silence. Appending
it to a positive result would read as a hedge on a result that is not hedged.
