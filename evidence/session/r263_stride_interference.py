"""R263 §2. Batched cohorts interfering at stride 1, measured on a CLEAN pipeline.

    PYTHONPATH=. py -3.12 evidence/session/r263_stride_interference.py

THE GROUND TRUTH IS KNOWN AND IT IS "NO LEAK". The builder reads the PREVIOUS
second's aggregate. Under the frame rule that cell's declared instant is
`floor(k) + window`, which is at or before the reading row's decision instant, so
it is AVAILABLE and no row is a finding. Every finding this probe reports on
this fixture is therefore false, and the count of them is the interference.

WHERE THE INTERFERENCE COMES FROM. `run_probe_a` corrupts every probed second in
ONE rebuild. Cohort F's finding region is `[F, min_B a(j))`. A row in it may
legitimately read a cell belonging to an EARLIER cohort -- that cell is available
to it, which is why reading it is legitimate -- and when that earlier cohort is
also probed, the row moves and is counted as F's finding. The cohorts do not
overlap; the INFLUENCE of their cells does.

WHY THIS IS THE DERIVED STRIDE'S KNOWN POSITIVE. R261 §1(b) derived a separation
and compared it to the smallest probed gap. The derived value was the finding
region's width, `min_B a(j) - F`, which at a one-second window is one second --
so stride 1 gives a gap EQUAL to it and the check passes. The interference below
happens at exactly that point, so the derived quantity was the wrong one, and the
one that matches the measurement is the ATTRIBUTION WINDOW, `max_B a(j) + 1s - F`.

Written with the Write tool per D2.1. Read-only against the repository.
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

REPO = pathlib.Path.cwd()
for p in (str(REPO), str(REPO / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.availability import (AvailabilityModel,            # noqa: E402
                                    ProbeError, run_probe_a)

T0 = pd.Timestamp("2026-01-01 00:00:00")
SEC = pd.Timedelta(seconds=1)
N = 40
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")


def frames():
    return {"agg": pd.DataFrame({"k": [T0 + i * SEC for i in range(N)],
                                 "v": np.arange(N, dtype="float64")})}


def build(raw):
    """Reads the PREVIOUS second's aggregate. LEGITIMATE, by construction."""
    agg = raw["agg"]
    v = agg["v"].to_numpy()
    return pd.DataFrame({"d": agg["k"].to_numpy(),
                         "x": np.concatenate(([np.nan], v[:-1]))})


def main() -> int:
    print("=" * 74)
    print("R263 section 2 -- stride interference on a pipeline with NO leak")
    print("=" * 74)
    print("%d aggregate rows, one decision row per second, window 1s." % N)
    print("The builder reads the previous second's cell, whose instant is at or")
    print("before the decision instant. Every finding below is FALSE.")
    print()
    print("MEASURED BEFORE THE R263 REPAIR, and recorded because a repair's")
    print("known positive has to stay re-readable after it stops reproducing:")
    print("  stride 1  ->  40 cohorts,  39 FALSE findings, verdict `finding`")
    print("  stride 2  ->  20 cohorts,   0 false findings, `observed_silence`")
    print("  stride 3  ->  14 cohorts,   0 false findings, `observed_silence`")
    print("  stride 4  ->  10 cohorts,   0 false findings, `observed_silence`")
    print("  stride 7  ->   6 cohorts,   0 false findings, `observed_silence`")
    print()
    print("AS IT BEHAVES NOW. Stride 1 is below the derived floor and refuses;")
    print("everything from stride 2 runs and is clean:")
    print()
    print("%-8s %9s %10s %10s %26s" % ("stride", "cohorts", "FALSE", "liveness",
                                       "verdict"))
    for stride in (1, 2, 3, 4, 7):
        try:
            res = run_probe_a(frames(), build, MODEL, side="s%d" % stride,
                              cohort_stride=stride, max_cohorts=40)
        except ProbeError as e:
            first = str(e).splitlines()[0]
            print("%-8d %9s %10s %10s %26s" % (stride, "-", "-", "-", "REFUSED"))
            print("         %s" % first)
            continue
        false = sum(c.moved_in_second for c in res.cohorts)
        print("%-8d %9d %10d %10d %26s"
              % (stride, res.n_cohorts, false, res.liveness, res.verdict()))
    print()

    print("AND UNDECLARED, which is the third state:")
    res = run_probe_a(frames(), build, MODEL, side="derived", max_cohorts=40)
    for n in res.notes:
        if "NOT DECLARED" in n:
            print("  " + n[:230])
    print("  cohorts %d, false findings %d, verdict %s"
          % (res.n_cohorts, sum(c.moved_in_second for c in res.cohorts),
             res.verdict()))
    print()
    print("THE TWO CANDIDATE FLOORS, at this window:")
    print("  finding-region width  max(min_a - F)      = 1s -> stride 1 PASSES")
    print("  attribution window    max(max_a + 1s - F) = 2s -> stride 1 REFUSED")
    print("  The measurement above chooses between them: interference at")
    print("  stride 1, none from stride 2. R261 derived the first.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
