"""Coverage is reported, and incomplete-and-silent is its own answer. R267 §3.

`DESIGN.md` §5.2's "quick mode" is ruled here as a BUDGET rather than a mode,
and the ruling rests on a measurement: L3.1's cohorts cost ~0.02 s each because
one rebuild serves the whole batch, while **L2a rebuilds once per cohort**. So
there is nothing to save on L3.1 and everything to save on L2a, and a "mode"
that dialled both would be trading away coverage it was not buying anything for.

  (a) L3.1 ALWAYS RUNS EVERY ELIGIBLE COHORT. Not a default -- there is no
      parameter, because there is no saving to make.
  (b) THE BUDGET IS L2a's COHORT COUNT, declared by the user, defaulting to a
      number chosen from cost and PRINTED AS A DEFAULT, the way stride 97 is.

THE DEFAULT'S ARITHMETIC, MEASURED RATHER THAN PICKED. On the acceptance fixture
a build is **34.9 s** (R267, `zc` 2025-01, 338,159 rows), and L2a spends one
rebuild per cohort plus one for the baseline, so a run costs about
`(N + 1) x 34.9 s`. Ten minutes is 600 s, which gives `N <= 16`. **The shipped
default was 25**, or about 14.5 minutes -- over the target by half again, and
nobody had written the arithmetic down to notice. It is 16 here, and the number
travels with the sum that produced it so the next person can redo it against
their own build time instead of inheriting mine.

COVERAGE IS REPORTED, NEVER THRESHOLDED. Two numbers: cohorts probed of
eligible, and output rows in probed cohorts of all rows. **They are the
population of every silence the run reports**, which is the whole reason they
are printed. No level is required and none is offered: a level is a threshold,
and a threshold is a number people adjust toward until it passes.

INCOMPLETE-AND-SILENT IS A FOURTH ANSWER. A run that probed a subsample and
found nothing has not said "clean" -- it has said "nothing in the part I
looked at". Collapsing that into the clean exit is the same collapse as
reporting `none` as `observed_silence`, one level up. So there are four:

    complete and silent      everything eligible was probed, nothing moved
    finding                  something moved
    INCOMPLETE and silent    a subsample was probed, nothing moved in it
    refused                  the run could not be made

A CI user who accepts partial coverage DECLARES it, with one flag named for what
it accepts, and only then does the incomplete class map to the clean exit -- with
the acceptance printed beside the verdict. A declared acceptance, never a
default.

Written with the Write tool per D2.1.
"""

from __future__ import annotations

from dataclasses import dataclass

#: Seconds per build on the acceptance fixture, measured at R267. Carried so the
#: default below can be re-derived rather than trusted.
FIXTURE_BUILD_SECONDS = 34.9

#: The ten-minute target §5.2 is written against.
BUDGET_TARGET_SECONDS = 600

#: `(N + 1) * 34.9 <= 600` -> `N <= 16`. A COST CHOICE, printed as one.
DEFAULT_L2A_COHORTS = 16


def budget_arithmetic(n=DEFAULT_L2A_COHORTS, build_seconds=FIXTURE_BUILD_SECONDS):
    """The sum behind the default, so the number is never bare."""
    return ("L2a cohort budget: %d (default %d). L2a rebuilds ONCE PER COHORT, "
            "so the cost is about (N + 1) x %.1f s = %.0f s on the acceptance "
            "fixture, against a %d s target. The default is derived from that "
            "sum, not chosen: (%d + 1) x %.1f = %.0f s."
            % (n, DEFAULT_L2A_COHORTS, build_seconds,
               (n + 1) * build_seconds, BUDGET_TARGET_SECONDS,
               DEFAULT_L2A_COHORTS, build_seconds,
               (DEFAULT_L2A_COHORTS + 1) * build_seconds))


@dataclass
class Coverage:
    """The two numbers. Reported; never compared against a level."""

    cohorts_probed: int = 0
    cohorts_eligible: int = 0
    rows_in_probed: int = 0
    rows_total: int = 0
    #: L2a's own two numbers. It is the row with a BUDGET -- one rebuild per
    #: cohort -- so it is the row that can fall short, and a run's completeness
    #: is both rows or neither. L3.1 has no budget and is complete by
    #: construction; carrying its numbers anyway means a reader never has to
    #: know which row was the cheap one to read the coverage.
    l2a_probed: int = 0
    l2a_eligible: int = 0

    @property
    def complete(self) -> bool:
        """Every SEPARATION-ELIGIBLE cohort was probed.

        The denominator is not every second in the frame. `cohort_stride` is the
        attribution requirement rather than a budget -- seconds it excludes were
        never probeable at all -- so counting them here would report a shortfall
        no budget could close and would make the incomplete class fire on every
        run, which is the same as it firing on none.

        Note the direction: completeness is about COHORT coverage, not detector
        coverage. A complete run can still carry `unsupported` rows, and this
        says nothing about them.
        """
        l31_ok = (self.cohorts_eligible > 0
                  and self.cohorts_probed >= self.cohorts_eligible)
        # L2a is `unsupported` on most runs -- no label declaration -- and an
        # eligible count of zero means it did not run rather than that it ran
        # short. A row that never ran does not make the audit incomplete; it
        # makes it silent about that row, which its own verdict already says.
        l2a_ok = (self.l2a_eligible <= 0
                  or self.l2a_probed >= self.l2a_eligible)
        return l31_ok and l2a_ok

    def table(self) -> str:
        def pct(a, b):
            return "%.1f%%" % (100.0 * a / b) if b else "n/a"
        return (
            "COVERAGE (reported, not thresholded -- these two numbers are the "
            "POPULATION of every silence above):\n"
            "  L3.1 cohorts probed   %d of %d eligible (%s)\n"
            "  rows in those cohorts %d of %d (%s)\n"
            "  L2a  cohorts probed   %s"
            % (self.cohorts_probed, self.cohorts_eligible,
               pct(self.cohorts_probed, self.cohorts_eligible),
               self.rows_in_probed, self.rows_total,
               pct(self.rows_in_probed, self.rows_total),
               ("%d of %d eligible (%s) -- this is the budgeted row"
                % (self.l2a_probed, self.l2a_eligible,
                   pct(self.l2a_probed, self.l2a_eligible))
                if self.l2a_eligible > 0 else
                "not run (see its own verdict above)")))


class AuditIncomplete(AssertionError):
    """A silence was asserted over a subsample without accepting partial cover."""


def assert_audit_complete(coverage, *, accept_partial_coverage=False) -> None:
    """`DESIGN.md` §8's assertion, at the library entry point. R267 §3(e).

    THE SAME RULE AS THE EXIT CODE, AT THE OTHER DOOR. A CI user reaches this
    through the CLI and an embedding user reaches it here; a rule enforced at one
    of two entry points is a rule with a bypass, which is the shape R255 §5
    settled for the slice refusal.

    The name is `DESIGN.md`'s and still fits: what it asserts is that the audit
    was complete, and it raises when it was not unless the caller has said, in
    the call, that partial coverage is acceptable to them.
    """
    if coverage is None or coverage.complete or accept_partial_coverage:
        return
    # NAME THE ROW THAT FELL SHORT. A first version quoted L3.1's numbers on
    # every failure, so a run short only on L2a was told "72 of 72" and had to
    # guess -- the count was true and answered a different question.
    short = []
    if not (coverage.cohorts_eligible > 0
            and coverage.cohorts_probed >= coverage.cohorts_eligible):
        short.append("L3.1 probed %d of %d eligible cohorts"
                     % (coverage.cohorts_probed, coverage.cohorts_eligible))
    if coverage.l2a_eligible > 0 and coverage.l2a_probed < coverage.l2a_eligible:
        short.append("L2a probed %d of %d eligible cohorts (this is the "
                     "budgeted row)"
                     % (coverage.l2a_probed, coverage.l2a_eligible))
    raise AuditIncomplete(
        "the audit is INCOMPLETE: %s. A silence from it is a silence ABOUT "
        "THAT SUBSAMPLE and not about the pipeline. Pass "
        "`accept_partial_coverage=True` to assert over the subsample "
        "deliberately -- the acceptance is then yours and is recorded -- or "
        "raise the cohort budget until the run is complete."
        % "; ".join(short))
