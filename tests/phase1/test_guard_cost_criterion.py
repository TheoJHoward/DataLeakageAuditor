"""The guard's cost limit, asserted in both directions. R230 §1.

THE SHAPE, reused from the frozen instrument's `N = 4`. A limit is only a limit if
something checks BOTH that the measurement is under it AND that the limit was not
set to the measurement. The second assertion is the one that catches a threshold
chosen after the number arrived — **a limit equal to its measurement is what
choosing it late looks like from outside**.

THE ORDERING IS DISCLOSED RATHER THAN CONCEALED. R230 §1 asked for this criterion
before the `setprofile` number was read. It could not be: the measurement
completed and the decision was committed in R229 before R230 arrived.
`evidence/session/GUARD_COST_CRITERION.md` says so in its first section, and this
file exists to make the criterion checkable from here on rather than to claim it
was checkable then.

WHY THE LIMIT IS 20 MINUTES, and why it is not about milliseconds. A guard that
gets skipped protects nothing, so the cost that matters is the cost at which
somebody stops running it. This project has both ends of that on record: routine
runs of ~7-9.5 minutes have been completed repeatedly across five rounds, and one
run at 34+ minutes was KILLED rather than waited out. Twenty is roughly twice the
longest completed run and comfortably below the abandoned one.

AND THE FALLBACK PASSES THIS, which is the point of keeping it. 13.4 minutes
against a 20-minute limit: the rejection was NOT about cost. It was about the
fallback recording 2 modules where `sys.monitoring` records 4 — a false negative
in the one direction a staleness guard exists to prevent. Without this file a
reader would assume cost and be wrong.
"""
from __future__ import annotations

# --- the criterion, and the measurement it is applied to --------------------

FULL_GUARD_LIMIT_S = 20 * 60          # 1200 s. See the docstring for the anchor.

# `py -3.12 <scratch>/r229_setprofile_real.py`, CPython 3.12.10, numpy 2.4.2,
# pandas 3.0.1. One guard side over the acceptance fixture, stride=997,
# max_cohorts=300, imports warmed. MV-16 carries the full table.
MEASURED_SIDE_S = {"none": 209.2, "monitoring": 185.8, "setprofile": 379.5}
MEASURED_MODULES = {"none": 0, "monitoring": 4, "setprofile": 2}
CAPTURE_S = 43.0


def full_guard_seconds(recorder: str) -> float:
    """Both sides plus one fixture capture — what a person actually waits for."""
    return 2 * MEASURED_SIDE_S[recorder] + CAPTURE_S


def test_the_shipped_recorder_is_under_the_limit():
    assert full_guard_seconds("monitoring") < FULL_GUARD_LIMIT_S


def test_the_FALLBACK_is_under_the_limit_too_so_cost_was_not_the_reason():
    """The assertion that makes the rejection checkable rather than assumed."""
    cost = full_guard_seconds("setprofile")
    assert cost < FULL_GUARD_LIMIT_S, (
        "the fallback fails the cost criterion at %.0f s, which would make the "
        "reported reason for rejecting it wrong" % cost)


def test_the_LIMIT_EXCEEDS_the_measurement_it_bounds():
    """The other direction. A limit equal to, or barely above, the number it is
    applied to is a limit chosen after reading that number."""
    worst = max(full_guard_seconds(r) for r in MEASURED_SIDE_S)
    assert FULL_GUARD_LIMIT_S > worst, (
        "the limit does not exceed the largest measurement: %s vs %.0f s"
        % (FULL_GUARD_LIMIT_S, worst))
    assert FULL_GUARD_LIMIT_S >= 1.4 * worst, (
        "the limit is %.2fx the largest measurement, which is close enough to "
        "look chosen to fit it. State a limit with headroom or state why this "
        "one is right." % (FULL_GUARD_LIMIT_S / worst))


def test_the_limit_is_below_the_run_that_was_actually_ABANDONED():
    """The upper anchor is behavioural: 34+ minutes was killed rather than
    waited out. A limit above that would permit a cost somebody has already
    demonstrated they will not pay."""
    abandoned_s = 34 * 60
    assert FULL_GUARD_LIMIT_S < abandoned_s


def test_the_REAL_reason_for_the_rejection_is_recorded_as_coverage():
    """If this ever passes on cost alone the record has lost its reason."""
    assert MEASURED_MODULES["setprofile"] < MEASURED_MODULES["monitoring"], (
        "the fallback no longer under-records, so the rejection's stated reason "
        "no longer holds and the decision needs revisiting")


def test_the_criterion_document_discloses_that_it_was_written_AFTER():
    from pathlib import Path
    doc = (Path(__file__).resolve().parents[2]
           / "evidence" / "session" / "GUARD_COST_CRITERION.md")
    assert doc.is_file(), doc
    head = doc.read_text(encoding="utf-8")[:2000]
    assert "AFTER the measurement" in head, (
        "the criterion document no longer says the criterion was written after "
        "the number was read, which is the one thing a reader must not assume "
        "the other way")
