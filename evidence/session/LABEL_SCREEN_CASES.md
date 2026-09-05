# The label screen's threshold — its cases, measured before any key exists

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures. This is a Phase 2 instrument report.

> **SUPERSEDED IN PART AT R231 §5, and left in place.** The check is now
> `check_pairwise_label_correlation` and screens under Pearson **and Spearman**.
> The Pearson-only tables below are what produced that decision and are the record
> of it; the two-statistic measurement is appended at the end of this file. A
> dated measurement is not rewritten to carry a later result.

**What this file is for.** `check_label_under_another_name` (as it was then)
screens each feature against the declared label at Pearson `|r| >= 0.999`. R222's defaults instrument
put that number in the **should_refuse** set as a candidate: a threshold the user
cannot see, which did not appear in the check's own output, so a silence it
produced was a figure without its frame. R224 §4 item 1 split the repair in two —
**the mandatory half** (name it) and **the cases, reported before any key**. This
is the second half, and it is written first on purpose: a configuration key whose
cases nobody has measured hands the user a number and no way to choose it.

**The mandatory half is done and is not conditional on this file.** The check's
population line now reads `… at a Pearson screen of |r| >= 0.999`, so the
threshold is in the output on every run including the silent ones, and a second
note states what the screen cannot see.

---

## The measurement

2,000 rows, seeded (`default_rng(19)`), one continuous label and one binary
label, each case a single feature column screened on its own. `FIRE` means the
check reported the column as a candidate at that threshold.

### A continuous label

| case | \|r\| | 0.999 | 0.990 | 0.950 | 0.900 | 0.800 |
|---|---|---|---|---|---|---|
| exact copy | 1.00000 | FIRE | FIRE | FIRE | FIRE | FIRE |
| affine rescale `3y+7` | 1.00000 | FIRE | FIRE | FIRE | FIRE | FIRE |
| **monotone non-linear copy `y**3`** | **0.73936** | — | — | — | — | — |
| monotone non-linear copy `sign(y)*sqrt(|y|)` | 0.96285 | — | — | FIRE | FIRE | FIRE |
| `rank(y)` | 0.97747 | — | — | FIRE | FIRE | FIRE |
| `y` + noise (sd 0.02) | 0.99979 | FIRE | FIRE | FIRE | FIRE | FIRE |
| `y` + noise (sd 0.05) | 0.99868 | — | FIRE | FIRE | FIRE | FIRE |
| `y` + noise (sd 0.10) | 0.99449 | — | FIRE | FIRE | FIRE | FIRE |
| `y` + noise (sd 0.30) | 0.95823 | — | — | FIRE | FIRE | FIRE |
| unrelated feature | 0.02068 | — | — | — | — | — |

### A binary label

| case | \|r\| | 0.999 | 0.990 | 0.950 | 0.900 | 0.800 |
|---|---|---|---|---|---|---|
| exact copy | 1.00000 | FIRE | FIRE | FIRE | FIRE | FIRE |
| copy as float | 1.00000 | FIRE | FIRE | FIRE | FIRE | FIRE |
| `1 - y` (perfect inverse) | 1.00000 | FIRE | FIRE | FIRE | FIRE | FIRE |
| `y` with 1% of labels flipped | 0.98100 | — | — | FIRE | FIRE | FIRE |
| `y` with 5% of labels flipped | 0.90911 | — | — | — | FIRE | FIRE |
| unrelated feature | 0.03058 | — | — | — | — | — |

---

## What the cases say

**THE THRESHOLD IS NOT THE INTERESTING VARIABLE. THE STATISTIC IS.** `y**3` is a
*perfect* copy of the label — same rank order, invertible, no information lost —
and it screens at 0.739. It passes at **every threshold in the grid**, and it
would pass at 0.5. No choice of cutoff catches it, because the failure is that
Pearson measures linear agreement and a leak does not have to be linear. Anyone
tuning the number is tuning the wrong dial.

**AT 0.999 THE SCREEN IS AN EXACT-COPY DETECTOR AND LITTLE MORE.** A continuous
label with 5% relative noise (`|r|` 0.9987) passes. A binary label with 1% of its
values flipped (`|r|` 0.981) passes. Both are leaks by any reading — a feature
that is the label with a rounding error — and neither is reported.

**AND LOOSENING IT BUYS FALSE POSITIVES ON THE SAME AXIS.** At 0.950 the screen
catches the 1%-flipped binary copy, and it also catches `y + noise(sd 0.30)`,
which is the shape of a genuinely strong legitimate predictor. The check already
says it reports candidates rather than deciding, so a false candidate is cheaper
here than in a detector — but it is not free, and the trade is monotone: there is
no cutoff that separates these two families, because they are not separated in
the statistic.

**`|r|` AND NOT `r` IS RIGHT, AND THE CASES CONFIRM IT.** `1 - y` is a perfect
inverse copy and correlates at −1. Screening on signed correlation would miss
every inverted copy.

---

## Why no configuration key is proposed

**Because the cases say a key would sell the wrong control.** Exposing
`label_screen_threshold` would let a user move a dial that does not separate the
two families above, and would imply the number is the thing to adjust. The
honest reading of the table is that the *statistic's blind spot* — non-linear
copies, and labels reconstructed from more than one column — dominates anything
the threshold does, and both blind spots are now stated in the check's own output
rather than left to be discovered.

**What would change this.** A second screen on a rank statistic (Spearman) would
catch every monotone copy in the table above, including `y**3`, at any sensible
cutoff. That is a new check with its own known positives and its own registered
position, not a parameter on this one, and it is named here so that "no key" does
not read as "nothing more to do."

> **THAT IS WHAT HAPPENED, at R231 §5** — though as an extension of this check
> rather than a separate one, because the two screens share their population,
> their label, their per-column loop and their output, and splitting them would
> have given a user two silences to reconcile instead of one result. The
> prediction that a rank statistic would catch every monotone copy **held
> exactly**: all four score 1.000.

**Where the number lives meanwhile.** In the signature, with a default, and in
the output on every run. It stays in R222's `should_refuse` candidate set with
its reason updated: the naming half is closed, and the key half is declined with
these cases as the reason rather than deferred without one.

---

## The cases under BOTH statistics — measured at R231, when the extension shipped

2,000 rows, seeded (`default_rng(19)`), `py -3.12`, CPython 3.12.10, numpy 2.4.2,
pandas 3.0.1. Both screens at 0.999.

| case, against a continuous label | Pearson | Spearman | caught? |
|---|---|---|---|
| exact copy | 1.00000 | 1.00000 | both |
| affine `3y+7` | 1.00000 | 1.00000 | both |
| **monotone `y**3`** | 0.73936 | **1.00000** | **Spearman only** |
| **monotone `sign(y)·√\|y\|`** | 0.96285 | **1.00000** | **Spearman only** |
| **`rank(y)`** | 0.97747 | **1.00000** | **Spearman only** |
| **logistic `1/(1+e^-5y)`** | 0.90091 | **1.00000** | **Spearman only** |
| `y` + noise sd 0.02 | 0.99979 | 0.99975 | neither (both just under) |
| `y` + noise sd 0.05 | 0.99868 | 0.99856 | neither |
| `y` + noise sd 0.30 | 0.95409 | 0.94909 | neither |
| **NON-monotone `y**2`** | **0.01117** | **0.02177** | **NEITHER — a perfect copy both are blind to** |
| unrelated | 0.00198 | 0.00147 | neither |

| case, against a binary label | Pearson | Spearman |
|---|---|---|
| exact copy | 1.00000 | 1.00000 |
| `1-y`, perfect inverse | 1.00000 | 1.00000 |
| 1% of labels flipped | 0.97500 | 0.97500 |
| 5% of labels flipped | 0.91712 | 0.91712 |

**Why 0.999 for the Spearman screen too, and why the choice is uninteresting.**
Every monotone copy above scores **exactly 1.000**, so no cutoff below 1 is doing
any work on the class the extension was added for. Matching the Pearson number
keeps the pair symmetric, and the two statistics diverge only on the noise rows,
where they agree to three decimal places anyway. **The threshold was never the
dial** — that was the finding that produced the extension, and it applies to the
new threshold as much as to the old one.

**On a binary label the two statistics coincide**, which is expected: a
two-valued column's ranks are a monotone function of its values. The extension
buys nothing there and costs a second correlation, which is the honest price.

**`y**2` is the bound and it is now in the check's own output.** It reproduces
the label exactly — every value determined, no information lost — and screens at
0.011 and 0.022. A silence from this check is a silence about **monotone**
pairwise resemblance, and about nothing wider.
