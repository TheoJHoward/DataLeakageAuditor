"""R264 §2(b). Every recorded figure produced at stride 1, re-measured at the floor.

    PYTHONPATH=. py -3.12 evidence/session/r264_stride_remeasure.py

WHY. R263 measured 39 false findings at stride 1 on a pipeline with no leak:
batched cohorts one second apart let a cell corrupted for one cohort move a row
the next counts as its finding. Any recorded figure produced at stride 1 with
BATCHED cohorts is therefore suspect and is re-measured under the derived floor.
The old figure is kept, dated and superseded; it is never replaced in place.

WHICH FIGURES ARE IN SCOPE, and the criterion is mechanical rather than a
judgment: a figure is in scope when the run that produced it (i) probed more
than one cohort and (ii) corrupted them in ONE rebuild. L2a fails (ii) -- it
rebuilds per cohort, so no two cohorts share a batch and no moved row lies in
two of them -- so its figures are out of scope for this defect whatever stride
they used, and that is stated rather than assumed.

Written with the Write tool per D2.1. Read-only against the repository.
"""
from __future__ import annotations

import pathlib
import sys

import pandas as pd

REPO = pathlib.Path.cwd()
for p in (str(REPO), str(REPO / "src"), str(REPO / "tests" / "phase1")):
    if p not in sys.path:
        sys.path.insert(0, p)

import test_slicing as sl                                        # noqa: E402
from leakaudit.availability import ProbeError, run_probe_a       # noqa: E402


def probe(frames, stride, **kw):
    return run_probe_a(frames, sl._leaky_build, sl.MODEL, side="remeasure",
                       cohort_stride=stride, max_cohorts=400, **kw)


def row(label, stride, frames, **kw):
    try:
        res = probe(frames, stride, **kw)
    except ProbeError as e:
        return (label, stride, "-", "-", "REFUSED: " + str(e).split(":")[0])
    return (label, stride, res.n_cohorts, len(res.findings), res.verdict())


def main() -> int:
    print("=" * 78)
    print("R264 section 2(b) -- figures produced at stride 1, re-measured")
    print("=" * 78)
    print("Fixture: tests/phase1/test_slicing, imported not copied.")
    print()
    lookback = pd.Timedelta(seconds=sl.LOOKBACK)
    rows = [
        row("D pair, unpadded (cut frame)", 1, sl._truncate(sl._full(), sl.SLICE_AT)),
        row("D pair, unpadded (cut frame)", 2, sl._truncate(sl._full(), sl.SLICE_AT)),
        row("D pair, padded", 1, sl._full(),
            slice_from=sl.SLICE_AT, padding=lookback),
        row("D pair, padded", 2, sl._full(),
            slice_from=sl.SLICE_AT, padding=lookback),
        row("residual hole (2s padding)", 2,
            sl._truncate(sl._full(), sl.SLICE_AT - pd.Timedelta(seconds=2)),
            slice_from=sl.SLICE_AT, padding=pd.Timedelta(seconds=2)),
    ]
    print("%-30s %7s %9s %9s  %s"
          % ("figure", "stride", "cohorts", "findings", "verdict"))
    for r in rows:
        print("%-30s %7s %9s %9s  %s" % r)
    print()
    print("THE RECORDED FIGURES THESE SUPERSEDE, with their dates:")
    print("  D-V30A-95 / R255, and FEATURE_BACKLOG.md: `same 30 probed cohorts:")
    print("  unpadded -> observed_silence, 0 findings; padded -> finding, 30`.")
    print("  Produced at stride 1. Kept as written; the rows above are beside")
    print("  them, not over them.")
    print()
    print("OUT OF SCOPE, by the criterion rather than by inspection:")
    print("  L2a's pair and D-V30A-101's nine-of-ten. L2a rebuilds ONCE PER")
    print("  COHORT, so no two cohorts share a batch and the interference this")
    print("  re-measurement is about cannot arise at any stride. Its recorded")
    print("  runs used stride 7 regardless.")
    print("  R205's 25-against-0 (D-V30A-49, D-V30A-100): stride 13, above the")
    print("  2s floor.")
    print("  The clock pair's 3-against-0 (R236): stride 97, above the floor.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
