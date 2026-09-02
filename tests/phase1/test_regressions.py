"""Regressions for two defects found by this suite, kept so they stay fixed.

Both were found the same way -- by running the instrument, not by reviewing it
(H-L21) -- and both had the same signature: a wrong FailureReason is worse than
an absent one, because it sends the next reader to look for a fault that was
never there.
"""
import numpy as np
import pandas as pd

from leakaudit import audit, probe_columns
from leakaudit.determinism import check_frame
from protocol.runtime_reference import (
    EvidenceOutcome,
    FailureReason,
    ScheduleStateKind,
    resolve_state_pair,
)


def _frame(n=32):
    rng = np.random.default_rng(11)
    return pd.DataFrame({"a": rng.normal(size=n), "b": rng.integers(0, 9, n)})


def _reads_a(d):
    return pd.DataFrame({"y": d["a"] * 3.0}, index=d.index)


def test_bare_frame_reaches_build_as_a_frame_not_as_a_dict():
    """DEFECT: `audit()` normalised a bare frame to {"raw": frame} and then
    handed the DICT to `build`. Every k6-shaped pipeline raised, the guard
    caught the raise, and the run was reported could_not_run -- a fault
    attributed to the caller's pipeline that belonged to this package.
    """
    seen = {}

    def spy(d):
        seen["type"] = type(d).__name__
        return _reads_a(d)

    result = audit(_frame(), spy)
    assert seen["type"] == "DataFrame", "build was handed a %s" % seen["type"]
    state, outcome = resolve_state_pair(result.traces[0])
    assert state.kind is ScheduleStateKind.COMPLETED
    assert outcome is EvidenceOutcome.FINDING


def test_a_build_that_cannot_run_is_CRASH_and_never_DETERMINISM():
    """DEFECT: a build raising on its own UNPERTURBED input was reported
    could_not_run(determinism). It had not been shown to be nondeterministic --
    it had been shown not to run. §6.6's precedence names that CRASH.
    """
    def cannot_run(_d):
        raise TypeError("this pipeline does not accept that input")

    r = probe_columns({"raw": _frame()}, cannot_run, bare=True, case_id="c")
    reasons = {x.failure_reason for x in r.preserving.records}
    assert reasons == {FailureReason.CRASH}, reasons
    assert FailureReason.DETERMINISM not in reasons

    state, outcome = resolve_state_pair(r.preserving)
    assert state.kind is ScheduleStateKind.INCOMPLETE
    assert state.reason is FailureReason.CRASH
    assert outcome is EvidenceOutcome.NONE


def test_the_guard_still_reports_DETERMINISM_when_it_is_determinism():
    """The companion negative: separating CRASH out must not have removed the
    guard's ability to report the thing it exists for."""
    state = {"n": 0}

    def flaky(d):
        state["n"] += 1
        return pd.DataFrame({"y": d["a"] * state["n"]}, index=d.index)

    r = probe_columns({"raw": _frame()}, flaky, bare=True, case_id="c")
    reasons = {x.failure_reason for x in r.preserving.records}
    assert reasons == {FailureReason.DETERMINISM}, reasons
    sstate, outcome = resolve_state_pair(r.preserving)
    assert sstate.reason is FailureReason.DETERMINISM
    assert outcome is EvidenceOutcome.NONE


def test_raised_flag_distinguishes_the_two_at_the_guard():
    g_raise = check_frame(lambda _d: (_ for _ in ()).throw(ValueError("x")),
                          _frame(), "original")
    assert g_raise.raised is True
    assert "own unperturbed input" in g_raise.detail

    counter = iter(range(100))

    def flaky(d):
        return pd.DataFrame({"y": d["a"] + next(counter)}, index=d.index)

    g_flaky = check_frame(flaky, _frame(), "original")
    assert g_flaky.deterministic is False
    assert g_flaky.raised is False
    assert g_flaky.differing_columns == ("y",)
