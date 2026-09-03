# SECOND prediction — written 3 September 2026, before the repaired check is run

Nothing here is a `PREREG.md` §6.2 result.

## Why there are two and why the first one stays

`ROUND_RECONCILIATION_PREDICTION.md` was committed at R216 and the repository has
moved several commits since, so **the subject grew between the commitment and the
measurement**. Re-predicting *in place of* the first would be indistinguishable
from adjusting toward the answer once it is known.

So: a second prediction, labelled and dated, both kept, **then one run**. If the
two agree the drift did not matter. If they differ, the difference is itself a
free measurement of how far the population moved. If the measurement matches
neither, that is the most informative outcome available — R207 §5's manifest
defect was found by a wrong prediction, and a correct one would have told nobody
anything.

## What changed in the subject since prediction 1

| | at R216 | now |
|---|---|---|
| files in the live scratchpad | 11,985 | **12,002** |

Seventeen files, which is nothing. **But prediction 1 got the composition badly
wrong, and that is the substantive drift** — not the count.

I predicted "hundreds to low thousands" and reasoned about applier scripts and
`dod_work/`. I did not account for **`dod_env`, a full virtualenv living inside
the scratchpad**: 7,690 of the 12,002 files, including 2,873 `.py` files under
`site-packages` from numpy, pandas, pyarrow and pytest. Those are not in the
repository and no ephemeral token reaches them. `dod_work/` — the thing
prediction 1 named specifically — is **28 files**.

## The second prediction

**I predict the repaired check reports THOUSANDS of unreconciled files —
between 5,000 and 9,000 — and that the overwhelming majority are third-party
library sources inside `dod_env`, not working files in any sense the D10 rule
cares about.**

Falsifiable in parts:

1. The count is **greater than 3,000**. (Prediction 1 said ">100", which is true
   but so weak it would have been satisfied by a wrong answer.)
2. **`dod_env` contributes the majority** — more than half of all unreconciled.
3. The ephemeral classification absorbs roughly **3,200** (2,750 `.pyc` in the
   venv plus 441 `__pycache__` files elsewhere), so the ephemeral-to-unreconciled
   ratio is well **under 1:1** — reversing prediction 1's claim that ephemeral
   would exceed unreconciled by 5:1.
4. `dod_work/stations.csv` and `dod_work/scans.csv` are among the unreconciled.
   *(Carried unchanged from prediction 1.)*
5. **Zero** files from the dead `8b1d67a4` directory. *(Carried unchanged.)*

## What I expect the result to MEAN, stated before seeing it

**A count in the thousands is not a defect in the tree and it is not a defect in
the repair.** It is a finding about the **ephemeral list**: that list was written
against an older working directory whose contents were repo copies, ceremony
drafts and backups, and it has no token for a virtualenv. Pointing the check at a
live directory that contains one produces a flood of true-by-its-own-rule
findings that no reader would act on.

**Which is the second-order problem R215 §5 already named:** a check earns
attention in proportion to the fraction of its findings that require thought. A
repair that turns one janitorial finding into six thousand spends that credit
entirely.

**So the likely correct follow-up is an ephemeral token for virtualenv
directories** — declared with its reason, exactly as the fifteen existing tokens
are. That is a change to the check's declared population and it is **not** made
in the same act as the repair, and **not** before the number is measured. Naming
it here is a prediction about what the number will imply, recorded so that acting
on it afterwards cannot be mistaken for having discovered it afterwards.

## What the repair must not do — carried unchanged from prediction 1

**The plausible wrong instrument resolves the work root at IMPORT time.** The
checker is imported by the registration suite in processes unrelated to any
session, so an import-time resolution binds whatever the environment looked like
when the module loaded — the original defect in a new form. **Resolution happens
at run time, inside the check.**

**Known positive, both directions:** a file that exists only in the live
directory is found; a file matching an ephemeral token is not. The import-time
repair passes both within one process and fails across processes, so the
discriminating case is resolving in one process and checking in another.

*Written before the repaired check was run. Prediction 1 stands unedited beside
this file.*
