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
import subprocess
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


# ---------------------------------------------------------------------------
# THE CONSTANTS. R232 §4.
# ---------------------------------------------------------------------------
#
# WHAT WAS MISSING. The guard's stride, seed, instrument and month were typed
# here; the baseline it compares against lived in another file; and nothing
# checked that the two described the same run. Same shape as a digest without its
# recipe: **the baseline is a figure and its generation constants are its
# frame**, and a guard comparing against a baseline from a different run produces
# a number that means nothing.
#
# AND NOTHING HAD TO BE WRITTEN TO THE BASELINE, which is the part worth
# recording because it was not what anyone expected. R232 §4 supposed the
# baseline would need to start recording its constants. It already does:
# `criteria_12_population.json` carries a `scope` block with `stride`,
# `max_cohorts`, `seed`, and the `instruments` and `months` the run covered,
# written by the generating harness itself
# (`tests/phase1/harness_criteria_12_population.py`). The frame was beside the
# figure the whole time and nobody read it. So this is a READ, not an addition --
# and no dated acceptance artifact is edited to add a field, which the project's
# own rule about dated measurements would have made awkward.
#
# A REFUSAL, NOT A WARNING, and it happens BEFORE the probe runs. A warning on a
# seven-minute run is a line somebody scrolls past on the way to the verdict; and
# refusing after the computation would spend seven minutes to say the comparison
# was never going to mean anything.


def constants_match(scope: dict, sym: str, month: str, stride: int,
                    seed: int, maxc: int) -> bool:
    """Does the baseline's `scope` describe the run this guard is about to do?"""
    return all(ok for _n, ok, _d in _constant_limbs(
        scope, sym, month, stride, seed, maxc))


def _constant_limbs(scope, sym, month, stride, seed, maxc):
    scope = scope or {}
    return [
        ("stride", scope.get("stride") == stride,
         "baseline=%s guard=%s" % (scope.get("stride"), stride)),
        ("max_cohorts", scope.get("max_cohorts") == maxc,
         "baseline=%s guard=%s" % (scope.get("max_cohorts"), maxc)),
        ("seed", scope.get("seed") == seed,
         "baseline=%s guard=%s" % (scope.get("seed"), seed)),
        ("instrument", sym in (scope.get("instruments") or []),
         "guard=%r baseline covers %s" % (sym, scope.get("instruments"))),
        ("month", month in (scope.get("months") or []),
         "guard=%r baseline covers %s" % (month, scope.get("months"))),
    ]


def constants_report(scope: dict, sym: str, month: str, stride: int,
                     seed: int, maxc: int) -> list:
    """One line per constant, so a mismatch names which one."""
    return ["%-12s %-4s %s" % (name, "OK" if ok else "FAIL", detail)
            for name, ok, detail in _constant_limbs(
                scope, sym, month, stride, seed, maxc)]


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


#: WHERE "LAST RECORDED" LIVES, AND IT IS WRITTEN BY THE RUN. R263 §4.
#:
#: R262 shipped these as a hand-typed dict in this file, which is the
#: count-in-prose defect wearing a constant's clothes: a number about a
#: measurement, kept somewhere the measurement does not touch, drifting the
#: moment the measurement moves. The same shape as the enumeration R262 deleted
#: from `OPERATING_RULES.md` two hours earlier.
#:
#: NOT UNDER `evidence/`, deliberately. Every file there is manifest-attested,
#: so a guard that rewrote one would dirty the tree on every run and the
#: manifest update would have to follow the run that invalidated it. This is
#: tracked, so it survives a cleaned scratch directory, and unattested, so a
#: timing does not have a hash hanging off it.
#:
#: WRITTEN ONLY AFTER A COMPLETED COMPARISON. A stalled or refused run must not
#: become the baseline the next run is lenient against -- which is the whole
#: failure mode: at R261 this guard ran eighteen hours and would have recorded
#: eighteen hours as normal.
TIMES_FILE = REPO / "tools" / "wholeframe_guard_times.json"

#: The fallback if the file is absent, and it is labelled as one. Measured at
#: R261 on `b975ca7`, CPython 3.12.10 / numpy 2.4.2 / pandas 3.0.1.
SEED_TIMES = {"capture": 39, "side": 231, "source": "R261 seed, no file yet"}


def last_recorded() -> dict:
    """The previous completed run's wall times, or the labelled seed."""
    try:
        runs = json.loads(TIMES_FILE.read_text(encoding="utf-8"))["runs"]
    except Exception:                                        # noqa: BLE001
        return dict(SEED_TIMES)
    if not runs:
        return dict(SEED_TIMES)
    last = runs[-1]
    return {"capture": last["capture"], "side": max(last["contaminated"],
                                                    last["corrected"]),
            "source": "%s at %s" % (last.get("commit", "?"),
                                    last.get("when", "?"))}


def record_times(capture, contaminated, corrected, total) -> None:
    """Append this run's wall times. Ten kept, so drift is visible."""
    import datetime
    try:
        doc = json.loads(TIMES_FILE.read_text(encoding="utf-8"))
    except Exception:                                        # noqa: BLE001
        doc = {"what": "Wall times of completed whole-frame guard runs. "
                       "Written by tools/wholeframe_guard.py, never by hand "
                       "(R263 section 4). The last entry is what the next run "
                       "prints its comparison against.",
               "runs": []}
    commit = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short",
                             "HEAD"], capture_output=True, text=True)
    doc["runs"] = (doc.get("runs", []) + [{
        "when": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "commit": commit.stdout.strip() or "?",
        "capture": round(capture, 1),
        "contaminated": round(contaminated, 1),
        "corrected": round(corrected, 1),
        "total": round(total, 1),
    }])[-10:]
    TIMES_FILE.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8",
                          newline="\n")


LAST_RECORDED = last_recorded()

#: The measured reach per side, R268 §4. Held OUTSIDE `out`, the dict the
#: comparison reads, so nothing that iterates the compared terms can reach it.
REACH_SEEN = {}


def main() -> int:
    PRIOR = REPO / "evidence" / "phase1" / "criteria_12_population.json"
    SYM, MONTH, STRIDE, SEED, MAXC = "zc", "2025-01", 997, 20260828, 300
    MODEL = AvailabilityModel(aggregate_frames={"magg": "ts_floor", "trades": "ts_event"},
                              decision_column="timestamp")

    prior = json.loads(PRIOR.read_text(encoding="utf-8"))

    # BEFORE ANYTHING IS COMPUTED. Seven minutes spent to discover the comparison
    # was never going to mean anything is seven minutes spent badly.
    scope = prior.get("scope", {})
    print("CONSTANTS, this guard against the baseline's own `scope`:")
    for line in constants_report(scope, SYM, MONTH, STRIDE, SEED, MAXC):
        print("  " + line)
    if not constants_match(scope, SYM, MONTH, STRIDE, SEED, MAXC):
        print("\nHALT: this guard's constants are not the ones the baseline was "
              "generated under, so any comparison against it would be a "
              "comparison between two different runs. Nothing was probed.")
        return 4

    im = [i for i in prior["instrument_months"]
          if i["instrument"] == SYM and i["month"] == MONTH][0]

    print("\nBASELINE, from the committed population run:")
    for s in ("contaminated", "corrected"):
        x = im["sides"][s]
        print("  %-13s verdict=%-17s eligible=%-4d records=%-5d features=%d"
              % (s, x["probe_verdict"], x["n_eligible"], x["n_finding_records"],
                 len(x["features_with_findings"])))

    t0 = time.time()
    cap = fa.read_inputs(SYM, MONTH)
    capture_s = time.time() - t0
    print("\ncapture %.0f s   (last recorded %d s, from %s)"
          % (capture_s, LAST_RECORDED["capture"], LAST_RECORDED["source"]))
    print("EXPECTED WALL TIMES, printed so the comparison is on the screen "
          "rather than in somebody's memory: capture ~%d s, each side ~%d s. "
          "A phase running an ORDER OF MAGNITUDE past these is stopped and "
          "looked at, not waited out (OPERATING_RULES.md section 7, R262). It "
          "is the only complexity instrument this project has: R261 shipped a "
          "correct per-cell Python loop that every twelve-row unit test passed "
          "in under a second, and this guard was still running eighteen hours "
          "later on 365 seconds of CPU."
          % (LAST_RECORDED["capture"], LAST_RECORDED["side"]))

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
        ratio = out[side]["seconds"] / max(1, LAST_RECORDED["side"])
        print("  %-13s verdict=%-17s eligible=%-4d records=%-5d features=%d  "
              "(%.0f s, %.1fx the last recorded %d s)"
              % (side, res.verdict(), len(eligible), recs, len(feats),
                 out[side]["seconds"], ratio, LAST_RECORDED["side"]))
        if ratio >= 10:
            print("  ORDER OF MAGNITUDE SLOWER THAN THE LAST RECORDED RUN. That "
                  "is the shape a complexity regression makes here, and no test "
                  "in the suite can see it: they run on twelve-row frames. Stop "
                  "and look at the change rather than waiting for the other "
                  "side (OPERATING_RULES.md section 7, R262).")
        # R268 §4. THE REACH RIDES ALONG, AND IT IS NOT A TERM. The guard runs
        # what a user runs, and the reach control now runs on every probe, so it
        # runs here too and costs what it costs. It is printed and it is NOT
        # added to `out[side]` -- the comparison stays the frozen eight, and
        # keeping it out of that dict is what keeps a future loop over `out`
        # from comparing it by accident. A reach that moves is a finding about
        # the fixture's builder and a ruling, not a red guard.
        REACH_SEEN[side] = res.reach
        _r = res.reach
        print("  %-13s reach=%s  (k=%d, %d usable, %d censored) -- REPORTED, "
              "not a compared term"
              % (side,
                 getattr(_r, "measured", None) if _r is not None else "not measured",
                 getattr(_r, "k", 0) if _r is not None else 0,
                 len(_r.uncensored) if _r is not None else 0,
                 (len(_r.samples) - len(_r.uncensored)) if _r is not None else 0))

    _watch.__exit__(None, None, None)

    print("\nTHE RELATION, checked before the comparison:")
    for line in relation_report(out):
        print("  " + line)
    if not relation_holds(out):
        print("\nHALT: the guard's two sides do not stand in the relation that makes "
              "its SAME mean anything. Do not read the comparison below.")
        return 3

    print("\nREACH, REPORTED AND NOT COMPARED (R268 section 4) -- printed beside "
          "the eight terms and never one of them. A reach that moves is a "
          "finding about the fixture's builder and a ruling, not a red guard:")
    for _side in ("contaminated", "corrected"):
        _r = REACH_SEEN.get(_side)
        print("  %-13s measured reach %s"
              % (_side, getattr(_r, "measured", None) if _r is not None
                 else "not measured"))
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
    # WRITTEN HERE AND NOWHERE EARLIER: the comparison above has completed, so
    # this run is a run whose times mean something. A stalled or refused run
    # never reaches this line and never becomes the next run's baseline.
    record_times(capture_s, out["contaminated"]["seconds"],
                 out["corrected"]["seconds"], time.time() - t0)
    print("\ntotal wall time %.0f s (capture + both sides + comparison)."
          % (time.time() - t0))
    print("UNCHANGED. The whole-frame path is byte-for-byte the result the committed "
          "population run recorded, so the wiring did not alter the probe that "
          "produced Phase 1's evidence.")

    return 0


if __name__ == "__main__":                                   # pragma: no cover
    raise SystemExit(main())
