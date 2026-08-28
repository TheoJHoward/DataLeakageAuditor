"""B-9 -- one wrapped Probe A run per side, through the registered resolvers.

SC-7(d) as before: one side per process invocation; the harness pairs afterwards.

R153 §1.1: these results are reported SEPARATELY from the published row 7 and
never silently replace it. If the wrapped verdicts differ from the published
run's, that difference is a finding and is reported as one.

    usage: b9_wrapped_side.py --side contaminated|corrected --out result.json
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

import pandas as pd                                      # noqa: E402

from leakaudit import fixture_adapter as fa              # noqa: E402
from leakaudit.availability import (                     # noqa: E402
    AvailabilityModel, run_probe_a)
from leakaudit.availability_trace import (               # noqa: E402
    resolve_all, traces_for)

ap = argparse.ArgumentParser()
ap.add_argument("--side", required=True, choices=["contaminated", "corrected"])
ap.add_argument("--stride", type=int, default=997)
ap.add_argument("--max-cohorts", type=int, default=300)
ap.add_argument("--seed", type=int, default=20260828)
ap.add_argument("--out", required=True)
a = ap.parse_args()

t0 = time.time()
inputs = fa.read_inputs("zc", "2025-01")
model = AvailabilityModel(
    aggregate_frames={"magg": "ts_floor", "trades": "ts_event"},
    decision_column="timestamp")
build = fa.builder_for(inputs, side=a.side)

res = run_probe_a(inputs.raw, build, model, side=a.side,
                  cohort_stride=a.stride, max_cohorts=a.max_cohorts, seed=a.seed)

# ELIGIBILITY, derived not assumed: a picked second is eligible iff some
# aggregate frame carries a row in it. A second with nothing to corrupt
# scheduled nothing, and a trace that claimed otherwise would resolve to
# INCOMPLETE(crash) -- reporting a dead process where the truth is an empty
# probe surface.
picked = [c.second for c in res.cohorts]
pset = set(picked)
have = set()
for fname, keycol in model.aggregate_frames.items():
    f = inputs.frames.get(fname)
    if f is None:
        continue
    k = pd.to_datetime(f[keycol])
    if getattr(k.dt, "tz", None) is not None:
        k = k.dt.tz_convert("UTC").dt.tz_localize(None)
    have |= (set(k.dt.floor("s").unique()) & pset)
eligible = [s for s in picked if s in have]
ineligible = [s for s in picked if s not in have]
print("picked %d second(s): %d eligible (an aggregate row exists), %d not"
      % (len(picked), len(eligible), len(ineligible)))

traces = traces_for(res, eligible, case_id="fixture_%s_zc_2025-01" % a.side)
resolved = resolve_all(traces)          # raises on an illegal pair

rec = {"side": a.side, "seed": a.seed, "stride": a.stride,
       "probe_verdict": res.verdict(),
       "n_picked": len(picked), "n_eligible": len(eligible),
       "n_ineligible_no_aggregate": len(ineligible),
       "determinism_ok": res.determinism_ok,
       "resolved": resolved,
       "seconds": round(time.time() - t0, 1)}

print()
for r in resolved:
    print("  %-10s %-14s x %-18s cohorts=%-4d records=%-4d findings=%d"
          % (r["promotion_status"], r["schedule_state"], r["evidence_outcome"],
             r["n_cohorts"], r["n_records"], r["n_findings"]))
print()
print("probe verdict (unwrapped) : %s" % res.verdict())
pres = [r for r in resolved if r["promotion_status"] == "preserving"][0]
print("contract outcome (wrapped): %s" % pres["evidence_outcome"])
agree = res.verdict() == pres["evidence_outcome"]
rec["agrees_with_unwrapped"] = agree
print("AGREE: %s%s" % (agree, "" if agree else "   <- A DIFFERENCE IS A FINDING (R153 §1.1)"))

pathlib.Path(a.out).write_text(json.dumps(rec, indent=2, default=str), encoding="utf-8")
print("written: %s (%.1fs)" % (a.out, time.time() - t0))
