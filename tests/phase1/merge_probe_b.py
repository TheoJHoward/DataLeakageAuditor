"""Assemble the sharded column sweep into the two CombinationTraces.

THE MERGE IS WHERE PARALLELISM IS MADE SAFE, not where it is assumed safe. Three
things are checked before any trace is built, and each is a refusal rather than a
warning:

  1. **Every shard reports the same baseline digest.** Workers that did not start
     from the same bytes did not probe the same pipeline, and their findings
     cannot be pooled. The digest is value-based (`hash_pandas_object`), because
     the obvious buffer-bytes version hashes PyObject pointers on object columns
     and differs between processes for frames that are in fact identical.
  2. **The shards' cohort assignments partition the population** — every cohort
     covered exactly once, none missing, none duplicated. A silently dropped
     cohort would read downstream as `observed_silence`, which is a finding-
     shaped absence and the worst way to lose work.
  3. **Every shard is complete.** A partial shard's cohorts are absent, not
     silent, and the difference matters.

Then the records are rebuilt into the two combinations §6.6 requires — a case has
exactly two, keyed by promotion status — and handed to the reducers UNCHANGED. If
a reducer rejects the result, the trace is wrong, not the reducer.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in (ROOT, ROOT / "src"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from leakaudit.corruption import NAN, SENTINEL, SHUFFLE          # noqa: E402
from leakaudit.probe import DETECTOR_ID                          # noqa: E402
from protocol.runtime_reference import (                         # noqa: E402
    CombinationTrace,
    ExecutionRecord,
    FailureReason,
    FindingRecord,
    PromotionStatus,
    RunContext,
    derive_evidence_events,
    resolve_state_pair,
)

EV = ROOT / "evidence" / "phase1"
SHARD_DIR = pathlib.Path(os.environ.get(
    "LEAKAUDIT_B8_SHARD_DIR", str(pathlib.Path.home() / ".leakaudit_b8")))
shards = sorted(SHARD_DIR.glob("probe_b_shard_*_of_*.json"))
if not shards:
    sys.exit("HALT: no shard files under %s" % SHARD_DIR)

data = [json.loads(p.read_text(encoding="utf-8")) for p in shards]

# ---- guard 1: one baseline ------------------------------------------------
bases = {d.get("baseline_sha256") for d in data}
if len(bases) != 1 or None in bases:
    sys.exit("HALT: shards disagree on the baseline (%s). They did not probe the "
             "same pipeline, so their findings cannot be pooled." % sorted(bases))
baseline_sha = bases.pop()

# ---- guard 2: complete shards ---------------------------------------------
partial = [d["shard"] for d in data if not d.get("complete")]
if partial:
    sys.exit("HALT: shard(s) %s did not finish. Their cohorts are ABSENT, not "
             "silent, and merging would present the gap as coverage." % partial)

# ---- guard 3: an exact partition ------------------------------------------
assigned: dict[str, int] = {}
dupes = []
for d in data:
    for cid in d["cohorts_assigned"]:
        if cid in assigned:
            dupes.append(cid)
        assigned[cid] = d["shard"]
if dupes:
    sys.exit("HALT: cohort(s) covered by more than one shard: %s" % sorted(set(dupes)))

expected_of = {d["of"] for d in data}
if len(expected_of) != 1 or len(data) != expected_of.copy().pop():
    sys.exit("HALT: expected %s shards, found %d" % (expected_of, len(data)))

case = {d["case"] for d in data}.pop()
REASONS = {r.value: r for r in FailureReason}

pres, prom = [], []
depmap: dict[str, list[str]] = {}
det: dict[str, str] = {}
for d in data:
    det.update(d["determinism"])
    for cid, feats in d["dependency_map"].items():
        depmap[cid] = feats
    for r in d["records"]:
        status = (PromotionStatus.PRESERVING if r["promotion"] == "preserving"
                  else PromotionStatus.PROMOTED)
        rec = ExecutionRecord(
            detector_id=DETECTOR_ID, case_id=case, strategy_id=r["strategy"],
            promotion_status=status, cohort_id=r["cohort"],
            attempted=r["attempted"], valid=r["valid"],
            finding=(FindingRecord(r["feature"], r["cohort"], r["cohort"])
                     if r.get("feature") else None),
            failure_reason=(REASONS[r["failure_reason"]]
                            if r.get("failure_reason") else None))
        (pres if status is PromotionStatus.PRESERVING else prom).append(rec)

pres_cohorts = sorted({r.cohort_id for r in pres})
prom_cohorts = sorted({r.cohort_id for r in prom})

preserving = CombinationTrace(
    DETECTOR_ID, case, PromotionStatus.PRESERVING, RunContext.FIXTURE,
    (SHUFFLE, SENTINEL) if pres_cohorts else (), tuple(pres_cohorts),
    True, False, tuple(pres))
promoted = CombinationTrace(
    DETECTOR_ID, case, PromotionStatus.PROMOTED, RunContext.FIXTURE,
    (NAN,) if prom_cohorts else (), tuple(prom_cohorts),
    True, False, tuple(prom))

out = {"case": case, "detector": DETECTOR_ID,
       "baseline_sha256": baseline_sha,
       "shards": len(data), "threads_pinned": 1,
       "domain": data[0]["domain"],
       "not_probed": data[0]["not_probed"],
       "cohorts": len(assigned),
       "dependency_map": {k: sorted(v) for k, v in sorted(depmap.items())},
       "determinism": det, "traces": {}}

for t in (preserving, promoted):
    state, outcome = resolve_state_pair(t)          # raises on an illegal pair
    out["traces"][t.promotion_status.value] = {
        "schedule_state": state.kind.value,
        "reason": state.reason.value if state.reason else None,
        "evidence_outcome": outcome.value,
        "cohorts": len(t.selected_eligible_cohorts),
        "strategies": list(t.resolved_strategies),
        "records": len(t.records),
        "valid_records": sum(1 for r in t.records if r.valid),
    }

events = derive_evidence_events((preserving, promoted))
out["evidence_events"] = len(events)
out["events_licensing_proven"] = sum(1 for e in events if e.licenses_proven)
out["silent_cohorts"] = sorted(set(assigned) - set(depmap))

# The output path is overridable so that a SECOND run -- over a second set of
# shards, e.g. to check reproducibility -- cannot overwrite the banked result
# it exists to be compared against. Default unchanged (R134/B9).
OUT_PATH = pathlib.Path(os.environ.get(
    "LEAKAUDIT_B8_MERGE_OUT", str(EV / "probe_b_merged.json")))
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUT_PATH.write_text(json.dumps(out, indent=1), encoding="utf-8")

print("wrote %s" % OUT_PATH)
print("MERGED %d shards, %d cohorts, baseline %s" % (len(data), len(assigned),
                                                     baseline_sha[:16]))
for k, v in out["traces"].items():
    print("  %-11s %s x %s  records=%d valid=%d  cohorts=%d"
          % (k, v["schedule_state"], v["evidence_outcome"], v["records"],
             v["valid_records"], v["cohorts"]))
print("  evidence events: %d (%d license PROVEN)"
      % (out["evidence_events"], out["events_licensing_proven"]))
print("  cohorts with findings: %d | silent: %d"
      % (len(depmap), len(out["silent_cohorts"])))
