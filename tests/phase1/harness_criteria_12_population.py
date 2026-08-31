"""Score section 6.2 criteria 1 and 2 on L3.1 across the declared population. R192.

IT LIVES OUTSIDE THE PACKAGE, ON PURPOSE. SC-7(b)/(c) withhold the declared
ground-truth map from the tool: a detector graded against a key it had seen
measures retrieval, not discrimination. The probe receives the pipeline for one
side and the declared availability model, and nothing else. The map, the manifest
and the required list are read HERE.

WHAT IS DIFFERENT FROM THE zc 2025-01 HARNESS, and each difference is a decision
rather than a tidy-up:

  THE VIOLATION PREDICATE IS `strict_count > 0`, NOT "strict or equal".
  `ties` is declared `available`, so the comparator reads `a(j,c) <= d(i)` and an
  event at exactly the decision instant is AVAILABLE. An equal count is therefore
  a violation only under the branch the declaration did not take. It changes
  nothing at zc 2025-01, where the contaminated cells carry 89,568 strict; it
  changes two cells of this population -- es 2025-10 and es 2025-11 corrected,
  which carry 0 strict and 1 equal and would otherwise have been read as
  declaring a violation they do not declare.

  CRITERION 1 IS SCORED PER (SIDE, INSTRUMENT-MONTH), wherever a governing cell
  carries strict > 0. SC-5(b) satisfies a required entry only by a finding "on
  the side, in the cells, and on the ground the map declares", and the map is
  stated side-relatively (SC-3(d)). At zc 2025-01 only the contaminated side
  qualified, so the distinction was invisible; across the population 48
  contaminated and 18 corrected instrument-months qualify. No single aggregate
  over those contexts is published as "the" criterion-1 result: the registration
  defines the criterion over units, not over instrument-months, and inventing an
  aggregation rule is not this harness's to do.

  CRITERION 2 REMAINS ON THE CONTAMINATED SIDE, which its own text names, in all
  48. Its reach does NOT grow with the population: of the four manifest-clean
  columns, one is present in the built frame, so the criterion has one reachable
  unit per instrument-month however many are run.

  THE vwap_distance GROUND CONDITION IS CHECKED PER INSTRUMENT-MONTH, never
  inherited. R192 §4. The column is required on its forward-join ground and legal
  on its same-row mid read; a finding on the legal ground would not satisfy the
  entry (SC-5(b)). What makes it scoreable is that the probe's perturbation
  domain cannot reach the legal ground -- the domain is the declared aggregate
  frames and `mid_price` is a snapshot column. That is a property of a
  configuration, so it is asserted against THIS instrument-month's frames every
  time, and where it fails the column is excluded from the numerator with its
  ground recorded rather than silently credited.

  COLUMNS COME FROM THE PROBE'S OWN BASELINE (`base_columns`), not from a second
  build. Cheaper, and it removes the possibility of the column set disagreeing
  with the frame the findings came from.

  FINDINGS ARE SUMMARISED, NOT ENUMERATED. One instrument-month produced 5,220
  finding records; ninety-six sides of them would be a file nobody commits. What
  the criteria read is whether a feature received at least one finding, so the
  per-side record is the feature-to-count map plus the totals. That is a
  summary and is labelled one.

CHECKPOINTS AFTER EVERY INSTRUMENT-MONTH, and a failure in one does not lose the
others: it is recorded as `could_not_run` with its exception, which section 8.2
accounts separately from findings and never displays as a pass.
"""
from __future__ import annotations

import csv
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

import pandas as pd                                              # noqa: E402

from leakaudit import fixture_adapter as fa                       # noqa: E402
from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402
from leakaudit.availability_trace import resolve_all, traces_for   # noqa: E402
from protocol.runtime_reference import derive_evidence_events      # noqa: E402

INSTRUMENTS = tuple(os.environ.get(
    "ACC_INSTRUMENTS", "cl,es,gc,he,le,nq,zc,zs").split(","))
MONTHS = tuple(os.environ.get(
    "ACC_MONTHS", "2025-01,2025-08,2025-09,2025-10,2025-11,2025-12").split(","))
SIDES = ("contaminated", "corrected")
STRIDE = int(os.environ.get("ACC_STRIDE", "997"))
MAX_COHORTS = int(os.environ.get("ACC_MAX_COHORTS", "300"))
SEED = int(os.environ.get("ACC_SEED", "20260828"))
OUT = pathlib.Path(os.environ.get(
    "ACC_OUT", str(ROOT / "evidence" / "phase1" / "criteria_12_population.json")))

DECL = ROOT / "AVAILABILITY_DECLARATION.md"
MANIFEST = ROOT / "evidence" / "fixture_spike" / "f3" / "fixture_manifest_DRAFT.json"
MAP = ROOT / "evidence" / "fixture_spike" / "n1" / "declared_map.csv"

MODEL = AvailabilityModel(aggregate_frames={"magg": "ts_floor", "trades": "ts_event"},
                          decision_column="timestamp")

# The dual-ground column and the frame its LEGAL ground lives in. Section C.5 and
# section C.3: the same-row `mid[t]` read is availability-legal at the boundary;
# the forward-join `vwap` term is the violating ground.
DUAL_GROUND_COLUMN = "vwap_distance"
LEGAL_GROUND_SOURCE = ("snap", "mid_price")

# THE COST MODEL, and it is an ESTIMATE with ONE measured point behind it.
# zc 2025-01 cost 444 s: a 34.8 s capture, and 409 s of builds and fingerprinting
# over 1.262M snapshot rows, of which about 68 s were the two redundant column
# builds this harness no longer does. 341 s over 1.262M rows is the coefficient
# below. It is charged only on the term it was measured on; the capture is
# measured rather than predicted, for the reason at `predicted_probe_seconds`.
SEC_PER_M_SNAP_ROWS = 270.0
COST_HALT_MULTIPLE = 10.0


def log(msg: str) -> None:
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


# ---------------------------------------------------------------------------
# Ground truth, derived from the attested files. HARNESS SIDE ONLY.
# ---------------------------------------------------------------------------

def required_units() -> list[tuple[str, str]]:
    """(column, governing map class) for each unit of criterion 1's denominator.

    The parse checks itself against the declaration's own stated N: a first
    version returned ten units for a denominator of eleven, having dropped the
    row whose class cell carries a parenthetical, and a denominator short by one
    scores a different criterion.
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
            "N = %d. Parsed: %s" % (len(rows), declared_n, [c for c, _ in rows]))
    return rows


def manifest_columns() -> dict[str, str]:
    d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {c["name"]: c["class"] for c in d["columns"]}


def _int(x):
    x = (x or "").strip()
    return int(x) if x else None


def load_map() -> dict[tuple[str, str, str, str], dict]:
    out = {}
    with MAP.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            out[(r["side"], r["instrument"], r["month"], r["class"])] = {
                "strict_count": _int(r["strict_count"]),
                "equal_count": _int(r["equal_count"]),
                "rows": _int(r["rows"]),
                "scored_flag": r["scored_flag"],
                "boundary": r["boundary"]}
    return out


def declares_violation(cell) -> bool:
    """`ties` is declared `available`, so only a STRICT count is a violation."""
    return bool(cell) and (cell.get("strict_count") or 0) > 0


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------

def probe_side(cap, sym: str, month: str, side: str) -> dict:
    t0 = time.time()
    build = fa.builder_for(cap, side)
    res = run_probe_a(cap.raw, build, MODEL, side=side,
                      cohort_stride=STRIDE, max_cohorts=MAX_COHORTS, seed=SEED)

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

    case_id = "fixture_%s_%s_%s" % (side, sym, month)
    traces = traces_for(res, eligible, case_id=case_id)
    resolved = resolve_all(traces)
    events = derive_evidence_events(traces)

    counts: dict[str, int] = {}
    n_records = 0
    for t in traces:
        for r in t.records:
            if r.finding is None:
                continue
            n_records += 1
            counts[r.finding.feature] = counts.get(r.finding.feature, 0) + 1

    return {
        "case_id": case_id,
        "probe_verdict": res.verdict(),
        "determinism_ok": res.determinism_ok,
        "notes": list(res.notes),
        "n_picked": len(picked),
        "n_eligible": len(eligible),
        "n_ineligible_no_aggregate": len(picked) - len(eligible),
        "resolved": resolved,
        "n_finding_records": n_records,
        "n_events": len(events),
        # A SUMMARY, LABELLED ONE. What the criteria read is whether a feature
        # received at least one finding; the per-record list would be a file
        # nobody commits.
        "feature_finding_counts": dict(sorted(counts.items())),
        "features_with_findings": sorted(counts),
        "base_columns": list(res.base_columns),
        "n_base_columns": len(res.base_columns),
        "seconds": round(time.time() - t0, 1),
    }


def vwap_ground_condition(cap) -> dict:
    """Can this probe reach `vwap_distance`'s LEGAL ground on these frames?

    The legal ground is the same-row `mid_price` read. The probe perturbs only
    the declared aggregate frames. The condition holds when `mid_price` lives in
    a frame the probe does not perturb and in none that it does.
    """
    perturbed = {k for k in MODEL.aggregate_frames if k in cap.raw}
    src_frame, src_col = LEGAL_GROUND_SOURCE
    src = cap.raw.get(src_frame)
    in_source = src is not None and src_col in src.columns
    in_perturbed = sorted(
        k for k in perturbed if src_col in cap.raw[k].columns)
    holds = in_source and not in_perturbed
    return {
        "holds": holds,
        "perturbed_frames": sorted(perturbed),
        "legal_ground_column": "%s.%s" % (src_frame, src_col),
        "legal_ground_column_present_in_its_frame": in_source,
        "legal_ground_column_found_in_perturbed_frames": in_perturbed,
        "ground": (
            "the probe perturbs only %s; the legal same-row read lives in %s, "
            "which is not among them, so a movement in %s can only rest on the "
            "forward-join ground the map declares violating"
            % (", ".join(sorted(perturbed)), src_frame, DUAL_GROUND_COLUMN))
        if holds else (
            "the legal ground is reachable by this configuration, or its column "
            "is absent, so a finding on %s cannot be attributed to the declared "
            "violating ground here" % DUAL_GROUND_COLUMN),
    }


def score_instrument_month(im: dict, req, classes, mp) -> dict:
    """Criteria 1 and 2 for one instrument-month, per side where the map declares."""
    sym, month = im["instrument"], im["month"]
    clean = sorted(c for c, k in classes.items() if k == "CLEAN")
    vw = im["vwap_ground_condition"]
    out = {"criterion_1_contexts": [], "criterion_2": None}

    for side in SIDES:
        sd = im["sides"].get(side)
        if not sd:
            continue
        present = set(sd["base_columns"])
        found = set(sd["features_with_findings"])
        governing = {k for _c, k in req}
        scored_here = any(declares_violation(mp.get((side, sym, month, g)))
                          for g in governing)
        if not scored_here:
            out["criterion_1_contexts"].append({
                "side": side, "scored": False,
                "ground": "no governing class carries a strict count on this "
                          "side, instrument and month; `ties` is declared "
                          "`available`, so an equal count is not a violation",
                "units": []})
            continue

        units = []
        for col, klass in sorted(req):
            cell = mp.get((side, sym, month, klass))
            if col not in present:
                state, why = "unsupported", (
                    "absent from the built frame; section 8.2 -- missing or "
                    "impossible inputs are unsupported, never a pass")
            elif not declares_violation(cell):
                state, why = "no_declared_violation", (
                    "the governing cell carries no strict count on this side, "
                    "so SC-5(b)'s 'in the cells the map declares' is not met")
            elif col == DUAL_GROUND_COLUMN and not vw["holds"]:
                state, why = "excluded_ground_not_established", vw["ground"]
            elif classes.get(col) == "DESCENDANT" and col in found:
                state, why = "secondary_only", (
                    "the manifest classes this column a descendant, so section "
                    "7.6 makes its findings secondary and line 700 says they do "
                    "not satisfy criterion 1")
            elif col in found:
                state, why = "satisfied", (
                    "at least one primary finding attributed to this column, in "
                    "a cell the map declares by a strict count")
            else:
                state, why = "missed", "no finding attributed to this column"
            units.append({"column": col, "governing_map_class": klass,
                          "state": state, "ground": why,
                          "declared_cell": cell,
                          "present_in_built_frame": col in present})
        out["criterion_1_contexts"].append({
            "side": side, "scored": True, "units": units,
            "counts": {s: sum(1 for u in units if u["state"] == s)
                       for s in sorted({u["state"] for u in units})}})

    con = im["sides"].get("contaminated")
    if con:
        present = set(con["base_columns"])
        found = set(con["features_with_findings"])
        units = []
        for col in clean:
            if col not in present:
                state, why = "unsupported", (
                    "absent from the built frame on the contaminated side; "
                    "section 8.2, and never displayed as a pass")
            elif col in found:
                state, why = "violated", (
                    "a finding names a manifest-clean column on the "
                    "contaminated side; criterion 2 admits any tier")
            else:
                state, why = "clean", "no finding of any tier names this column"
            units.append({"column": col, "state": state, "ground": why,
                          "present_in_built_frame": col in present})
        out["criterion_2"] = {
            "population": len(clean),
            "reachable_population": sum(
                1 for u in units if u["state"] != "unsupported"),
            "units": units,
            "counts": {s: sum(1 for u in units if u["state"] == s)
                       for s in sorted({u["state"] for u in units})}}

    unexpected = sorted(
        set().union(*[set(im["sides"][s]["features_with_findings"])
                      for s in im["sides"]]) - {c for c, _ in req} - set(clean))
    out["features_with_findings_not_in_either_declared_list"] = [
        {"feature": f, "manifest_class": classes.get(f, "NOT_IN_MANIFEST")}
        for f in unexpected]
    return out


def predicted_probe_seconds(cap) -> float:
    """The PROBE phase only, predicted from snapshot rows.

    THE CAPTURE IS MEASURED, NOT PREDICTED, and the halt is on the probe phase
    alone. The capture's cost is dominated by a scan of the raw order-book file,
    whose size varies by more than two orders of magnitude across this
    population; one warm-cache measurement does not support extrapolating it, and
    a halt built on a number that weak would fire on the model rather than on the
    run. The probe phase is builds and fingerprinting over the snapshot's rows,
    which is the term the single measured point actually measured.
    """
    snap = cap.frames.get("snap")
    return SEC_PER_M_SNAP_ROWS * (0 if snap is None else len(snap)) / 1e6


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    req = required_units()
    classes = manifest_columns()
    mp = load_map()
    clean = sorted(c for c, k in classes.items() if k == "CLEAN")
    population = [{"instrument": s, "month": m} for s in INSTRUMENTS for m in MONTHS]
    log("population: %d instrument-month(s); %d REQUIRED, %d CLEAN (harness side)"
        % (len(population), len(req), len(clean)))

    doc: dict = {
        "detector": "L3.1 -- the availability probe (leakaudit.availability)",
        "scope": {"instruments": list(INSTRUMENTS), "months": list(MONTHS),
                  "sides": list(SIDES), "artifact": "A (the f2 rebuild pair)",
                  "stride": STRIDE, "max_cohorts": MAX_COHORTS, "seed": SEED},
        "criteria_scored": [1, 2],
        "criterion_3": "BLOCKED_LABEL_GAP_SEE_DEVIATIONS_D_V30A_28",
        "criterion_4": "BLOCKED_LABEL_GAP_SEE_DEVIATIONS_D_V30A_28",
        "gate_result": "NOT_A_GATE_RESULT_TWO_OF_FOUR_CRITERIA",
        "violation_predicate": "strict_count > 0; `ties` is declared `available`",
        "criterion_2_reach_note":
            "of 4 manifest-CLEAN columns 1 is present in the built frame, so "
            "criterion 2 has ONE reachable unit per instrument-month however "
            "many instrument-months are run. Its reach does not grow with the "
            "population.",
        "gate_status_of_repository": {
            "exit": 1, "finding": "hash_set_single_source at HISTORY.md",
            "disposition": "known false positive, disclosed at D-V30A-11"},
        "required_units_pairs": req,
        "manifest_clean": clean,
        "cost_model": {"sec_per_M_snap_rows": SEC_PER_M_SNAP_ROWS,
                       "halt_multiple": COST_HALT_MULTIPLE,
                       "halt_applies_to": "the probe phase only; the capture is "
                                          "measured, never predicted",
                       "basis": "one measured point, zc 2025-01 at 444 s"},
        "instrument_months": [],
    }

    t_all = time.time()
    for spec in population:
        sym, month = spec["instrument"], spec["month"]
        im: dict = {"instrument": sym, "month": month, "run_status": "ok",
                    "sides": {}}
        t0 = time.time()
        try:
            log("%s %s: capturing" % (sym, month))
            cap = fa.read_inputs(sym, month)
            im["capture_seconds"] = round(time.time() - t0, 1)
            im["raw_frames"] = {k: list(v.shape) for k, v in cap.raw.items()}
            im["frames_absent"] = sorted(
                k for k in ("snap", "trades", "magg") if k not in cap.raw)
            im["predicted_probe_seconds"] = round(predicted_probe_seconds(cap), 1)
            im["vwap_ground_condition"] = vwap_ground_condition(cap)
            t_probe = time.time()
            for side in SIDES:
                im["sides"][side] = probe_side(cap, sym, month, side)
                log("  %s %s %-13s %s, %d record(s), %d feature(s), %.0f s"
                    % (sym, month, side, im["sides"][side]["probe_verdict"],
                       im["sides"][side]["n_finding_records"],
                       len(im["sides"][side]["features_with_findings"]),
                       im["sides"][side]["seconds"]))
            im["probe_seconds"] = round(time.time() - t_probe, 1)
            im["scoring"] = score_instrument_month(im, req, classes, mp)
        except BaseException as exc:                       # noqa: BLE001
            im["run_status"] = "could_not_run"
            im["failure"] = "%s: %s" % (type(exc).__name__, exc)
            im["traceback"] = traceback.format_exc()
            log("  %s %s COULD NOT RUN: %s" % (sym, month, im["failure"]))
        im["seconds"] = round(time.time() - t0, 1)
        pred, actual = im.get("predicted_probe_seconds"), im.get("probe_seconds")
        if pred and actual and actual > COST_HALT_MULTIPLE * pred:
            im["cost_halt"] = ("the probe phase took %.0f s, which exceeds %gx "
                               "the predicted %.0f s"
                               % (actual, COST_HALT_MULTIPLE, pred))
            doc["instrument_months"].append(im)
            doc["halted"] = "%s %s: %s" % (sym, month, im["cost_halt"])
            OUT.write_text(json.dumps(doc, indent=1, sort_keys=True, default=str),
                           encoding="utf-8", newline="")
            log("HALT: %s" % doc["halted"])
            return 2
        doc["instrument_months"].append(im)
        doc["elapsed_seconds"] = round(time.time() - t_all, 1)
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
