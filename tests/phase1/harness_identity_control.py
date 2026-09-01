"""Criterion 4 -- the identity control on L3.1, across the declared population. R195.

WHAT IS SCORED. "Silent under the identity control on both." Section 6.11's
control 2 -- replace unavailable cells with an exact copy of themselves; any
delta is measurement artifact -- and SC-5(f)'s declared sentinel route. Neither
reads the pair-keyed labels the metric family consumes, and neither reads the
declared map, so this criterion is not blocked by the correspondence gap.

F = 1, AND THAT IS FIXED BY THE STRATEGY SET RATHER THAN THE POPULATION. The
number of execution frames is one original plus one per promoted alignment
family. This detector's perturbation is dtype-preserving by construction, so no
promoting strategy resolves and there are no promoted families. Section 6.11's
"once per alignment family" therefore imposes ONE identity control per execution
frame per audit, and here that is one. **A coverage fact follows and is recorded
rather than repaired: the promoted-family path is unexercised by this detector.**

THE AUDIT COUNT IS NOT SETTLED BY THE REGISTRATION. Criterion 4's text fixes the
side axis -- both -- and says nothing about the instrument-month axis. The full
population is run, on the ground of COMPARABILITY: the four criteria then share
one population, and no later sentence of the form "three of four criteria
scored" quotes three different ones. That is a choice, it is not made on cost or
on safety, and it can be narrowed.

TWO LIMBS, AND ONLY THE FIRST IS THE CRITERION. Limb (a), the registered one:
did the OUTPUT move. Limb (b), input invariance, is beyond the registered text,
is reported separately, and is NEVER quoted as satisfying criterion 4. It exists
because a builder can absorb an input-side promotion, so limb (a) can pass while
the write-back has changed the frame the promotion status is computed from.

A SHAPE OR COLUMN-SET CHANGE IS A COMPATIBILITY FAILURE, NOT A FINDING. Section
6.11's third control owns shape and index and says every comparison past a shape
change is meaningless, including one that looks clean, so the result is
discarded; section 6.11's head says control failures are recorded per the
coverage scheme and never as findings; and section 6.6 puts `compatibility`
ahead of `control_artifact` in precedence. It is NOT a pass: section 8.2 forbids
displaying any not-run state as one, so criterion 4 has no answer on that side
and that is reported as itself.

THE COST MODEL IS 48 MEASURED POINTS, NOT ONE. D-V30A-37 and TB-10 record what a
one-point model does: it interpolates its own fitting point to within four per
cent and misses the population by 2.35x, because at one point every term is
confounded and it cannot see which term it omitted. This harness predicts each
instrument-month from THAT instrument-month's own measured probe cost in the
committed population run, scaled by a ratio of two measured terms. The halt sits
on that per-instrument-month prediction.

CHECKPOINTS AFTER EVERY INSTRUMENT-MONTH, and a failure in one does not lose the
others.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import sys
import time
import traceback

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import fixture_adapter as fa                        # noqa: E402
from leakaudit.availability import AvailabilityModel                # noqa: E402
from leakaudit.identity_control import (                            # noqa: E402
    CONTROL_ID, run_identity_control, sentinel_columns,
    sentinel_false_positives)

INSTRUMENTS = tuple(os.environ.get(
    "ACC_INSTRUMENTS", "cl,es,gc,he,le,nq,zc,zs").split(","))
MONTHS = tuple(os.environ.get(
    "ACC_MONTHS", "2025-01,2025-08,2025-09,2025-10,2025-11,2025-12").split(","))
SIDES = ("contaminated", "corrected")
STRIDE = int(os.environ.get("ACC_STRIDE", "997"))
MAX_COHORTS = int(os.environ.get("ACC_MAX_COHORTS", "300"))
OUT = pathlib.Path(os.environ.get(
    "ACC_OUT", str(ROOT / "evidence" / "phase1" / "criterion_4_population.json")))

DECL = ROOT / "AVAILABILITY_DECLARATION.md"
PRIOR_RUN = ROOT / "evidence" / "phase1" / "criteria_12_population.json"

MODEL = AvailabilityModel(aggregate_frames={"magg": "ts_floor", "trades": "ts_event"},
                          decision_column="timestamp")

# A probe side is 3 builds plus one full compare; a control side is 2 builds
# plus one compare. At zc 2025-01 a build measured 34 s and a probe side 176.8 s,
# so the compare term is about 75 s and the ratio is 143/177.
CONTROL_TO_PROBE_RATIO = 0.81
COST_HALT_MULTIPLE = 10.0

# SC-5(f)'s declared sentinel, from A.9. THE ENUMERATION IS THE DECLARATION'S AND
# IS NEVER EXTENDED IN RESPONSE TO WHAT FIRES. The two literals below are checked
# against the declaration's own text at startup, so a sentinel that changed there
# fails loudly here rather than being scored stale.
SENTINEL_LITERALS = ("4294967291", "2^32")


def log(msg: str) -> None:
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def check_sentinel_declaration() -> str:
    text = DECL.read_text(encoding="utf-8")
    start = text.index("### A.9")
    end = text.index("### A.10", start)
    body = text[start:end]
    missing = [s for s in SENTINEL_LITERALS if s not in body]
    if missing:
        raise RuntimeError(
            "A.9 no longer carries %s. The sentinel signature this harness "
            "scores against is the declaration's, and a stale copy of it would "
            "score a sentinel the declaration does not declare." % missing)
    return body.strip().split("\n")[0]


def prior_probe_seconds() -> dict[tuple[str, str], float]:
    """Each instrument-month's own measured probe cost, from the committed run."""
    d = json.loads(PRIOR_RUN.read_text(encoding="utf-8"))
    return {(i["instrument"], i["month"]): i["probe_seconds"]
            for i in d["instrument_months"] if i.get("probe_seconds")}


def frame_signature(cap) -> dict[str, list]:
    """The dtype signature of the frames the write-back touches."""
    out = {}
    for name in sorted(MODEL.aggregate_frames):
        f = cap.raw.get(name)
        out[name] = None if f is None else [
            [c, str(f[c].dtype)] for c in f.columns]
    return out


def run_instrument_month(cap, sym: str, month: str, predicted: float) -> dict:
    im: dict = {"instrument": sym, "month": month, "sides": {},
                "predicted_control_seconds": round(predicted, 1)}
    t_ctl = time.time()
    for side in SIDES:
        t0 = time.time()
        build = fa.builder_for(cap, side)
        res = run_identity_control(cap.raw, build, MODEL, side=side,
                                   cohort_stride=STRIDE, max_cohorts=MAX_COHORTS)
        im["sides"][side] = {
            "sentinel_columns": dict(res.base_sentinel_columns),
            "verdict": res.verdict(),
            "scoreable": res.scoreable,
            "determinism_ok": res.determinism_ok,
            "compatibility_ok": res.compatibility_ok,
            "output_identical": res.output_identical,
            "moved_columns": list(res.moved_columns),
            "n_cohorts": res.n_cohorts,
            "n_base_columns": len(res.base_columns),
            "notes": list(res.notes),
            # LIMB (b): BEYOND THE REGISTERED TEXT, reported apart.
            "limb_b_input_invariant": res.input_invariant,
            "limb_b_columns_checked": len(res.input_checks),
            "limb_b_failures": [
                {"frame": c.frame, "column": c.column, "why": c.why()}
                for c in res.input_checks if not c.invariant],
            "seconds": round(time.time() - t0, 1),
        }
        log("  %s %s %-13s %-28s limb_b_invariant=%s  %.0f s"
            % (sym, month, side, res.verdict(), res.input_invariant,
               im["sides"][side]["seconds"]))
    im["control_seconds"] = round(time.time() - t_ctl, 1)
    return im


def score(im: dict) -> dict:
    """Criterion 4: silent under the identity control ON BOTH."""
    sides = im["sides"]
    sentinels = {s: sides[s]["sentinel_columns"] for s in sides}
    verdicts = {s: sides[s]["verdict"] for s in sides}
    if not all(sides[s]["scoreable"] for s in sides):
        state = "not_scored"
        why = ("at least one side is in a not-run state (%s); section 8.2 -- no "
               "not-run state is displayed in a way mistakable for a pass"
               % ", ".join("%s=%s" % (s, v) for s, v in sorted(verdicts.items())))
    elif all(v == "silent" for v in verdicts.values()):
        state = "satisfied"
        why = "the output did not move under the identity write, on either side"
    else:
        state = "failed"
        why = ("the output moved under the identity write on %s; any delta is "
               "measurement artifact"
               % ", ".join(s for s, v in sorted(verdicts.items())
                           if v != "silent"))
    a, b = sentinels.get("contaminated") or {}, sentinels.get("corrected") or {}
    moved = sorted(set(sides["contaminated"]["moved_columns"])
                   | set(sides["corrected"]["moved_columns"]))
    return {"criterion_4": state, "ground": why,
            "sentinel_columns_contaminated": a,
            "sentinel_columns_corrected": b,
            "sentinel_false_positives": sentinel_false_positives(moved, a, b)}


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sentinel_heading = check_sentinel_declaration()
    prior = prior_probe_seconds()
    population = [(s, m) for s in INSTRUMENTS for m in MONTHS]
    missing = [k for k in population if k not in prior]
    if missing:
        raise RuntimeError("no measured prior cost for %s; the halt would have "
                           "nothing to sit on" % missing)
    log("population: %d instrument-month(s); sentinel heading verified: %s"
        % (len(population), sentinel_heading[:60]))

    doc: dict = {
        "detector": "L3.1 -- the availability probe, under section 6.11 control 2",
        "control_id": CONTROL_ID,
        "criteria_scored": [4],
        "criteria_1_2": "SCORED SEPARATELY at criteria_12_population.json",
        "criterion_3": "BLOCKED_LABEL_GAP_SEE_DEVIATIONS_D_V30A_28",
        "gate_result": "NOT_A_GATE_RESULT_ONE_CRITERION",
        "alignment_families": {
            "F": 1,
            "promoted_families": 0,
            "ground": "the perturbation is dtype-preserving by construction, so "
                      "no promoting strategy resolves; F is one original frame "
                      "plus one per promoted family",
            "coverage_fact": "the promoted-family path is UNEXERCISED by this "
                             "detector. Recorded, not repaired."},
        "audit_population_ground":
            "the registration does not settle how many audits criterion 4 is "
            "evaluated over; the full population is run for COMPARABILITY with "
            "criteria 1 and 2, not for cost and not for safety",
        "limb_b_note":
            "input invariance is BEYOND the registered text, reported apart, "
            "and never quoted as satisfying criterion 4",
        "cost_model": {"basis": "48 measured points -- each instrument-month's "
                                "own probe cost in the committed population run",
                       "control_to_probe_ratio": CONTROL_TO_PROBE_RATIO,
                       "halt_multiple": COST_HALT_MULTIPLE},
        "instrument_months": [],
    }

    t_all = time.time()
    signatures: dict[str, list] = {}
    for sym, month in population:
        t0 = time.time()
        im: dict = {"instrument": sym, "month": month, "run_status": "ok"}
        try:
            log("%s %s: capturing" % (sym, month))
            cap = fa.read_inputs(sym, month)
            im["capture_seconds"] = round(time.time() - t0, 1)
            sig = frame_signature(cap)
            im["frame_signature"] = sig
            signatures[json.dumps(sig, sort_keys=True)] = signatures.get(
                json.dumps(sig, sort_keys=True), []) + ["%s %s" % (sym, month)]
            predicted = CONTROL_TO_PROBE_RATIO * prior[(sym, month)]
            got = run_instrument_month(cap, sym, month, predicted)
            im.update(got)
            im["scoring"] = score(im)
        except BaseException as exc:                        # noqa: BLE001
            im["run_status"] = "could_not_run"
            im["failure"] = "%s: %s" % (type(exc).__name__, exc)
            im["traceback"] = traceback.format_exc()
            log("  %s %s COULD NOT RUN: %s" % (sym, month, im["failure"]))
        im["seconds"] = round(time.time() - t0, 1)
        pred, actual = im.get("predicted_control_seconds"), im.get("control_seconds")
        if pred and actual and actual > COST_HALT_MULTIPLE * pred:
            im["cost_halt"] = ("the control phase took %.0f s, which exceeds %gx "
                               "the predicted %.0f s" % (actual, COST_HALT_MULTIPLE, pred))
            doc["instrument_months"].append(im)
            doc["halted"] = "%s %s: %s" % (sym, month, im["cost_halt"])
            OUT.write_text(json.dumps(doc, indent=1, sort_keys=True, default=str),
                           encoding="utf-8", newline="")
            log("HALT: %s" % doc["halted"])
            return 2
        doc["instrument_months"].append(im)
        doc["elapsed_seconds"] = round(time.time() - t_all, 1)
        doc["frame_signature_groups"] = {
            "n_distinct": len(signatures),
            "groups": {k[:24] + "...": v for k, v in signatures.items()}}
        OUT.write_text(json.dumps(doc, indent=1, sort_keys=True, default=str),
                       encoding="utf-8", newline="")
        log("  checkpointed after %s %s (%.0f s; %.0f s total)"
            % (sym, month, im["seconds"], doc["elapsed_seconds"]))

    doc["elapsed_seconds"] = round(time.time() - t_all, 1)
    OUT.write_text(json.dumps(doc, indent=1, sort_keys=True, default=str),
                   encoding="utf-8", newline="")
    log("done -> %s (%.0f s)" % (OUT, doc["elapsed_seconds"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
