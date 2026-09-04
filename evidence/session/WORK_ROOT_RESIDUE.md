# The unreconciled working files — what they are

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures.

**The ask, and the shape of the answer.** R224 §4 item 4: the residue reported by
`round_reconciliation` is to be **declared for what it is, not for how many files
a token would remove**. A token justified by its yield is a scan exclusion
wearing a reason; a token justified by what it names is a claim about the files,
which is falsifiable. So this file is a census first and a decision second.

**The number moves and that is expected.** It was **633** when R222 measured it,
**651** when this census was taken, and **548** after the four tokens below were
added. The census table is the pre-token population, because the question was
what the files ARE and taking some of them out of view first would have answered
a different one. The 103 the tokens account for are a consequence of naming four
kinds, not the reason for naming them.

All of these count files in one session's scratch directory, and
that directory grows every round. It is not a stable quantity and it is listed as
such in `METHOD_VERIFICATIONS.md` MV-12.

---

## The census

651 files under the current work root, after the `.pyc`, repository-content and
manifest matches and the ephemeral tokens **as they stood before this round** are
taken out.

| what they are | count |
|---|---|
| captured command output (`.txt`, `.log`) — a run's stdout kept so a number can be re-read | 188 |
| round-numbered working files (`rNNN_*`) — the per-round scratch of 113 distinct rounds | 170 |
| one-off scripts (`.py`) — written to answer one question and not reused | 102 |
| draft fragments (`.md`) — text composed here and then applied to a repository file | 28 |
| commit-message files (`*_msg.txt`) — the `-F` source for `git commit` | 25 |
| virtualenv launchers outside `site-packages` (`dod_env/`, `floor_env/`) | 26 |
| intermediate data (`.json`) | 15 |
| test trees and demo data in sub-directories (`dod_work/`, `maintree/`, `b7/`, `instest/`, `availdemo/`, `clidemo/`, `b2_inputs/`, `b3_inputs/`, `b8_shards/`, `k1_broken/`, `k1_fixed/`, `b9/`, `t/`, `tagchecker/`) | 97 |

By suffix: 267 `.txt`, 170 `.py`, 108 `.md`, 44 `.json`, 16 `.log`, 16 `.exe`,
9 `.csv`, 6 no suffix, 4 `.parquet`, 4 `.bat`, 2 `.sh`, 2 `.cfg`.

---

## The one thing this check cannot tell apart, said plainly

**A draft that was applied and a deliverable that was forgotten look identical to
it.** The check matches on content hash. A fragment composed here and spliced
into a repository file has different bytes from the file it became, so it does
not match — and neither does a file that should have been brought in and was not.
**28 draft fragments are in exactly that state**, and the check reports them for
the same reason it would report a real omission.

That is not a defect in the check; it is the check working. Its job is to leave
nothing unaccounted for, and a class it cannot discriminate is a class it must
keep reporting.

---

## What was tokened, and what deliberately was not

**Tokened — four kinds, each with a definite marker and a reason about the files
themselves:**

- `_msg.txt` — commit messages. Their content lives in the commit history, not in
  the tree, so they can never match repository content. `tools/safe_edit.py`
  requires the message to be a file on disk, so these exist by rule.
- `/dod_env/`, `/floor_env/` — the `.exe` shims, `pyvenv.cfg` and activation
  scripts a `python -m venv` writes outside `site-packages`. The `site-packages`
  contents were already tokened at R220; these are the same virtualenvs' other
  half.
- `/k1_broken/`, `/k1_fixed/` — a deliberately mutated tree and its repaired twin,
  kept so a defect can be reproduced. Not matching repository content is the
  point of them.

**Not tokened, on purpose:** the 188 captured outputs, the 170 round-numbered
files, the 102 one-off scripts and the 28 drafts. They are the largest classes
and they have **no definite marker** — only a naming habit. R220 §3 chose
`/site-packages/` precisely because it is a marker rather than a resemblance, and
a pattern over `r\d+_` would be matching on "looks like a round file", which is
the thing that rule exists to prevent. The residue after the four tokens stays a
**finding**, not a note.

**So the number does not go to zero, and it should not.** A check that reported
green here would be telling me that nothing in a decade of scratch work was ever
left behind, which is a claim nobody has established. What has changed is that
the residue is now a described population rather than a bare count.
