"""Score PREREG.md section 6.2 criteria 1 and 2 on L3.1. R190 §2.

IT LIVES OUTSIDE THE PACKAGE, ON PURPOSE. SC-7(b)/(c) withhold the declared
ground-truth map from the tool: a detector graded against a key it had seen
measures retrieval, not discrimination. The probe receives the pipeline for one
side and the declared availability model, and nothing else. The map, the
manifest and the required list are read HERE, after the probe has returned.

WHICH DETECTOR. L3.1, the availability probe. Established R188 §3.1 and accepted
R189 §1: the criteria adjudicate `runtime findings`; section 3.1 defines a
runtime finding by promotion status and excludes the review rows that are not
runtime detectors; section 7.1 assigns both runtime metric rows to L2a and L3.1
and to no others; section 4.1 says of those two that they emit at a tier derived
from promotion status alone, which is the property criterion 1 turns on. The
column probe is none of the eleven rows and is not scored here.

WHICH SIDE. Both criteria are scored on the CONTAMINATED side, and the reason is
per instrument-month rather than general. Criterion 2 names that side in its own
text. Criterion 1 is scored where the map declares the violations, which SC-5(b)
requires -- "on the side, in the cells, and on the ground the map declares" --
and for zc 2025-01 that is the contaminated side: section 13(c) has every one of
the 48 instrument-months strict-positive there, while section 13(b)'s eighteen
non-zero corrected instrument-months do not include this one. The corrected side
is RUN and REPORTED as a control, and no criterion is scored on it.

PRIMARY AND SECONDARY ARE DECIDED HERE, NOT BY THE TOOL. The trace's
`is_secondary` flag is the tool's own claim about itself. PREREG.md line 914
records why that may not decide anything: a classifier the tool controls cannot
be allowed to decide what counts against it. The classification is taken from
the fixture manifest's own column classes -- the ground-truth DAG section 6.2
line 578 puts there -- so a finding on a DESCENDANT column is secondary under
section 7.6 and line 700, and neither satisfies criterion 1 nor enters criterion 2.

THE DENOMINATOR IS NEVER ADJUSTED TO REACHABILITY. N is the length of the
required list and no other quantity is N (SC-4(b)). Units absent from the built
frame are `unsupported` under section 8.2, and section 8.2 forbids displaying
any not-run state in a way mistakable for a pass. They are neither hits nor
misses and they stay in the denominator.

CHECKPOINTS after every side, so an interrupted run leaves usable evidence.
"""
from __future__ import annotations

import csv
import json
import os
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pandas as pd                                              # noqa: E402

from leakaudit import fixture_adapter as fa                       # noqa: E402
from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402
from leakaudit.availability_trace import resolve_all, traces_for   # noqa: E402
from protocol.runtime_reference import derive_evidence_events      # noqa: E402

SYM = os.environ.get("ACC_SYM", "zc")
MONTH = os.environ.get("ACC_MONTH", "2025-01")
STRIDE = int(os.environ.get("ACC_STRIDE", "997"))
MAX_COHORTS = int(os.environ.get("ACC_MAX_COHORTS", "300"))
SEED = int(os.environ.get("ACC_SEED", "20260828"))
SCORED_SIDE = os.environ.get("ACC_SCORED_SIDE", "contaminated")
SIDES = tuple(os.environ.get("ACC_SIDES", "contaminated,corrected").split(","))
OUT = pathlib.Path(os.environ.get(
    "ACC_OUT", str(ROOT / "evidence" / "phase1" / "criteria_12_run.json")))

DECL = ROOT / "AVAILABILITY_DECLARATION.md"
MANIFEST = ROOT / "evidence" / "fixture_spike" / "f3" / "fixture_manifest_DRAFT.json"
MAP = ROOT / "evidence" / "fixture_spike" / "n1" / "declared_map.csv"

# The declared model. Every element is the declaration's, and the two aggregate
# frames are the ones whose rows are wall-clock-second aggregates: their
# declared availability instant is the key plus one second, which is the
# `at_source_timestamp` truth section C names and not the `at_bar_close` role it
# declares an approximation of.
MODEL = AvailabilityModel(aggregate_frames={"magg": "ts_floor", "trades": "ts_event"},
                          decision_column="timestamp")


def log(msg: str) -> None:
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


# ---------------------------------------------------------------------------
# Ground truth, derived from the attested files. HARNESS SIDE ONLY.
# ---------------------------------------------------------------------------

def required_units() -> list[tuple[str, str]]:
    """(column, governing map class) for each unit of criterion 1's denominator.

    Split on the cell delimiter and take the first quoted token from each cell.
    One row's class cell reads "`trades_sell` (= `trades_all` here, section 15)",
    and a whole-row pattern that assumed a bare quoted token dropped it --
    returning ten units for a denominator the declaration states as eleven, with
    nothing to show the difference. The count is checked against the
    declaration's own N, so an under-reading parser fails loudly instead of
    scoring a short denominator.
    """
    text = DECL.read_text(encoding="utf-8").split("\n")
    start = next(i for i, l in enumerate(text) if l.startswith("#### A.6.1"))
    window = text[start:start + 40]

    rows: list[tuple[str, str]] = []
    for line in window:
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or not re.fullmatch(r"\d+", cells[0]):
            continue
        col = re.search(r"`([^`]+)`", cells[1])
        klass = re.search(r"`([^`]+)`", cells[3])
        if col and klass:
            rows.append((col.group(1).strip(), klass.group(1).strip()))

    declared_n = None
    for line in window:
        m = re.search(r"\*\*N = (\d+)", line)
        if m:
            declared_n = int(m.group(1))
            break
    if declared_n is None:
        raise RuntimeError("A.6.1 states no N; the parse cannot check itself")
    if len(rows) != declared_n:
        raise RuntimeError(
            "parsed %d required units from A.6.1 but the declaration states "
            "N = %d. A denominator short by even one unit scores a different "
            "criterion. Parsed: %s" % (len(rows), declared_n, [c for c, _ in rows]))
    return rows


def manifest_columns() -> tuple[dict[str, str], dict[str, list]]:
    d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return ({c["name"]: c["class"] for c in d["columns"]},
            {c["name"]: c.get("parents") or [] for c in d["columns"]})


def map_cells(side: str) -> dict[str, dict]:
    """The declared cells for this side, instrument and month, by class."""
    out: dict[str, dict] = {}
    with MAP.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if (row["side"] == side and row["instrument"] == SYM
                    and row["month"] == MONTH):
                out[row["class"]] = {
                    "strict_count": int(row["strict_count"]),
                    "equal_count": int(row["equal_count"]),
                    "rows": int(row["rows"]),
                    "scored_flag": row["scored_flag"],
                    "boundary": row["boundary"]}
    return out


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------

def run_side(cap, side: str) -> dict:
    log("side %s: building and probing" % side)
    t0 = time.time()
    build = fa.builder_for(cap, side)
    res = run_probe_a(cap.raw, build, MODEL, side=side,
                      cohort_stride=STRIDE, max_cohorts=MAX_COHORTS, seed=SEED)

    # ELIGIBILITY, derived and not assumed: a picked second is eligible iff some
    # aggregate frame carries a row in it. A second with nothing to corrupt
    # scheduled nothing, and a trace claiming otherwise would resolve to
    # INCOMPLETE(crash) -- a dead process reported where the truth is an empty
    # probe surface.
    picked = [c.second for c in res.cohorts]
    pset = set(picked)
    have: set = set()
    for fname, keycol in MODEL.aggregate_frames.items():
        f = cap.frames.get(fname)
        if f is None:
            continue
        k = pd.to_datetime(f[keycol])
        if getattr(k.dt, "tz", None) is not None:
            k = k.dt.tz_convert("UTC").dt.tz_localize(None)
        have |= (set(k.dt.floor("s").unique()) & pset)
    eligible = [s for s in picked if s in have]

    case_id = "fixture_%s_%s_%s" % (side, SYM, MONTH)
    traces = traces_for(res, eligible, case_id=case_id)
    resolved = resolve_all(traces)              # raises on an illegal pair
    events = derive_evidence_events(traces)

    findings = []
    for t in traces:
        for r in t.records:
            if r.finding is None:
                continue
            findings.append({
                "promotion_status": t.promotion_status.value,
                "strategy": r.strategy_id,
                "cohort": r.cohort_id,
                "feature": r.finding.feature,
                "probe_cohort": r.finding.probe_cohort,
                "affected_output_cohort": r.finding.affected_output_cohort,
                "tool_is_secondary_claim": r.finding.is_secondary,
            })
    log("side %s: %.0f s, %d cohort(s) eligible, %d finding record(s), %d event(s)"
        % (side, time.time() - t0, len(eligible), len(findings), len(events)))
    return {
        "case_id": case_id,
        "probe_verdict": res.verdict(),
        "determinism_ok": res.determinism_ok,
        "notes": list(res.notes),
        "n_picked": len(picked),
        "n_eligible": len(eligible),
        "n_ineligible_no_aggregate": len(picked) - len(eligible),
        "resolved": resolved,
        "n_events": len(events),
        "features_with_findings": sorted({f["feature"] for f in findings}),
        "findings": findings,
        "seconds": round(time.time() - t0, 1),
    }


def score(doc: dict, columns_present: dict[str, list[str]]) -> dict:
    """Criteria 1 and 2, from the closed probe output and the declared lists."""
    req = dict(doc["required_units_pairs"])
    classes = doc["_classes"]
    side = SCORED_SIDE
    present = set(columns_present[side])
    cells = doc["declared_map_cells"][side]
    found = {f["feature"] for f in doc["sides"][side]["findings"]}

    def is_secondary(col: str) -> bool:
        # Section 7.6 through the manifest's own DAG, never through the tool's flag.
        return classes.get(col) == "DESCENDANT"

    c1 = []
    for col, klass in sorted(req.items()):
        cell = cells.get(klass)
        if col not in present:
            state, why = "unsupported", (
                "the column is absent from the built frame on the scored side; "
                "section 8.2 -- missing or impossible inputs are unsupported, "
                "and no not-run state is displayed as a pass")
        elif cell is None:
            state, why = "unscoreable_no_cell", (
                "the declared map carries no cell for governing class %r on this "
                "side, instrument and month" % klass)
        elif cell["strict_count"] == 0 and cell["equal_count"] == 0:
            state, why = "no_declared_violation", (
                "the governing cell is zero strict and zero equal, so SC-5(b)'s "
                "'in the cells the map declares' is not met on this side")
        elif col in found and not is_secondary(col):
            state, why = "satisfied", (
                "at least one primary finding attributed to this column, in a "
                "cell the map declares non-zero")
        elif col in found:
            state, why = "secondary_only", (
                "findings exist but the manifest classes this column a "
                "descendant, so section 7.6 makes them secondary and line 700 "
                "says they do not satisfy criterion 1")
        else:
            state, why = "missed", "no finding attributed to this column"
        c1.append({"column": col, "governing_map_class": klass, "state": state,
                   "ground": why,
                   "declared_cell": cell,
                   "manifest_class": classes.get(col),
                   "present_in_built_frame": col in present})

    clean = sorted(c for c, k in classes.items() if k == "CLEAN")
    c2 = []
    for col in clean:
        if col not in present:
            state, why = "unsupported", (
                "the column is absent from the built frame on the contaminated "
                "side; section 8.2, and never displayed as a pass")
        elif col in found:
            state, why = "violated", (
                "a finding names a manifest-clean column on the contaminated "
                "side; criterion 2 admits findings of ANY tier, primary or "
                "secondary")
        else:
            state, why = "clean", "no finding of any tier names this column"
        c2.append({"column": col, "state": state, "ground": why,
                   "present_in_built_frame": col in present})

    unexpected = sorted(found - set(req) - set(clean))
    return {
        "scored_side": side,
        "criterion_1": {
            "denominator_N": len(req),
            "denominator_source": "A.6.1's REQUIRED list; SC-4(b) -- N is the "
                                  "length of that list and no other quantity is N",
            "units": c1,
            "counts": {s: sum(1 for u in c1 if u["state"] == s)
                       for s in sorted({u["state"] for u in c1})},
        },
        "criterion_2": {
            "population": len(clean),
            "units": c2,
            "counts": {s: sum(1 for u in c2 if u["state"] == s)
                       for s in sorted({u["state"] for u in c2})},
        },
        "features_with_findings_not_in_either_declared_list": [
            {"feature": f, "manifest_class": classes.get(f, "NOT_IN_MANIFEST")}
            for f in unexpected],
    }


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    req = required_units()
    classes, parents = manifest_columns()
    clean = sorted(c for c, k in classes.items() if k == "CLEAN")
    desc = sorted(c for c, k in classes.items() if k == "DESCENDANT")
    log("ground truth: %d REQUIRED, %d CLEAN, %d DESCENDANT (harness side only)"
        % (len(req), len(clean), len(desc)))

    doc: dict = {
        "detector": "L3.1 -- the availability probe (leakaudit.availability)",
        "scope": {"instrument": SYM, "month": MONTH, "sides_run": list(SIDES),
                  "scored_side": SCORED_SIDE,
                  "artifact": "A (the f2 rebuild pair)",
                  "stride": STRIDE, "max_cohorts": MAX_COHORTS, "seed": SEED},
        "criteria_scored": [1, 2],
        "criterion_3": "BLOCKED_LABEL_GAP_SEE_DEVIATIONS_D_V30A_28",
        "criterion_4": "BLOCKED_LABEL_GAP_SEE_DEVIATIONS_D_V30A_28",
        "gate_result": "NOT_A_GATE_RESULT_TWO_OF_FOUR_CRITERIA_ONE_INSTRUMENT_MONTH",
        "gate_status_of_repository": {
            "exit": 1,
            "finding": "hash_set_single_source at HISTORY.md",
            "disposition": "known false positive, disclosed at D-V30A-11",
        },
        "required_units_pairs": req,
        "manifest_clean": clean,
        "manifest_descendant": desc,
        "_classes": classes,
        "declared_map_cells": {s: map_cells(s) for s in SIDES},
        "sides": {},
    }

    log("capturing inputs once")
    t0 = time.time()
    cap = fa.read_inputs(SYM, MONTH)
    doc["capture_seconds"] = round(time.time() - t0, 1)
    doc["raw_frames"] = {k: list(v.shape) for k, v in cap.raw.items()}

    columns_present: dict[str, list[str]] = {}
    for side in SIDES:
        columns_present[side] = list(fa.builder_for(cap, side)(dict(cap.raw)).columns)
        doc["sides"][side] = run_side(cap, side)
        doc["columns_present"] = columns_present
        OUT.write_text(json.dumps(doc, indent=1, sort_keys=True, default=str),
                       encoding="utf-8", newline="")
        log("checkpointed after side %s -> %s" % (side, OUT.name))

    doc["scoring"] = score(doc, columns_present)
    doc.pop("_classes")
    OUT.write_text(json.dumps(doc, indent=1, sort_keys=True, default=str),
                   encoding="utf-8", newline="")
    log("done -> %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
