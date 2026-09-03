# Prediction, written BEFORE the repaired round-reconciliation check is run

Nothing here is a `PREREG.md` §6.2 result.

**Why this file exists and why it is timestamped by its commit.** R207 §5's
precedent: the manifest defect was found *because* a prediction was wrong, and a
correct prediction would have told nobody anything. So the number goes down
first, in a committed file, and the measurement follows in the next commit.

## What is being repaired

`check_round_reconciliation` implements D10 — every working-directory file is in
the repository or declared ephemeral. Its `_WORK_ROOT` is a **hardcoded absolute
path** to a session that ended on 26 August 2026: 679 files, nothing written
since. The live session's directory holds 11,985 files and is not scanned. 149
such directories exist. Coverage of the current round's working files is **zero**
(D-V30A-48).

## R163 §1's exemption test, stated explicitly

> *Would this instrument change have been made if the content that triggered it
> did not exist?*

**Yes.** A hardcoded path to a dead directory is repaired regardless of what
pointing it correctly would find. The rule this test protects — *fix the world,
not the instrument* — prohibits changing an instrument so a finding goes away.
This change points an instrument at a population it was always meant to have and
will, if anything, **produce** findings. Opposite direction. Defect repair, ruled,
disclosed.

## The prediction

**I predict the repaired check reports MANY unreconciled files — on the order of
hundreds to low thousands — and that this is CORRECT behaviour rather than a new
defect.**

Reasoning, so the prediction is falsifiable in its parts rather than only in
total:

1. The live scratchpad holds **11,985** files against the dead one's 679.
2. Most are genuinely ephemeral by the check's own list — `__pycache__`, task
   output, `.txt` scratch — and will be classified as such.
3. But this session wrote many **applier scripts and fragments** that are neither
   in the repository nor obviously matching an ephemeral token: `append_lesson.py`,
   `r216_ic_audit.py`, the `dod_work/` tree with its CSVs and parquets, three
   venvs' worth of nothing (venvs are outside the scratchpad).
4. `dod_work/` alone holds the definition-of-done walk's pipeline, data files and
   outputs — perhaps 20–30 files, none in the repository by design.

**Specific sub-predictions, each checkable on its own:**

- The count will be **greater than 100**.
- `dod_work/stations.csv` and `dod_work/scans.csv` will be among the
  unreconciled, because they are working data that was never committed.
- The ephemeral classification will absorb the **majority** of the 11,985 —
  I expect ephemeral to exceed unreconciled by at least 5:1.
- **Zero** files from the dead directory will appear, because it will no longer
  be scanned.

## What the repair must NOT do, stated before it is written

**The plausible wrong instrument is one that resolves the work root at IMPORT
time.** The checker is imported by the registration test suite, in processes with
no relationship to any session, so an import-time resolution would bind whatever
the environment looked like when the module loaded — reproducing the original
defect in a new form. **Resolution happens at run time, inside the check.**

**And the dead-directory behaviour is decided before it is measured:** a work
root that does not exist is reported as a NOTE saying nothing was reconciled, not
as a pass. The check already does this and the behaviour is kept.

## The known positive, discriminating in both directions

1. **A file that exists only in the live directory must be found.** Write one,
   run the check, confirm it is named. Without this the repair could resolve to
   the right directory and still scan nothing.
2. **A file matching an ephemeral token must not be found.** Otherwise the check
   reports everything and its findings mean nothing.
3. **The wrong instrument must be ruled out explicitly:** an import-time
   resolution passes (1) and (2) in a single process and fails across processes.
   The discriminating case is resolving in one process and checking in another.

*Written 3 September 2026, before the repaired check was run.*
