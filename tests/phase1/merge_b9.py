"""Assemble the sharded B9 sweep into FOUR CombinationTraces -- two per detector.

THE MERGE IS WHERE PARALLELISM IS MADE SAFE, not where it is assumed safe. The
same three refusals as B8's merge, for the same reasons, and each is a refusal
rather than a warning:

  1. **Every shard reports the same baseline digest.** Workers that did not
     start from the same bytes did not probe the same pipeline, and pooling
     their findings would produce a map of no single object.
  2. **Every shard is complete.** A partial shard's cohorts are ABSENT, not
     silent, and merging would present the gap as coverage.
  3. **The shards' assignments partition the population** -- every cohort once,
     none missing, none twice. A dropped cohort reads downstream as
     `observed_silence`, which is a finding-shaped absence.

ONE FURTHER CHECK THIS MERGE MAKES AND B8's COULD NOT: `nullread`'s two
combinations must partition the cohorts. That is a property of the detector's
configuration, and a property nothing checks is one that quietly stops holding.

Traces are handed to the reducers UNCHANGED. If a reducer rejects one, the
trace is wrong, not the reducer.
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
    "LEAKAUDIT_B9_SHARD_DIR", str(pathlib.Path.home() / ".leakaudit_b9")))
shards = sorted(SHARD_DIR.glob("b9_shard_*_of_*.json"))
if not shards:
    sys.exit("HALT: no shard files under %s" % SHARD_DIR)

data = [json.loads(p.read_text(encoding="utf-8")) for p in shards]

fatal = [d.get("shard") for d in data if d.get("fatal")]
if fatal:
    sys.exit("HALT: shard(s) %s hit the determinism guard: %s"
             % (fatal, [d.get("fatal") for d in data if d.get("fatal")]))

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
STATUS = {"preserving": PromotionStatus.PRESERVING,
          "promoted": PromotionStatus.PROMOTED}

detector_ids = [x["detector"] for x in data[0]["detectors"]]
out = {"case": case, "baseline_sha256": baseline_sha, "shards": len(data),
       "threads_pinned": 1, "cohorts": len(assigned),
       "not_probed": data[0]["not_probed"],
       "domains": data[0]["domains"], "detectors": {}}

for det_id in detector_ids:
    per = [next(x for x in d["detectors"] if x["detector"] == det_id) for d in data]

    recs = {"preserving": [], "promoted": []}
    cohorts = {"preserving": [], "promoted": []}
    strategies = {"preserving": (), "promoted": ()}
    depmap: dict[str, list[str]] = {}

    for block in per:
        for k in ("preserving", "promoted"):
            cohorts[k].extend(block["cohorts"].get(k, []))
            got = tuple(block.get("strategies", {}).get(k, ()))
            if got:
                if strategies[k] and strategies[k] != got:
                    sys.exit("HALT: %s/%s -- shards resolved different strategy "
                             "sets %s vs %s. They did not run the same detector."
                             % (det_id, k, strategies[k], got))
                strategies[k] = got
        for c, feats in block["dependency_map"].items():
            depmap.setdefault(c, []).extend(feats)
        for r in block["records"]:
            recs[r["promotion"]].append(ExecutionRecord(
                detector_id=det_id, case_id=case, strategy_id=r["strategy"],
                promotion_status=STATUS[r["promotion"]], cohort_id=r["cohort"],
                attempted=r["attempted"], valid=r["valid"],
                finding=(FindingRecord(r["feature"], r["cohort"], r["cohort"])
                         if r.get("feature") else None),
                failure_reason=(REASONS[r["failure_reason"]]
                                if r.get("failure_reason") else None)))

    traces = []
    for k in ("preserving", "promoted"):
        cs = tuple(sorted(set(cohorts[k])))
        traces.append(CombinationTrace(
            detector_id=det_id, case_id=case, promotion_status=STATUS[k],
            run_context=RunContext.FIXTURE,
            resolved_strategies=strategies[k] if cs else (),
            selected_eligible_cohorts=cs,
            required_inputs_available=True, terminal_decision_occurred=False,
            records=tuple(recs[k])))

    block = {"traces": {}, "cohorts_with_findings": len(depmap),
             "dependency_map": {k: sorted(set(v)) for k, v in sorted(depmap.items())},
             "silent_cohorts": sorted(set(assigned) - set(depmap))}
    for t in traces:
        state, outcome = resolve_state_pair(t)      # raises on an illegal pair
        block["traces"][t.promotion_status.value] = {
            "schedule_state": state.kind.value,
            "reason": state.reason.value if state.reason else None,
            "evidence_outcome": outcome.value,
            "cohorts": len(t.selected_eligible_cohorts),
            "strategies": list(t.resolved_strategies),
            "records": len(t.records),
            "valid_records": sum(1 for r in t.records if r.valid),
        }
    events = derive_evidence_events(tuple(traces))
    block["evidence_events"] = len(events)
    block["events_licensing_proven"] = sum(1 for e in events if e.licenses_proven)

    # ---- nullread's partition claim, CHECKED --------------------------------
    if det_id == "nullread":
        pres = set(traces[0].selected_eligible_cohorts)
        prom = set(traces[1].selected_eligible_cohorts)
        if pres & prom:
            sys.exit("HALT: nullread put %s in BOTH combinations" % sorted(pres & prom))
        if pres | prom != set(assigned):
            sys.exit("HALT: nullread covers %d of %d cohorts; uncovered: %s"
                     % (len(pres | prom), len(assigned),
                        sorted(set(assigned) - pres - prom)))
        block["partition"] = {"preserving": len(pres), "promoted": len(prom),
                              "total": len(assigned), "holds": True}

    out["detectors"][det_id] = block

(EV / "b9_merged.json").write_text(json.dumps(out, indent=1), encoding="utf-8")

print("MERGED %d shards, %d cohorts, baseline %s"
      % (len(data), len(assigned), baseline_sha[:16]))
for det_id, block in out["detectors"].items():
    print("  %s" % det_id)
    for k, v in block["traces"].items():
        print("    %-11s %s%s x %-17s records=%3d valid=%3d cohorts=%2d"
              % (k, v["schedule_state"],
                 "(%s)" % v["reason"] if v["reason"] else "",
                 v["evidence_outcome"], v["records"], v["valid_records"],
                 v["cohorts"]))
    print("    evidence events: %d (%d license PROVEN) | fired %d, silent %d"
          % (block["evidence_events"], block["events_licensing_proven"],
             block["cohorts_with_findings"], len(block["silent_cohorts"])))
    if "partition" in block:
        print("    partition: %d + %d = %d, holds"
              % (block["partition"]["preserving"], block["partition"]["promoted"],
                 block["partition"]["total"]))
