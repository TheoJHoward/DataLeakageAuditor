"""B3 -- the determinism guard, and its KNOWN-POSITIVE test.

A guard that has only ever been run against deterministic pipelines has not been
shown to detect anything. `PREREG.md` H-L21: an instrument's PASS is a statement
about its domain, not about the world, and every one of the ten instances that
lesson records narrowed what could be seen and therefore produced a PASS. So the
guard is exercised against a deliberately non-deterministic callable it MUST
catch, and against the two shapes that a naive value-only comparison misses:
a dtype-only difference, and a difference confined to one column.
"""
import itertools

import numpy as np
import pandas as pd
import pytest

from leakaudit.determinism import check_frame, frames_equal


def _frame(n=64):
    rng = np.random.default_rng(7)
    return pd.DataFrame({
        "a": rng.integers(0, 100, n),
        "b": rng.normal(size=n),
        "c": rng.integers(0, 2, n).astype(bool),
    })


# --------------------------------------------------------------------------
# KNOWN-POSITIVE: the guard must FIRE on a pipeline that is not deterministic.
# --------------------------------------------------------------------------

def test_known_positive_nondeterministic_build_is_caught():
    counter = itertools.count()

    def flaky(df):
        out = df.copy()
        out["derived"] = out["b"] + next(counter)   # differs run to run
        return out

    r = check_frame(flaky, _frame(), "original")
    assert not r.deterministic, "the guard passed a build that changes every call"
    assert "derived" in r.differing_columns
    assert bool(r) is False


def test_known_positive_names_only_the_columns_that_moved():
    counter = itertools.count()

    def flaky(df):
        out = df.copy()
        out["stable"] = out["b"] * 2.0
        out["moving"] = float(next(counter))
        return out

    r = check_frame(flaky, _frame(), "original")
    assert not r.deterministic
    assert r.differing_columns == ("moving",), r.differing_columns


def test_known_positive_dtype_only_difference_is_caught():
    """Same numbers, different dtype, on the second call.

    A value-only comparison passes this. It must not: a pipeline that returns
    int64 once and float64 the next has changed the frame every downstream
    promotion decision is keyed on (§3.2).
    """
    state = {"n": 0}

    def dtype_flaky(df):
        out = df.copy()
        state["n"] += 1
        out["x"] = (df["a"] * 1).astype("int64" if state["n"] == 1 else "float64")
        return out

    r = check_frame(dtype_flaky, _frame(), "original")
    assert not r.deterministic
    assert r.differing_columns == ("x",)
    assert "int64->float64" in r.detail


def test_known_positive_row_count_change_is_caught():
    state = {"n": 0}

    def shrinking(df):
        state["n"] += 1
        return df.iloc[: len(df) - state["n"]].copy()

    r = check_frame(shrinking, _frame(), "original")
    assert not r.deterministic
    assert "shape differs" in r.detail or "index differs" in r.detail


def test_known_positive_build_that_raises_is_not_reported_deterministic():
    def explode(df):
        raise RuntimeError("boom")

    r = check_frame(explode, _frame(), "original")
    assert not r.deterministic
    assert "boom" in r.detail


# --------------------------------------------------------------------------
# The negative side: a deterministic pipeline must pass, or the guard is a
# blanket refusal rather than a test.
# --------------------------------------------------------------------------

def test_deterministic_build_passes():
    def stable(df):
        out = df.copy()
        out["derived"] = out["b"] * 2.0 + out["a"]
        return out

    r = check_frame(stable, _frame(), "original")
    assert r.deterministic, r.detail
    assert r.differing_columns == ()


def test_nan_in_the_same_cell_is_equality_not_tolerance():
    """Two runs that both produced a null in the same cell agree about it.

    This is positional identity, not a tolerance: no numeric slack is admitted
    anywhere, which §6.9 forbids ("bitwise equality, not a tolerance").
    """
    def with_nan(df):
        out = df.copy()
        out["n"] = np.nan
        return out

    r = check_frame(with_nan, _frame(), "original")
    assert r.deterministic


def test_no_tolerance_is_admitted():
    a = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
    b = pd.DataFrame({"x": [1.0, 2.0, 3.0 + 1e-15]})
    equal, cols, _ = frames_equal(a, b)
    assert not equal, "a 1e-15 difference was absorbed; that is a tolerance"
    assert cols == ("x",)
