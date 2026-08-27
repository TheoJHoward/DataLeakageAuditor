"""B-7 -- Probe A against ONE side of the acceptance fixture. R151 §4.

ONE SIDE PER PROCESS INVOCATION. SC-7(d) is a hard sequencing rule: "a single run
given more than one side satisfies none of the criteria, however its outputs are
partitioned afterwards." The harness compares the two runs afterwards -- which is
what the six comparator rows already are.

SC-7(a): this run receives the pipeline for its side and the declared
availability model. It never receives the paired side and never the R9
ground-truth map.

    usage: b7_probe_a_side.py --side contaminated|corrected --out result.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

_ROOT = pathlib.Path(__file__).resolve().parents[2]
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                        # noqa: BLE001
    pass

from leakaudit import fixture_adapter as fa              # noqa: E402
from leakaudit.availability import (                     # noqa: E402
    AvailabilityModel, ProbeError, run_probe_a)

ap = argparse.ArgumentParser()
ap.add_argument("--side", required=True, choices=["contaminated", "corrected"])
ap.add_argument("--sym", default="zc")
ap.add_argument("--month", default="2025-01")
ap.add_argument("--stride", type=int, default=997)
ap.add_argument("--max-cohorts", type=int, default=300)
ap.add_argument("--out", required=True)
a = ap.parse_args()

t0 = time.time()
inputs = fa.read_inputs(a.sym, a.month)
print("read_inputs %s %s in %.1fs" % (a.sym, a.month, time.time() - t0))

# THE MODEL, from the declaration. The join families' declared availability
# instant is `ts_floor + 1s` -- the at_source_timestamp truth, not the
# at_bar_close approximation, which the declaration says in terms would find the
# contaminated side clean.
#
# `magg` is already keyed by ts_floor. `trades` carries raw event stamps that the
# builder floors the same way, so its key is ts_event and the probe floors it.
# `snap` is the DECISION frame, not an aggregate, and is not corrupted.
model = AvailabilityModel(
    aggregate_frames={"magg": "ts_floor", "trades": "ts_event"},
    decision_column="timestamp")

build = fa.builder_for(inputs, side=a.side)
print("side=%s stride=%d max_cohorts=%d" % (a.side, a.stride, a.max_cohorts))

t1 = time.time()
try:
    res = run_probe_a(inputs.raw, build, model, side=a.side,
                      cohort_stride=a.stride, max_cohorts=a.max_cohorts)
    err = None
except ProbeError as e:
    res, err = None, str(e)

rec = {"side": a.side, "sym": a.sym, "month": a.month,
       "stride": a.stride, "max_cohorts": a.max_cohorts,
       "seconds": round(time.time() - t1, 1)}
if res is None:
    rec.update(verdict="could_not_run(probe_error)", detail=err)
    print("PROBE ERROR: %s" % err)
else:
    infd = sum(c.moved_in_second for c in res.cohorts)
    nxt = sum(c.moved_next_second for c in res.cohorts)
    rows = sum(c.rows_in_second for c in res.cohorts)
    rec.update(verdict=res.verdict(), determinism_ok=res.determinism_ok,
               n_cohorts=res.n_cohorts, cohorts_with_finding=len(res.findings),
               rows_in_probed_seconds=rows,
               moved_in_second=infd, moved_next_second=nxt,
               notes=res.notes,
               per_cohort=[{"second": str(c.second), "rows": c.rows_in_second,
                            "moved_in_second": c.moved_in_second,
                            "moved_next_second": c.moved_next_second}
                           for c in res.cohorts[:40]])
    print("verdict            : %s" % res.verdict())
    print("cohorts            : %d (%d with a finding)" % (res.n_cohorts, len(res.findings)))
    print("rows in those secs : %d" % rows)
    print("moved IN-second    : %d   <- unavailable-cell dependence" % infd)
    print("moved NEXT-second  : %d   <- available-cell dependence (expected, both sides)" % nxt)
    for n in res.notes:
        print("note: %s" % n)

pathlib.Path(a.out).write_text(json.dumps(rec, indent=2, default=str), encoding="utf-8")
print("written: %s  (%.1fs total)" % (a.out, time.time() - t0))
