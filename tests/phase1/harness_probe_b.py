"""B8 — Probe B end to end against the acceptance fixture's corrected side.

THIS IS A HARNESS, AND IT LIVES OUTSIDE THE PACKAGE ON PURPOSE. PREREG.md SC-7(b)
and (c) withhold the declared ground-truth map from the tool: a detector graded
against a key it had seen would be measuring retrieval, not discrimination. The
reducers already draw that line -- `compute_runtime_metrics(traces, labels)`
takes `CaseLabels` as a separate argument -- so the map is the harness's to hold
and `leakaudit` never receives it. This file holds no labels either; it is here so
that when scoring is added, it is added on this side of the boundary.

COST, MEASURED RATHER THAN ESTIMATED. Each build is ~25 s over 1.26M rows, and
the cost is feature construction, not I/O. The schedule is the full product --
PREREG.md §6.6 l.1053 forbids terminal short-circuit on the acceptance fixture
gate run, so every configured strategy executes at every selected eligible cohort
regardless of any finding. There is no cheaper honest run.

The per-promoted-frame determinism guard is kept per COLUMN rather than shared
across a single int->float "alignment family". SC-9(e) licenses interpretation
only toward the STRONGER reading, and more guards is stronger.

Results are checkpointed after every cohort so a run that is interrupted leaves
usable evidence rather than nothing.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in (ROOT, ROOT / "src"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from leakaudit import fixture_adapter as fa           # noqa: E402
from leakaudit.corruption import NAN, SENTINEL, SHUFFLE, promotion_of  # noqa: E402
from leakaudit.probe import (                          # noqa: E402
    DETECTOR_ID,
    cohort_id_for,
    domain_statement,
)
from protocol.runtime_reference import (               # noqa: E402
    CombinationTrace,
    EvidenceOutcome,
    ExecutionRecord,
    FailureReason,
    FindingRecord,
    PromotionStatus,
    RunContext,
    derive_evidence_events,
    resolve_state_pair,
)

import pandas as pd                                    # noqa: E402

from leakaudit.corruption import Unsupportable, corrupt  # noqa: E402
from leakaudit.determinism import check_frame, frames_equal  # noqa: E402

OUT = pathlib.Path(os.environ.get(
    "LEAKAUDIT_B8_OUT",
    str(ROOT / "evidence" / "phase1" / "probe_b_zc_2025-01.json")))
SYM, MONTH, SIDE = "zc", "2025-01", "corrected"
CASE = "fixture_%s_%s_%s" % (SIDE, SYM, MONTH)


def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)


T0 = time.time()
log("capturing the fixture's inputs")
inputs = fa.read_inputs(SYM, MONTH)
build = fa.builder_for(inputs, SIDE)
raw = inputs.raw
log("raw: %s" % {k: v.shape for k, v in raw.items()})
log("captured but NOT probed (adapter-unread): %s" % (inputs.not_probed,))

# ---- the original-frame determinism guard, once (§6.10) --------------------
log("original-frame determinism guard (2 builds)")
g0 = check_frame(build, raw, "original")
if not g0.deterministic:
    log("GUARD FAILED: %s" % g0.detail)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"determinism": g0.detail, "records": []}, indent=1),
                   encoding="utf-8")
    sys.exit(1)
baseline = build(raw)
log("baseline: %s" % (baseline.shape,))

targets = [(fn, str(c)) for fn, f in raw.items() for c in f.columns
           if "|" not in str(c) and "|" not in fn]
log("%d source columns across %d frames" % (len(targets), len(raw)))

pres_records, prom_records = [], []
pres_cohorts, prom_cohorts = [], []
depmap: dict[str, list[str]] = {}
det = {"original": g0.detail or "ok"}


def sub(frames, fname, col, series):
    out = dict(frames)
    f = frames[fname].copy(deep=False)
    f[col] = series
    out[fname] = f
    return out


def run_one(frames, base, fname, col, strat, cid, status):
    series = frames[fname][col]
    try:
        bad = corrupt(series, strat, seed=abs(hash((fname, col, strat))) % (2 ** 31))
    except Unsupportable:
        return [ExecutionRecord(DETECTOR_ID, CASE, strat, status, cid, True, False,
                                failure_reason=FailureReason.COMPATIBILITY)], set()
    if bad.equals(series):
        return [ExecutionRecord(DETECTOR_ID, CASE, strat, status, cid, True, False,
                                failure_reason=FailureReason.CONTROL_ARTIFACT)], set()
    try:
        out = build(sub(frames, fname, col, bad))
    except Exception:                                   # noqa: BLE001
        return [ExecutionRecord(DETECTOR_ID, CASE, strat, status, cid, True, False,
                                failure_reason=FailureReason.CRASH)], set()
    if out is None or out.shape[0] != base.shape[0] or not out.index.equals(base.index):
        return [ExecutionRecord(DETECTOR_ID, CASE, strat, status, cid, True, False,
                                failure_reason=FailureReason.COMPATIBILITY)], set()
    equal, differing, _ = frames_equal(base, out)
    if equal:
        return [ExecutionRecord(DETECTOR_ID, CASE, strat, status, cid, True, True,
                                finding=None)], set()
    return ([ExecutionRecord(DETECTOR_ID, CASE, strat, status, cid, True, True,
                             finding=FindingRecord(str(f), cid, cid))
             for f in differing],
            {str(f) for f in differing})


def checkpoint():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "case": CASE, "detector": DETECTOR_ID, "side": SIDE,
        "domain": domain_statement(),
        "not_probed": list(inputs.not_probed),
        "not_probed_reason":
            "captured but never read under the adapter: serving the MBO aggregate "
            "means the builder does not open the raw frame, so a probe of its "
            "columns would record silence the adapter caused",
        "raw_shapes": {k: list(v.shape) for k, v in raw.items()},
        "baseline_columns": [str(c) for c in baseline.columns],
        "determinism": det,
        "cohorts_done": len(pres_cohorts),
        "cohorts_total": len(targets),
        "dependency_map": {k: sorted(v) for k, v in depmap.items()},
        "elapsed_s": round(time.time() - T0, 1),
    }, indent=1), encoding="utf-8")


for n, (fname, col) in enumerate(targets, 1):
    cid = cohort_id_for(fname, col)
    pres_cohorts.append(cid)
    series = raw[fname][col]
    moved: set[str] = set()

    for strat in (SHUFFLE, SENTINEL):
        recs, mv = run_one(raw, baseline, fname, col, strat, cid,
                           PromotionStatus.PRESERVING)
        pres_records.extend(recs)
        moved |= mv

    if promotion_of(NAN, series) is PromotionStatus.PROMOTED:
        prom_cohorts.append(cid)
        pf = sub(raw, fname, col, series.astype("float64"))
        g = check_frame(build, pf, "promoted:" + cid)
        det["promoted:" + cid] = g.detail or "ok"
        if not g.deterministic:
            prom_records.append(ExecutionRecord(
                DETECTOR_ID, CASE, NAN, PromotionStatus.PROMOTED, cid, True, False,
                failure_reason=FailureReason.DETERMINISM))
        else:
            recs, mv = run_one(raw, build(pf), fname, col, NAN, cid,
                               PromotionStatus.PROMOTED)
            prom_records.extend(recs)
            moved |= mv

    if moved:
        depmap[cid] = sorted(moved)
    log("%3d/%d %-34s %s" % (n, len(targets), cid,
                             "%d feature(s)" % len(moved) if moved else "silent"))
    checkpoint()

preserving = CombinationTrace(
    DETECTOR_ID, CASE, PromotionStatus.PRESERVING, RunContext.FIXTURE,
    (SHUFFLE, SENTINEL) if pres_cohorts else (), tuple(pres_cohorts),
    True, False, tuple(pres_records))
promoted = CombinationTrace(
    DETECTOR_ID, CASE, PromotionStatus.PROMOTED, RunContext.FIXTURE,
    (NAN,) if prom_cohorts else (), tuple(prom_cohorts),
    True, False, tuple(prom_records))

summary = {}
for t in (preserving, promoted):
    state, outcome = resolve_state_pair(t)          # raises on an illegal pair
    summary[t.promotion_status.value] = {
        "schedule_state": state.kind.value,
        "reason": state.reason.value if state.reason else None,
        "evidence_outcome": outcome.value,
        "cohorts": len(t.selected_eligible_cohorts),
        "strategies": list(t.resolved_strategies),
        "records": len(t.records),
    }
events = derive_evidence_events((preserving, promoted))

checkpoint()
data = json.loads(OUT.read_text(encoding="utf-8"))
data["traces"] = summary
data["evidence_events"] = len(events)
data["proven_licensed_events"] = sum(1 for e in events if e.licenses_proven)
data["complete"] = True
OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
log("DONE  traces=%s events=%d" % (summary, len(events)))
