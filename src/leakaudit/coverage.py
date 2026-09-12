"""Coverage is reported, and incomplete-and-silent is its own answer. R267 §3.

`DESIGN.md` §5.2's "quick mode" is ruled here as a BUDGET rather than a mode.

  (a) L3.1 IS CHEAP PER COHORT BECAUSE IT BATCHES -- AND BATCHING IS WHAT LIMITS
      IT. One rebuild serves every cohort in a pass, but the cohorts in one pass
      must sit further apart than the builder's measured reach, so a pass at
      stride 97 probes one second in ninety-seven. **R267 wrote "L3.1 always
      runs every eligible cohort -- there is nothing to save", and it was wrong,
      retracted at R268 §0:** cheap per cohort is not the same as able to probe
      every cohort. A COMPLETE L3.1 run is `stride` passes at different offsets,
      each its own rebuild (R268 §3(d)), so L3.1's budget is PASSES.
  (b) L2a rebuilds once per cohort, so its budget is its COHORT COUNT, declared
      by the user, defaulting to a number chosen from cost and PRINTED AS A
      DEFAULT, the way stride 97 is. Complete for L2a is every eligible cohort.

THE DEFAULT'S ARITHMETIC, MEASURED RATHER THAN PICKED. On the acceptance fixture
a build is **34.9 s** (R267, `zc` 2025-01, 338,159 rows), and L2a spends one
rebuild per cohort plus one for the baseline, so a run costs about
`(N + 1) x 34.9 s`. Ten minutes is 600 s, which gives `N <= 16`. **The shipped
default was 25**, or about 14.5 minutes -- over the target by half again, and
nobody had written the arithmetic down to notice. It is 16 here, and the number
travels with the sum that produced it so the next person can redo it against
their own build time instead of inheriting mine.

COVERAGE IS REPORTED, NEVER THRESHOLDED, IN THREE STATES (R268 §3(b)). Every
decision second is probed, eligible-but-unprobed, or ineligible under the declared
model, and rows take the state of the second they fall in. The denominator is
every cohort the model makes probe-able, independent of stride and budget -- so a
default run is INCOMPLETE and exits as such. **These counts are the population of
every silence the run reports**, which is the whole reason they are printed. No
level is required and none is offered: a level is a threshold, and a threshold is
a number people adjust toward until it passes.

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
    """Three states, for cohorts and for rows. Reported; never thresholded.

    R268 §3(b). Every decision second is in exactly ONE state:

      probed               selected, and a declared frame carries a row in it
      eligible, unprobed   a declared frame carries a row; not selected
      ineligible           no declared frame carries a row -- nothing to corrupt
                           under THIS model, whatever the stride or the budget

    Rows take the state of the second they fall in. Rows in a slice's padding
    are CONTEXT -- present in the data, never a subject -- and are counted apart,
    so the three states still cover the subjects exactly. `verify` refuses a
    table whose states do not add up to the population it claims to describe.
    """

    cohorts_probed: int = 0
    cohorts_unprobed: int = 0
    cohorts_ineligible: int = 0
    rows_probed: int = 0
    rows_unprobed: int = 0
    rows_ineligible: int = 0
    context_rows: int = 0
    #: L2a's two numbers. Its eligible set is every decision second it could
    #: probe, independent of stride and budget -- the same rule as L3.1's.
    l2a_probed: int = 0
    l2a_eligible: int = 0

    @property
    def cohorts_eligible(self) -> int:
        return self.cohorts_probed + self.cohorts_unprobed

    @property
    def rows_total(self) -> int:
        return (self.rows_probed + self.rows_unprobed + self.rows_ineligible
                + self.context_rows)

    @property
    def complete(self) -> bool:
        """Every cohort the DECLARED MODEL makes probe-able was probed.

        THE DENOMINATOR IS INDEPENDENT OF STRIDE AND BUDGET, and it has been
        otherwise. R267 set it to the separation-eligible set, `secs[::stride]`,
        arguing that counting stride-excluded seconds made every run incomplete
        and "a class that fires always distinguishes nothing". R268 §3 ruled
        the other way, correctly: a default run at stride 97 probes one second
        in ninety-seven, so its silence IS incomplete, and the exit code that
        says so distinguishes the default run from a complete one -- which is
        the whole distinction. A note beside a clean exit is one shade from a
        pass (R220 §4); an exit code is not.

        Completeness is about COHORT coverage, not detector coverage: a complete
        run can still carry `unsupported` rows, and this says nothing about them.
        """
        l31_ok = self.cohorts_eligible > 0 and self.cohorts_unprobed == 0
        # An L2a eligible count of zero means the row did not run, not that it
        # ran short; its own verdict already says so.
        l2a_ok = (self.l2a_eligible <= 0
                  or self.l2a_probed >= self.l2a_eligible)
        return l31_ok and l2a_ok

    def verify(self, n_seconds: int, n_rows: int) -> None:
        """The states COVER their population, or the table describes nothing.

        Raised rather than asserted: `python -O` strips asserts, and this is a
        claim the run prints, not a debugging aid.
        """
        placed = (self.cohorts_probed + self.cohorts_unprobed
                  + self.cohorts_ineligible)
        if placed != n_seconds or self.rows_total != n_rows:
            raise ValueError(
                "coverage does not cover its population: %d cohort(s) placed "
                "of %d decision seconds, %d row(s) placed of %d"
                % (placed, n_seconds, self.rows_total, n_rows))

    def table(self) -> str:
        def cell(n, of):
            return "%d (%s)" % (n, ("%.1f%%" % (100.0 * n / of)) if of else "n/a")
        c_all = self.cohorts_eligible + self.cohorts_ineligible
        r_all = self.rows_probed + self.rows_unprobed + self.rows_ineligible
        fmt = "  %-13s %18s %22s %28s"
        lines = [
            "COVERAGE (reported, not thresholded -- the POPULATION of every "
            "silence above). Three states; together they cover every subject:",
            fmt % ("", "probed", "eligible, unprobed",
                   "ineligible under the model"),
            fmt % ("L3.1 cohorts", cell(self.cohorts_probed, c_all),
                   cell(self.cohorts_unprobed, c_all),
                   cell(self.cohorts_ineligible, c_all)),
            fmt % ("L3.1 rows", cell(self.rows_probed, r_all),
                   cell(self.rows_unprobed, r_all),
                   cell(self.rows_ineligible, r_all)),
        ]
        if self.context_rows:
            lines.append(
                "  %d row(s) sit in a slice's padding: context the builder "
                "reads, never a subject, outcome `not_applicable` -- counted "
                "apart from the three states." % self.context_rows)
        if self.l2a_eligible > 0:
            lines.append("  L2a cohorts   %d probed of %d eligible -- the "
                         "budgeted row" % (self.l2a_probed, self.l2a_eligible))
        else:
            lines.append("  L2a cohorts   not run (see its own verdict above)")
        lines.append(
            "  COMPLETE: yes" if self.complete else
            "  COMPLETE: NO -- a silence here is about the probed cohorts only "
            "(L3.1: %d eligible unprobed; L2a: %d of %d probed)"
            % (self.cohorts_unprobed, self.l2a_probed, self.l2a_eligible))
        return "\n".join(lines)


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
        "make the run COMPLETE: every eligible cohort probed, which for L3.1 "
        "is `stride` passes at different offsets (`--complete`) and for L2a is "
        "every eligible cohort at a build each. A larger budget alone does not "
        "complete L3.1, since one pass covers one second in `stride`."
        % "; ".join(short))
