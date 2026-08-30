# Track B lessons

The review register in `HISTORY.md` closed at lesson 45 and is not reopened per
round. Track B's lessons accumulate here, plain and dated, for a considered
append later.

Each entry records what happened and what it costs to get wrong. Nothing here
creates, amends or narrows a rule; these are observations, not instructions.

---

## TB-01 — *(28 August 2026)* A merge can resurrect a defect that was deliberately removed

`phase1`'s copy of the checker carried the line-pinned citation form that R163 §3
ruled against and main had converted to an anchor. "Main wins" was the correct
resolution, and it was correct for a reason stronger than recency: importing the
older side would have undone a ruling.

The ruling had already been demonstrated by then, not merely argued. The anchored
citation moved three times as the register grew — 281, then 313, then 315 — and
resolved at each. The pinned form would have been stale by 36 lines at the first
of those and would have needed re-pinning at every append after.

**Every reconciliation with an older branch is a chance to reinstate something
that was removed on purpose, and the conflicts are only where that shows up
loudly.** The quiet cases are the files that merge cleanly because only one side
touched them. What made this one safe was checking, for each conflicted file,
whether the older side's unique content was superseded text or genuine work —
and the answer differed per file, so the question had to be asked per file.

Measured, for that merge: zero lines unique to `phase1` in the review register;
two in the checker, both the ruled-against form; four in the README, all pre-tag
hash values; thirty in the session record, a pre-tag snapshot; fifty-three in the
availability declaration, including a citation to a clause that does not exist.
Six files, six times the older side lost, and each time for a stated reason.
