"""B9, sharded -- one worker running `valueread` and `nullread` over the fixture.

WHAT IS DIFFERENT FROM B8's HARNESS, AND WHY THAT MATTERS. B8's shard worker
reimplemented the probe loop so it could shard it. This one does not: it calls
`leakaudit.detectors` with a `cohorts=` subset and serialises the result. The
thing under test is therefore the SHIPPED code path, not a transcription of it
(H-L26: do not transcribe the thing under test). A harness that reimplements
the detector can pass while the detector is broken, and B8's did carry that
risk even though it did not realise it.

THE SAME THREE GUARDS AS B8, because none of them was about B8 specifically:

  1. **Threads pinned to one** before numpy is imported, so exact comparison
     (§6.9: bitwise, not a tolerance) is not at the mercy of BLAS contention.
  2. **Each worker publishes its baseline's sha256**, value-based via
     `hash_pandas_object` -- buffer bytes hash PyObject pointers on object
     columns and differ between processes for frames that are identical.
  3. **Cohorts are partitioned, and the merge checks the partition** rather
     than trusting it. A dropped cohort reads downstream as silence.

Round-robin, not contiguous blocks: the integer columns cost several times a
float column (a promoted frame adds a determinism guard, a promoted baseline
and a promoted probe, and `nullread` puts every integer column on its promoted
side), and they are clustered in the input.

Usage: harness_b9_shard.py --shard I --of N
"""
from __future__ import annotations

import os

# Pinned BEFORE numpy/pandas are imported anywhere -- these are read at import.
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"

import argparse            # noqa: E402
import hashlib             # noqa: E402
import json                # noqa: E402
import pathlib             # noqa: E402
import sys                 # noqa: E402
import time                # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in (ROOT, ROOT / "src"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import pandas as pd                                               # noqa: E402

from leakaudit import fixture_adapter as fa                       # noqa: E402
from leakaudit.detectors import (                                 # noqa: E402
    NULL_DETECTOR_ID, VALUE_DETECTOR_ID, null_domain_statement,
    probe_nulls, probe_values, value_domain_statement)
from leakaudit.determinism import check_frame                     # noqa: E402
from leakaudit.probe import cohort_id_for                         # noqa: E402
from protocol.runtime_reference import RunContext                 # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--shard", type=int, required=True)
ap.add_argument("--of", type=int, required=True)
ap.add_argument("--sym", default="zc")
ap.add_argument("--month", default="2025-01")
ap.add_argument("--side", default="corrected")
args = ap.parse_args()

# Shards are PER-RUN INTERMEDIATES and stay OUT of evidence/: every file under
# evidence/ needs a manifest line, and one rewritten on every run would force a
# manifest resync per run. Only the MERGED result is evidence.
OUT = pathlib.Path(os.environ.get(
    "LEAKAUDIT_B9_SHARD_DIR",
    str(pathlib.Path.home() / ".leakaudit_b9"))) / (
    "b9_shard_%d_of_%d.json" % (args.shard, args.of))
OUT.parent.mkdir(parents=True, exist_ok=True)
CASE = "fixture_%s_%s_%s" % (args.side, args.sym, args.month)
T0 = time.time()


def log(m):
    print("[b9 shard %d/%d %7.1fs] %s" % (args.shard, args.of, time.time() - T0, m),
          flush=True)


def frame_sha(df) -> str:
    """A digest of a frame's VALUES AND DTYPES, stable ACROSS PROCESSES.

    Dtypes are in the digest because a pipeline returning the same numbers in a
    different dtype has not returned the same frame -- §3.2 keys promotion on
    exactly that. `hash_pandas_object` hashes VALUES; the obvious
    `to_numpy().tobytes()` hashes PyObject pointers on an object column and
    differs between processes for identical frames, which is how an earlier
    version of this function accused the pipeline of its own defect.
    """
    h = hashlib.sha256()
    for c in df.columns:
        h.update(str(c).encode())
        h.update(str(df[c].dtype).encode())
        h.update(pd.util.hash_pandas_object(df[c], index=False)
                 .to_numpy(dtype="uint64", copy=False).tobytes())
    return h.hexdigest()


def serialise(result, detector_id):
    """A trace pair as plain data. The MERGE rebuilds the traces, so nothing
    here decides a schedule state -- that resolution belongs to the reducers
    and happens once, over the assembled population."""
    out = {"detector": detector_id, "domain": result.domain, "records": [],
           "dependency_map": {k: list(v) for k, v in result.dependency_map.items()},
           "cohorts": {}}
    for t in result.traces:
        key = t.promotion_status.value
        out["cohorts"][key] = list(t.selected_eligible_cohorts)
        out.setdefault("strategies", {})[key] = list(t.resolved_strategies)
        for r in t.records:
            out["records"].append({
                "promotion": key, "strategy": r.strategy_id,
                "cohort": r.cohort_id, "attempted": r.attempted,
                "valid": r.valid,
                "failure_reason": (r.failure_reason.value
                                   if r.failure_reason else None),
                "feature": r.finding.feature if r.finding else None})
    return out


log("capturing inputs")
inputs = fa.read_inputs(args.sym, args.month)
build = fa.builder_for(inputs, args.side)
raw = inputs.raw

log("original-frame determinism guard")
g0 = check_frame(build, raw, "original")
if not g0.deterministic:
    OUT.write_text(json.dumps({"shard": args.shard, "fatal": g0.detail}),
                   encoding="utf-8")
    sys.exit("determinism guard failed: %s" % g0.detail)

base_sha = frame_sha(build(raw))
log("baseline sha=%s" % base_sha[:16])

targets = [cohort_id_for(fn, str(c)) for fn, f in raw.items() for c in f.columns
           if "|" not in str(c) and "|" not in fn]
mine = tuple(t for i, t in enumerate(targets) if i % args.of == args.shard)
log("%d of %d cohorts assigned (round-robin)" % (len(mine), len(targets)))

detectors = []
for det_id, fn in ((VALUE_DETECTOR_ID, probe_values), (NULL_DETECTOR_ID, probe_nulls)):
    log("running %s over %d cohorts" % (det_id, len(mine)))
    r = fn(raw, build, case_id=CASE, run_context=RunContext.FIXTURE,
           bare=False, cohorts=mine)
    detectors.append(serialise(r, det_id))
    fired = len(r.dependency_map)
    log("%s: %d fired, %d silent" % (det_id, fired, len(mine) - fired))

OUT.write_text(json.dumps({
    "shard": args.shard, "of": args.of, "case": CASE,
    "baseline_sha256": base_sha, "complete": True,
    "cohorts_assigned": list(mine),
    # The adapter's OWN accounting of what it captured and deliberately did not
    # serve, not a set difference computed here. The 8.2M-row MBO frame is
    # excluded because serving `magg` from memory means the builder never opens
    # it -- probing it would record a silence the adapter caused.
    "not_probed": list(inputs.not_probed),
    "domains": {VALUE_DETECTOR_ID: value_domain_statement(),
                NULL_DETECTOR_ID: null_domain_statement()},
    "detectors": detectors,
}, indent=1), encoding="utf-8")
log("wrote %s" % OUT)
