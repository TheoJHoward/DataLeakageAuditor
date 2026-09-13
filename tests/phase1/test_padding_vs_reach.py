"""A declared padding below the MEASURED reach is refused. R269 §2(a).

R267 §2(d) wired `check_padding` into the slice branch of `run_probe_a`, so a
declared padding is compared against the builder's measured reach and not only
against the model's floor. R269 §2(a) asked to confirm that. On disk it was wired
-- and **no test had ever caused it to fire**, which is a check whose green
nobody had earned. This is its known positive, with the negative beside it.

HELD: the frame, the builder, the slice point. VARIED: the declared padding only.
The frame reaches 60 s back from the slice, so `plan_slice`'s own data check
passes for both paddings, and both clear the model's 1 s floor -- the only thing
separating them is the builder's measured reach of ~59.5 s.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src"), str(ROOT / "tests" / "phase1")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.availability import run_probe_a                  # noqa: E402
from leakaudit.reach import ReachError                         # noqa: E402
from test_slicing import (LOOKBACK, MODEL, SLICE_AT, STRIDE,    # noqa: E402
                          _full, _leaky_build)


def _probe(padding):
    return run_probe_a(_full(), _leaky_build, MODEL, side="t",
                       cohort_stride=STRIDE, max_cohorts=1,
                       slice_from=SLICE_AT, padding=padding)


def test_a_padding_that_CLEARS_THE_FLOOR_but_sits_BELOW_THE_MEASURED_REACH_is_REFUSED():
    with pytest.raises(ReachError) as e:
        _probe(pd.Timedelta(seconds=10))
    msg = str(e.value)
    assert "THIS BUILDER REACHES" in msg, "the refusal names the measurement"
    assert "the declared padding" in msg
    assert "0 days 00:00:10" in msg, "and the number it was given"


def test_the_NEGATIVE_a_padding_ABOVE_the_measured_reach_is_accepted():
    """Without this, a refusal firing on every padding would look identical."""
    res = _probe(pd.Timedelta(seconds=LOOKBACK))
    assert res.reach is not None and res.reach.measured is not None
    assert pd.Timedelta(seconds=LOOKBACK) > res.reach.measured
    assert res.verdict() == "finding"
