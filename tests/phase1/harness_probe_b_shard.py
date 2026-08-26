"""B8, sharded — one worker of a parallel column sweep.

WHAT PARALLELISM MAY NOT DO HERE. The probe decides a finding by EXACT equality
between a baseline build and a perturbed one (PREREG.md §6.9: bitwise, not a
tolerance). Anything that changes floating-point reduction order changes those
bytes, and the most likely such thing is thread count: several worker processes
contending for the same cores can each end up with a different BLAS thread count
than a serial run had. A probe that silently produced different numbers in
parallel would not be faster, it would be wrong.

THREE GUARDS, and none of them is an assumption:

  1. **Threads are pinned to one** in every worker, before numpy is imported, so
     the numeric environment is fixed rather than whatever contention produces.
  2. **Each worker publishes its baseline's sha256.** The merge refuses to
     assemble shards whose baselines disagree -- if two workers did not start
     from the same bytes, their findings are not about the same pipeline.
  3. **The serial run is kept alive as an independent reference.** Its results
     for the cohorts it reaches are compared against this run's, cohort by
     cohort. Agreement is evidence that pinning changed nothing; disagreement
     localises it immediately.

Shards are assigned ROUND-ROBIN, not in contiguous blocks: integer columns cost
~152 s (the promoted frame adds a determinism guard, a promoted baseline and a
promoted probe) against ~50 s for a float column, and they are clustered in the
input. Contiguous blocks would hand one worker all of them.

Usage: harness_probe_b_shard.py --shard I --of N
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

from leakaudit import fixture_adapter as fa                       # noqa: E402
from leakaudit.corruption import (                                # noqa: E402
    NAN, SENTINEL, SHUFFLE, Unsupportable, corrupt, promote, promotion_of,
    seed_for)
from leakaudit.determinism import check_frame, frames_equal       # noqa: E402
from leakaudit.probe import DETECTOR_ID, cohort_id_for, domain_statement  # noqa: E402
from protocol.runtime_reference import (                          # noqa: E402
    FailureReason, PromotionStatus)

ap = argparse.ArgumentParser()
ap.add_argument("--shard", type=int, required=True)
ap.add_argument("--of", type=int, required=True)
ap.add_argument("--sym", default="zc")
ap.add_argument("--month", default="2025-01")
ap.add_argument("--side", default="corrected")
args = ap.parse_args()

# Shards are PER-RUN INTERMEDIATES and stay OUT of evidence/. Every file
# under evidence/ needs a manifest line, and a file that is rewritten on
# every run would force a manifest resync per run -- churn in an attested
# tree, for an artifact the merge reconstructs. Only the MERGED result is
# evidence. Override with LEAKAUDIT_B8_SHARD_DIR.
OUT = pathlib.Path(os.environ.get(
    "LEAKAUDIT_B8_SHARD_DIR",
    str(pathlib.Path.home() / ".leakaudit_b8"))) / (
    "probe_b_shard_%d_of_%d.json" % (args.shard, args.of))
CASE = "fixture_%s_%s_%s" % (args.side, args.sym, args.month)
T0 = time.time()


def log(m):
    print("[shard %d/%d %7.1fs] %s" % (args.shard, args.of, time.time() - T0, m),
          flush=True)


def frame_sha(df):
    """A digest of a frame's VALUES AND DTYPES that is stable ACROSS PROCESSES.

    Dtypes are in the digest because a pipeline that returns the same numbers in
    a different dtype has not returned the same frame -- §3.2 keys promotion on
    exactly that.

    ACROSS PROCESSES is the load-bearing part, and the obvious implementation
    gets it wrong. `series.to_numpy().tobytes()` on an OBJECT column serialises
    PyObject POINTERS, not values, and pointers differ between processes. This
    frame has an object column (`month`), so the first version of this function
    produced three different digests from three workers that had in fact built
    identical frames -- an instrument reporting its own defect as a fault in the
    thing it measures, which is the failure mode this tool exists to detect.

    `hash_pandas_object` hashes VALUES and is stable across processes and
    platforms, so it is used instead of raw buffer bytes.
    """
    import pandas as _pd                                  # noqa: PLC0415

    h = hashlib.sha256()
    for c in df.columns:
        h.update(str(c).encode())
        h.update(str(df[c].dtype).encode())
        h.update(_pd.util.hash_pandas_object(df[c], index=False)
                 .to_numpy(dtype="uint64", copy=False).tobytes())
    return h.hexdigest()


log("capturing inputs")
inputs = fa.read_inputs(args.sym, args.month)
build = fa.builder_for(inputs, args.side)
raw = inputs.raw

log("original-frame determinism guard")
g0 = check_frame(build, raw, "original")
if not g0.deterministic:
    OUT.write_text(json.dumps({"shard": args.shard, "fatal": g0.detail}), encoding="utf-8")
    sys.exit("determinism guard failed: %s" % g0.detail)

baseline = build(raw)
base_sha = frame_sha(baseline)
log("baseline %s sha=%s" % ((baseline.shape,), base_sha[:16]))

targets = [(fn, str(c)) for fn, f in raw.items() for c in f.columns
           if "|" not in str(c) and "|" not in fn]
mine = [t for i, t in enumerate(targets) if i % args.of == args.shard]
log("%d of %d cohorts assigned (round-robin)" % (len(mine), len(targets)))

records, depmap, det = [], {}, {"original": g0.detail or "ok"}


def sub(frames, fname, col, series):
    out = dict(frames)
    f = frames[fname].copy(deep=False)
    f[col] = series
    out[fname] = f
    return out


def rec(strat, status, cid, valid, reason=None, feature=None):
    return {"strategy": strat, "promotion": status.value, "cohort": cid,
            "attempted": True, "valid": valid,
            "failure_reason": reason.value if reason else None,
            "feature": feature}


def run_one(base, fname, col, strat, cid, status):
    series = raw[fname][col]
    try:
        bad = corrupt(series, strat, seed=seed_for(fname, col, strat))
    except Unsupportable:
        return [rec(strat, status, cid, False, FailureReason.COMPATIBILITY)], set()
    except Exception:                                       # noqa: BLE001
        # A strategy with no realisation on this dtype is a COMPATIBILITY
        # failure to be recorded, never an exception that ends the sweep. One
        # unhandled TypeError on a datetime column killed four processes
        # fifteen minutes in; the finding is worth less than the run.
        return [rec(strat, status, cid, False, FailureReason.COMPATIBILITY)], set()
    if bad.equals(series):
        return [rec(strat, status, cid, False, FailureReason.CONTROL_ARTIFACT)], set()
    try:
        out = build(sub(raw, fname, col, bad))
    except Exception:                                       # noqa: BLE001
        return [rec(strat, status, cid, False, FailureReason.CRASH)], set()
    if out is None or out.shape[0] != base.shape[0] or not out.index.equals(base.index):
        return [rec(strat, status, cid, False, FailureReason.COMPATIBILITY)], set()
    equal, differing, _ = frames_equal(base, out)
    if equal:
        return [rec(strat, status, cid, True)], set()
    return ([rec(strat, status, cid, True, feature=str(f)) for f in differing],
            {str(f) for f in differing})


def checkpoint(done):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "shard": args.shard, "of": args.of, "case": CASE, "detector": DETECTOR_ID,
        "side": args.side, "threads_pinned": 1,
        "baseline_sha256": base_sha,
        "baseline_shape": list(baseline.shape),
        "domain": domain_statement(),
        "not_probed": list(inputs.not_probed),
        "cohorts_assigned": [cohort_id_for(f, c) for f, c in mine],
        "cohorts_done": done,
        "records": records,
        "dependency_map": {k: sorted(v) for k, v in depmap.items()},
        "determinism": det,
        "elapsed_s": round(time.time() - T0, 1),
        "complete": done == len(mine),
    }, indent=1), encoding="utf-8")


for n, (fname, col) in enumerate(mine, 1):
    cid = cohort_id_for(fname, col)
    series = raw[fname][col]
    moved: set[str] = set()
    for strat in (SHUFFLE, SENTINEL):
        r, mv = run_one(baseline, fname, col, strat, cid, PromotionStatus.PRESERVING)
        records.extend(r)
        moved |= mv
    if promotion_of(NAN, series) is PromotionStatus.PROMOTED:
        pf = sub(raw, fname, col, promote(series))
        g = check_frame(build, pf, "promoted:" + cid)
        det["promoted:" + cid] = g.detail or "ok"
        if not g.deterministic:
            records.append(rec(NAN, PromotionStatus.PROMOTED, cid, False,
                               FailureReason.DETERMINISM))
        else:
            r, mv = run_one(build(pf), fname, col, NAN, cid, PromotionStatus.PROMOTED)
            records.extend(r)
            moved |= mv
    if moved:
        depmap[cid] = sorted(moved)
    log("%2d/%d %-32s %s" % (n, len(mine), cid,
                             "%d feature(s)" % len(moved) if moved else "silent"))
    checkpoint(n)

log("DONE %d cohorts" % len(mine))
