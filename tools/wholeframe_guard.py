#!/usr/bin/env python3
"""The whole-frame path must not move after the wiring. R205 §3.2, R231 §4.

MOVED HERE FROM A SESSION SCRATCH DIRECTORY AT R231, and the move is the point
rather than tidying. This is the instrument whose result is quoted more often
than any other in this project, and it lived in a directory that gets cleaned —
which is exactly the property that made `15dc83c7…` unreproducible by anyone
(D-V30A-60) and the corner environment unrebuildable (D-V30A-58). **An assertion
that lives in a file that can vanish is an assertion nobody can re-run.**

    $ LEAKAUDIT_FIXTURE=1 py -3.12 tools/wholeframe_guard.py


Phase 1's entire evidence base was produced through the whole-frame path. If the
per-column wiring altered it, that is not a Phase 2 bug; it is a question about
the Phase 1 numbers, and it halts.

Same instrument-month, same stride, same seed, same model as the committed
population run. The comparison is against that run's own recorded figures, read
from the committed file rather than remembered.

Written with the Write tool per D2.1.
"""
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8")

import pandas as pd  # noqa: E402

from leakaudit import fixture_adapter as fa  # noqa: E402  # isort:skip


# ---------------------------------------------------------------------------
# THE RELATION. R231 §4.
# ---------------------------------------------------------------------------
#
# WHAT WAS MISSING. This guard reported eight terms SAME and that was read as
# "the probe still works". It establishes something narrower: that eight numbers
# match eight committed numbers. **The guard's SAME was a believed silence** --
# R215 §0's refinement, which says a result every plausible wrong instrument
# would also produce tests wiring rather than validity, pointed at the guard
# itself.
#
# THE RELATION THE TWO SIDES MUST STAND IN. The contaminated side is a fixture
# built with a known leak; the corrected side is the same fixture with it
# removed. So the contaminated side MUST FIND and the corrected side MUST NOT.
# That is what makes the comparison meaningful, and until now it held only
# because the committed baseline happened to encode it -- a property of the
# arrangement rather than a checked fact.
#
# WHAT CHECKING IT INDEPENDENTLY CATCHES that the term comparison does not.
# The comparison's authority is a file in this repository. If
# `criteria_12_population.json` were edited -- by a bad merge, a regenerated
# artifact, or a hand -- the comparison would pass against the edited values and
# report SAME. The relation is a property of the RUN, not of the baseline, so it
# survives a corrupted baseline and fails on one that no longer describes a
# discriminating probe.
#
# IT IS CHECKED FIRST AND HALTS. Reading a term-by-term SAME from a pair of
# sides that do not discriminate is reading a coincidence of two numbers, so the
# comparison is not printed at all if the relation fails.


def relation_holds(out: dict) -> bool:
    """The contaminated side finds; the corrected side does not."""
    c, k = out.get("contaminated", {}), out.get("corrected", {})
    return (c.get("verdict") == "finding" and c.get("records", 0) > 0
            and k.get("verdict") == "observed_silence"
            and k.get("records", 1) == 0)


def relation_report(out: dict) -> list:
    """One line per limb, so a failure names which limb failed."""
    c, k = out.get("contaminated", {}), out.get("corrected", {})
    limbs = [
        ("contaminated FINDS", c.get("verdict") == "finding",
         "verdict=%s" % c.get("verdict")),
        ("contaminated records > 0", c.get("records", 0) > 0,
         "records=%s" % c.get("records")),
        ("corrected is SILENT", k.get("verdict") == "observed_silence",
         "verdict=%s" % k.get("verdict")),
        ("corrected records == 0", k.get("records", 1) == 0,
         "records=%s" % k.get("records")),
    ]
    return ["%-26s %-4s %s" % (name, "OK" if ok else "FAIL", detail)
            for name, ok, detail in limbs]


from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402
from leakaudit.availability_trace import traces_for  # noqa: E402


# ---------------------------------------------------------------------------
# THE RUN. Behind `main()` so the module can be IMPORTED without executing it.
# ---------------------------------------------------------------------------
#
# It was not, and the cost was immediate: the first test file to import this
# module for its pure functions ran the entire nine-minute guard as an import
# side effect, and passed. A test that takes seven minutes to assert a
# dictionary comparison is a test nobody will keep running, and the reason was
# invisible from the test.


def main() -> int:
    PRIOR = REPO / "evidence" / "phase1" / "criteria_12_population.json"
    SYM, MONTH, STRIDE, SEED, MAXC = "zc", "2025-01", 997, 20260828, 300
    MODEL = AvailabilityModel(aggregate_frames={"magg": "ts_floor", "trades": "ts_event"},
                              decision_column="timestamp")

    prior = json.loads(PRIOR.read_text(encoding="utf-8"))
    im = [i for i in prior["instrument_months"]
          if i["instrument"] == SYM and i["month"] == MONTH][0]

    print("BASELINE, from the committed population run:")
    for s in ("contaminated", "corrected"):
        x = im["sides"][s]
        print("  %-13s verdict=%-17s eligible=%-4d records=%-5d features=%d"
              % (s, x["probe_verdict"], x["n_eligible"], x["n_finding_records"],
                 len(x["features_with_findings"])))

    t0 = time.time()
    cap = fa.read_inputs(SYM, MONTH)
    print("\ncapture %.0f s" % (time.time() - t0))

    # THE POPULATION IS READ, NOT CARRIED. R212 §2(b). This harness holds no copy of
    # the module list; it reads `evidence/session/PROBE_PATH_SET.json` through
    # `tools/probe_path_guard.py`, which REFUSES rather than returning an empty set
    # when that file is missing or unparseable. `watch()` also records every module
    # this run actually enters, so a module reached here and absent from the file is
    # reported by the guard itself rather than drifting while the guard keeps passing.
    sys.path.insert(0, str(REPO / "tools"))
    import probe_path_guard as ppg  # noqa: E402

    print("guard population: %d modules, measured at commit %s"
          % (len(ppg.path_set()), ppg.measured_at()))

    out = {}
    _watch = ppg.watch()
    _seen = _watch.__enter__()
    for side in ("contaminated", "corrected"):
        t = time.time()
        build = fa.builder_for(cap, side)
        # column_modes NOT passed: this is the whole-frame path exactly as it was.
        res = run_probe_a(cap.raw, build, MODEL, side=side,
                          cohort_stride=STRIDE, max_cohorts=MAXC, seed=SEED)
        built = build(dict(cap.raw))
        d = pd.to_datetime(built[MODEL.decision_column])
        picked = sorted(d.dt.floor("s").unique())[::STRIDE][:MAXC]
        # THE POPULATION HARNESS'S OWN LOOP, replicated exactly. `eligible_cohorts`
        # is NOT used: the extracted function refuses the aware-against-naive case
        # this fixture actually contains, and the baseline was produced by this rule.
        # Using the extracted one here would compare the wiring against a different
        # eligibility derivation and answer a question nobody asked.
        pset = set(picked)
        have = set()
        for fname, keycol in MODEL.aggregate_frames.items():
            f = cap.frames.get(fname)
            if f is None:
                continue
            k = pd.to_datetime(f[keycol])
            if getattr(k.dt, "tz", None) is not None:
                k = k.dt.tz_convert("UTC").dt.tz_localize(None)
            have |= (set(k.dt.floor("s").unique()) & pset)
        eligible = [s2 for s2 in picked if s2 in have]
        traces = traces_for(res, eligible, case_id="guard_%s" % side)
        recs = sum(1 for tr in traces for r in tr.records if r.finding is not None)
        feats = sorted({r.finding.feature for tr in traces for r in tr.records
                        if r.finding is not None})
        out[side] = {"verdict": res.verdict(), "eligible": len(eligible),
                     "records": recs, "features": feats,
                     "seconds": round(time.time() - t, 1)}
        print("  %-13s verdict=%-17s eligible=%-4d records=%-5d features=%d  (%.0f s)"
              % (side, res.verdict(), len(eligible), recs, len(feats),
                 out[side]["seconds"]))

    _watch.__exit__(None, None, None)

    print("\nTHE RELATION, checked before the comparison:")
    for line in relation_report(out):
        print("  " + line)
    if not relation_holds(out):
        print("\nHALT: the guard's two sides do not stand in the relation that makes "
              "its SAME mean anything. Do not read the comparison below.")
        return 3

    print("\nCOMPARISON, term by term:")
    moved = False
    for side in ("contaminated", "corrected"):
        b, n = im["sides"][side], out[side]
        for key, before, after in (
                ("verdict", b["probe_verdict"], n["verdict"]),
                ("eligible", b["n_eligible"], n["eligible"]),
                ("records", b["n_finding_records"], n["records"]),
                ("features", sorted(b["features_with_findings"]), n["features"])):
            same = before == after
            moved = moved or not same
            shown = ("%d" % len(before)) if key == "features" else before
            shown2 = ("%d" % len(after)) if key == "features" else after
            print("  %-13s %-9s %s  %s -> %s"
                  % (side, key, "SAME" if same else "MOVED", shown, shown2))

    print()
    if moved:
        print("HALT: the whole-frame path MOVED. This is a question about the Phase 1 "
              "numbers, not a Phase 2 bug.")
        return 2
    print("UNCHANGED. The whole-frame path is byte-for-byte the result the committed "
          "population run recorded, so the wiring did not alter the probe that "
          "produced Phase 1's evidence.")

    return 0


if __name__ == "__main__":                                   # pragma: no cover
    raise SystemExit(main())
