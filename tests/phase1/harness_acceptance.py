"""The §6.2 acceptance harness. Runs the probe, then scores criteria 1-4.

IT LIVES OUTSIDE THE PACKAGE, ON PURPOSE. PREREG.md SC-7(b)/(c) withhold the
declared ground-truth map from the tool: a detector graded against a key it had
seen measures retrieval, not discrimination. The probe runs first and its output
is closed before any label is read. `leakaudit` is never handed a label, a map,
or a manifest -- the executable statement of that is tests/phase1/sc7c.py.

WHAT IT SCORES ON. Criteria 1-4 are evaluated on Artifact A, the f2 rebuild pair
(`fixture_corrected` = the Phase 5 builder plus the universal lag;
`fixture_contaminated` = that builder unchanged). The declaration's own §0.1/§0.2
allocation sentences say the reverse, and I1_ALLOCATION_TABLE.md (R64), carried
into K2_ARTIFACT_B_ALLOCATION.md, determines both false for all four on the
ground that a criterion about columns receiving findings cannot be a statement
about an artifact with no columns. K2 records the criteria's registered text as
unambiguous and the allocation sentences as disclosure-class.

WHICH FIELD THE CRITERIA READ. Criterion 1 requires attribution "to the labelled
source", and the labelled sources are the manifest's columns, so the criteria are
scored from a finding's `feature` -- the output column that moved.
`affected_output_cohort` is not an input to any of the four; it was repaired this
round (it had carried the probed input) and its content is reported but not
scored on.

GROUND TRUTH IS DERIVED, NEVER TRANSCRIBED. The REQUIRED list and each unit's
governing map class are parsed from the declaration's §A.6.1 table; the column
classes are read from the fixture manifest. A hand-copied list is a second source
that will eventually disagree with the first.

CHECKPOINTS after every cohort, so an interrupted run leaves usable evidence
rather than nothing.
"""
from __future__ import annotations

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

import pandas as pd                                          # noqa: E402

from leakaudit import fixture_adapter as fa                   # noqa: E402
from leakaudit.probe import output_column_of, probe_columns    # noqa: E402

SYM = os.environ.get("ACC_SYM", "zc")
MONTH = os.environ.get("ACC_MONTH", "2025-01")
SIDES = tuple(os.environ.get("ACC_SIDES", "corrected,contaminated").split(","))
OUT = pathlib.Path(os.environ.get(
    "ACC_OUT", str(ROOT / "evidence" / "phase1" / "acceptance_run.json")))

DECL = ROOT / "AVAILABILITY_DECLARATION.md"
MANIFEST = ROOT / "evidence" / "fixture_spike" / "f3" / "fixture_manifest_DRAFT.json"
MAP = ROOT / "evidence" / "fixture_spike" / "n1" / "declared_map.csv"


def log(msg: str) -> None:
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


# ---------------------------------------------------------------------------
# Ground truth, derived from the attested files. Harness side only.
# ---------------------------------------------------------------------------

def required_units() -> list[tuple[str, str]]:
    """(column, governing map class) for each unit of the criterion-1
    denominator, parsed from the declaration's A.6.1 table.

    Split on the cell delimiter and take the first quoted token from each cell,
    rather than matching the row as one pattern. One row's class cell reads
    "`trades_sell` (= `trades_all` here, §15)", and a whole-row pattern that
    assumed a bare quoted token dropped it -- returning ten units for a
    denominator the declaration states as eleven, with nothing to show the
    difference. The count is checked against the declaration's own N below, so a
    parser that under-reads fails loudly instead of scoring a short denominator.
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
            "criterion. Parsed: %s"
            % (len(rows), declared_n, [c for c, _ in rows]))
    return rows


def manifest_classes() -> dict[str, str]:
    d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {c["name"]: c["class"] for c in d["columns"]}


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------

def findings_of(result) -> list[dict]:
    out = []
    for status, trace in (("preserving", result.preserving),
                          ("promoted", result.promoted)):
        for r in trace.records:
            if r.finding is None:
                continue
            out.append({
                "promotion_status": status,
                "strategy": r.strategy_id,
                "probe_cohort": r.finding.probe_cohort,
                "feature": r.finding.feature,
                "affected_output_cohort": r.finding.affected_output_cohort,
                "is_secondary": r.finding.is_secondary,
            })
    return out


def run_side(side: str) -> dict:
    log("side %s: capturing inputs" % side)
    cap = fa.read_inputs(SYM, MONTH)
    build = fa.builder_for(cap, side)
    log("side %s: probing %d source columns"
        % (side, sum(len(f.columns) for f in cap.raw.values())))
    t0 = time.time()
    result = probe_columns(cap.raw, build, case_id="fixture_%s_%s_%s"
                           % (side, SYM, MONTH))
    log("side %s: probe finished in %.0f s" % (side, time.time() - t0))
    return {
        "case_id": "fixture_%s_%s_%s" % (side, SYM, MONTH),
        "cohorts": [c for c in result.preserving.selected_eligible_cohorts],
        "findings": findings_of(result),
        "dependency_map": {k: list(v) for k, v in result.dependency_map.items()},
    }


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    req = required_units()
    classes = manifest_classes()
    clean = sorted(c for c, k in classes.items() if k == "CLEAN")
    log("ground truth: %d REQUIRED units, %d CLEAN columns" % (len(req), len(clean)))

    doc: dict = {
        "scope": {"instrument": SYM, "month": MONTH, "sides": list(SIDES),
                  "artifact": "A (the f2 rebuild pair)"},
        # Carried as data, not as prose, so a reader of the JSON alone cannot
        # mistake any of it for a satisfied gate.
        "criteria_scored": [1, 2, 3],
        "criterion_3_scope": "THIS_INSTRUMENT_MONTH_ONLY_20_OF_960_CELLS",
        "criterion_4": "UNSCOREABLE_NO_IDENTITY_CONTROL_IMPLEMENTED",
        "gate_result": "NOT_A_GATE_RESULT_PARTIAL_SCOPE",
        "gate_status_of_repository": {
            "exit": 1,
            "finding": "hash_set_single_source at HISTORY.md:236",
            "disposition": "known false positive, disclosed at D-V30A-11; the "
                           "detector fires on prose naming three registered "
                           "paths and carries no digest",
        },
        "required_units": [{"column": c, "governing_map_class": g} for c, g in req],
        "clean_columns": clean,
        "sides": {},
    }
    for side in SIDES:
        doc["sides"][side] = run_side(side)
        OUT.write_text(json.dumps(doc, indent=1, sort_keys=True),
                       encoding="utf-8", newline="")
        log("checkpointed after side %s -> %s" % (side, OUT.name))

    OUT.write_text(json.dumps(doc, indent=1, sort_keys=True),
                   encoding="utf-8", newline="")
    log("done -> %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
