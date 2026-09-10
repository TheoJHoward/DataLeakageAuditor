"""R262 §7(c). What a cohort costs, on each runtime row, at fixture scale.

    LEAKAUDIT_FIXTURE=1 PYTHONPATH=. py -3.12 evidence/session/r262_cost_per_cohort.py

MEASURED, NOT ESTIMATED, and the two rows have different shapes so a single
"cost per cohort" would be a false figure for one of them:

    L3.1  corrupts every probed second in ONE rebuild. Its cost is one build
          plus classification, so cohorts are nearly free after the first.
    L2a   corrupts the cells unavailable at ONE cohort and rebuilds, per cohort.
          That is the registered `C x S` term (DESIGN.md section 5.1) and it
          makes cohorts LINEAR in the builder's own cost.

For CI that asymmetry is the whole question, so it is measured as a SLOPE rather
than as one number: each row is timed at several cohort counts and the marginal
cost of a cohort is read off the difference.

THE FIXTURE CAPTURE IS TIMED AND EXCLUDED from the slopes. It happens once per
process and would otherwise be charged to whichever run went first.

Written with the Write tool per D2.1. Read-only against the repository.
"""
from __future__ import annotations

import os
import pathlib
import sys
import time

import pandas as pd

REPO = pathlib.Path.cwd()
for p in (str(REPO), str(REPO / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import fixture_adapter as fa                       # noqa: E402
from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402
from leakaudit.label_probe import (LabelAvailability,             # noqa: E402
                                   RawLabel, run_probe_l2a)

SYM, MONTH, STRIDE, SEED = "zc", "2025-01", 997, 20260828
MODEL = AvailabilityModel(
    aggregate_frames={"magg": "ts_floor", "trades": "ts_event"},
    decision_column="timestamp")


def main() -> int:
    if not os.environ.get("LEAKAUDIT_FIXTURE"):
        print("REFUSED: set LEAKAUDIT_FIXTURE=1. This reads the acceptance "
              "fixture and takes minutes; it does not run by accident.")
        return 1

    t0 = time.time()
    cap = fa.read_inputs(SYM, MONTH)
    capture = time.time() - t0
    build = fa.builder_for(cap, "contaminated")
    rows = sum(len(f) for f in cap.raw.values())
    print("=" * 76)
    print("R262 section 7(c) -- cost per cohort, both runtime rows, %s %s"
          % (SYM, MONTH))
    print("=" * 76)
    print("capture %.0f s (once per process, excluded below)" % capture)
    print("raw rows across %d probed frame(s): %d" % (len(cap.raw), rows))

    t = time.time()
    base = build(dict(cap.raw))
    one_build = time.time() - t
    print("one clean build: %.1f s, output %d rows x %d cols"
          % (one_build, len(base), len(base.columns)))
    print()

    print("L3.1 -- one rebuild for ALL probed cohorts")
    print("%-10s %10s %14s" % ("cohorts", "seconds", "marginal/cohort"))
    prev_n = prev_t = None
    for n in (1, 5, 25):
        t = time.time()
        run_probe_a(cap.raw, build, MODEL, side="cost", cohort_stride=STRIDE,
                    max_cohorts=n, seed=SEED)
        el = time.time() - t
        marg = "" if prev_t is None else "%.3f s" % ((el - prev_t) / (n - prev_n))
        print("%-10d %10.1f %14s" % (n, el, marg))
        prev_n, prev_t = n, el
    print()

    print("L2a -- one rebuild PER cohort (the registered `C x S` term)")
    print("%-10s %10s %14s" % ("cohorts", "seconds", "marginal/cohort"))
    lab = LabelAvailability(base_column="ts_floor",
                            horizon=pd.Timedelta(seconds=60))
    prev_n = prev_t = None
    for n in (1, 2, 4):
        t = time.time()
        run_probe_l2a(cap.raw, build, MODEL, side="cost",
                      raw_label=RawLabel("magg", "total_events"),
                      label_availability=lab,
                      cohort_stride=STRIDE, max_cohorts=n, seed=SEED)
        el = time.time() - t
        marg = "" if prev_t is None else "%.1f s" % ((el - prev_t) / (n - prev_n))
        print("%-10d %10.1f %14s" % (n, el, marg))
        prev_n, prev_t = n, el
    print()
    print("total wall time %.0f s" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
