"""The idempotency fix, with the two positives R211 §1 requires.

THE FIX BEING TESTED WAS ITSELF A FIX FOR A DEFECT ITS OWN TEST FOUND. Item 6 of
the definition-of-done walk wrapped the user's build callable at the CLI, and
`contract.audit` wrapped again. Both are right alone. Together they put
`contract.py, in checked` into the stack TWICE -- two frames of this tool's
plumbing inserted into the one traceback whose whole value is that it points at
the user's file. Nothing but re-running the wrong turn showed it: the suite was
green and every fixed case returned one clean line.

TWO THINGS HAVE TO BE SHOWN, NOT ASSUMED.

  1. The doubling is actually prevented. The positive is the doubled frame that
     was observed -- so the test counts frames in a real traceback rather than
     asserting object identity, which would pass even if the frames were still
     there for some other reason.

  2. The marker does not suppress a DIFFERENT guard. A guard that declines to
     apply because something else already did is the discarded-parameter defect
     wearing a decorator: its check goes unperformed and nothing is said. The
     first version of the marker read `__leakaudit_guarded__` -- generic, and
     exactly that shape. It is now keyed on the JOB, and the two-guard case is
     constructed here rather than argued.
"""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.contract import (                                  # noqa: E402
    GUARD_BUILD_RETURN, ContractError, guarded_build, guards_applied)


def _raising_build(frames):
    raise ValueError("my own pipeline is broken")


def _frames_in_traceback(fn) -> list[str]:
    """The function names on the stack when `fn` raises, in order."""
    try:
        fn({})
    except ValueError:
        return [f.name for f in traceback.extract_tb(sys.exc_info()[2])]
    raise AssertionError("the build did not raise, so there is no stack to read")


# ---------------------------------------------------------------------------
# POSITIVE 1 -- the doubling is prevented, counted in a real traceback.
# ---------------------------------------------------------------------------

def test_positive_1_wrapping_twice_leaves_ONE_checked_frame():
    once = guarded_build(_raising_build)
    twice = guarded_build(once)

    names = _frames_in_traceback(twice)
    n = names.count("checked")
    assert n == 1, (
        "%d `checked` frames in the user's traceback, not 1. This is the exact "
        "defect the idempotency fix exists to prevent, and its whole cost falls "
        "on the one case the guard was careful to preserve -- a traceback whose "
        "value is that it points at the user's file. Stack: %s" % (n, names))
    assert names[-1] == "_raising_build", (
        "the user's own function is not the last frame: %s" % names)


def test_positive_1_the_UNGUARDED_shape_is_what_a_single_wrap_looks_like():
    """The control. Without it, `== 1` could be passing for the wrong reason."""
    names = _frames_in_traceback(guarded_build(_raising_build))
    assert names.count("checked") == 1
    bare = _frames_in_traceback(_raising_build)
    assert bare.count("checked") == 0, (
        "an unwrapped callable already shows a `checked` frame, so counting "
        "them measures nothing: %s" % bare)


def test_positive_1_a_TRIPLE_wrap_is_also_one():
    f = guarded_build(guarded_build(guarded_build(_raising_build)))
    assert _frames_in_traceback(f).count("checked") == 1


def test_positive_1_the_guard_still_does_its_job_after_a_second_wrap():
    """Idempotent must not mean inert."""
    def returns_a_dict(frames):
        return {"a": [1]}

    twice = guarded_build(guarded_build(returns_a_dict))
    with pytest.raises(ContractError, match="returned dict"):
        twice({})


# ---------------------------------------------------------------------------
# POSITIVE 2 -- the marker does not suppress a different guard.
# ---------------------------------------------------------------------------

GUARD_OTHER = "other_job_entirely"


def _other_guard(fn):
    """A second guard, written the way a later one would be: its own job name."""
    if GUARD_OTHER in guards_applied(fn):
        return fn

    def wrapper(*a, **kw):
        out = fn(*a, **kw)
        wrapper.calls += 1
        return out

    wrapper.calls = 0
    wrapper.__leakaudit_guards__ = guards_applied(fn) | {GUARD_OTHER}
    return wrapper


def _ok_build(frames):
    return pd.DataFrame({"a": [1]})


def test_positive_2_a_DIFFERENT_guard_is_not_skipped_by_this_ones_marker():
    both = _other_guard(guarded_build(_ok_build))
    assert both is not guarded_build(_ok_build), (
        "the second guard declined to apply because the first had -- its check "
        "goes unperformed and nothing is said about it")
    both({})
    assert both.calls == 1, "the second guard wrapped but never ran"
    assert guards_applied(both) == {GUARD_BUILD_RETURN, GUARD_OTHER}


def test_positive_2_order_does_not_matter():
    both = guarded_build(_other_guard(_ok_build))
    assert guards_applied(both) == {GUARD_BUILD_RETURN, GUARD_OTHER}
    both({})


def test_positive_2_each_guard_is_still_idempotent_in_the_presence_of_the_other():
    f = _other_guard(guarded_build(_ok_build))
    assert guarded_build(f) is f, "the build guard re-applied over a foreign one"
    assert _other_guard(f) is f, "the foreign guard re-applied over ours"


def test_positive_2_BOTH_guards_actually_fire():
    """Applied is not the same as effective, and the walk taught that twice."""
    def returns_none(frames):
        return None

    both = _other_guard(guarded_build(returns_none))
    with pytest.raises(ContractError, match="returned None"):
        both({})
    # The outer guard's counter never increments, because the inner one raised
    # first -- which is the correct order and is asserted rather than assumed.
    assert both.calls == 0


def test_positive_2_the_marker_is_keyed_on_the_JOB_not_on_being_guarded():
    """The regression this file exists to prevent, stated as a property."""
    assert GUARD_BUILD_RETURN != "guarded" and GUARD_BUILD_RETURN, GUARD_BUILD_RETURN
    f = guarded_build(_ok_build)
    assert not getattr(f, "__leakaudit_guarded__", False), (
        "a generic boolean marker is back; a later guard checking it would "
        "silently decline to apply")
    assert GUARD_BUILD_RETURN in guards_applied(f)
