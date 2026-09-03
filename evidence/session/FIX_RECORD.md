# Fix record — one boolean per fix, and a threshold committed before any data

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures.

## What this is, and the one thing it is not

Per fix shipped in Phase 2, one field: **did this fix's acceptance test find a
defect in the fix, before commit?** True or false.

**Nothing is computed from it.** Not now, and not when it has ten rows. The
reason is in `TRACKB_LESSONS.md` TB-17 and is worth restating at the top of the
file that could most easily violate it: an events register cannot supply a rate,
because the "nothing happened" cases do not present themselves for recording. A
discipline that requires writing "nothing happened" after every fix will be
complied with unevenly, and **uneven compliance on non-events produces a wrong
rate — which computes, publishes, and persuades.** An absent denominator reports
no result; a sloppy one reports a number.

This file exists so the false rows are written down too. That is the whole of
what it adds, and it is exactly the thing that was missing.

## The threshold, pre-committed on 2026-09-03, before the first row was entered

**No rate may be computed from this file until it carries at least 30 rows.**

Committed now, with n = 2 observed and the file otherwise empty, because a
threshold chosen once numbers are visible is the thing this project was built not
to do. The number is derived from what a proportion needs rather than from
anything here: below about 30 observations a proportion's confidence interval is
wider than the difference anyone would act on, so a smaller sample produces a
figure that reads as a finding and supports no decision.

**And a further pre-commitment, so the first one cannot be satisfied cheaply:**
at 30 rows the output is a proportion **with an interval**, and if the interval
spans the range that would change what anyone does, the reported result is *"no
usable rate at n=30"* rather than the point estimate. There is no second
threshold to fall back to; the alternative to a usable interval is saying so.

**This threshold may be revised only by a delta that states the new number and
the reason, before the rows that would satisfy it exist.** Revising it with the
data visible is the defect it was written to prevent.

## What IS usable at n = 2, and is not a rate

`TRACKB_LESSONS.md` TB-18: both defects were in a case the fix was **holding
constant**, not in a case it was changing. That is a location, actionable
immediately, and it is the practice adopted below rather than any frequency.

## The practice this file records the compliance of

**Every fix's acceptance test names what the fix holds constant, and tests that
directly.** Both known instances were found because something incidentally
exercised the held-constant case. Making it deliberate costs one assertion.

## The rows

| date | fix | acceptance test | found a defect in the fix? | held-constant case tested? |
|---|---|---|---|---|
| 2026-09-02 | the build-return-type guard (walk item 6) | re-run of the walk's wrong turns | **yes** — double-wrapped, adding two frames to a user traceback (D-V30A-45) | incidentally — the user's-own-exception case was a wrong turn, so the re-run covered it |
| 2026-09-03 | the guard's idempotency marker | the two-guard collision case | **yes** — the marker was generic, so a later guard would silently decline to apply (D-V30A-46) | yes — the held-constant case *was* the test |
| 2026-09-03 | the six walk fixes (items 1–5) | re-run of each wrong turn | no | items 3 and 6 held "a user's own exception keeps its traceback" constant, and it is asserted |
| 2026-09-03 | the opt-in currency check | its own stale/vanished/unattested positives | no | held constant: that an existing-result check keeps passing — asserted by leaving `test_every_opt_in_test_has_a_recorded_result` untouched and green |
| 2026-09-03 | the probe path guard | six refusal cases plus the drift positive | no | held constant: that `watch()` does not report third-party frames — asserted |

**Five rows. The threshold is thirty. Nothing is computed.**
