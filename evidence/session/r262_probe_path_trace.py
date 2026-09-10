"""R262 §4. Probe-path membership, re-measured rather than reasoned.

    PYTHONPATH=. py -3.12 evidence/session/r262_probe_path_trace.py

WHY THIS EXISTS. `PROBE_PATH_SET.json` was built by a TRACE -- `sys.monitoring`
PY_START over four runs, recording the file of every frame entered. R261 added
`label_probe.py` to `not_on_the_path` by READING IMPORTS instead: nothing in
`availability.py` imports it, so nothing on the probe's path can reach it. That
argument is sound and it is a different instrument from the one that built the
set, and a set half-measured and half-reasoned is two sets. R262 §4: re-run the
trace; membership is what it returns.

WHAT THIS COVERS AND WHAT IT DOES NOT. Runs A, B and C of the original four are
synthetic and are reproduced here. Run D is the whole-frame fixture guard, which
carries its own recorder and reports its own executed set on every run -- it is
not reproduced here, and its result is read from that run rather than restated.
A NEW RUN IS ADDED, and it is the point: run E executes the label probe, so the
trace can say what L2a's execution reaches as well as what L3.1's does.

Written with the Write tool per D2.1. Read-only against the repository.
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np
import pandas as pd

REPO = pathlib.Path.cwd()
for p in (str(REPO), str(REPO / "src"), str(REPO / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import probe_path_guard as ppg                                    # noqa: E402
from leakaudit.availability import (AvailabilityModel,            # noqa: E402
                                    eligible_cohorts, run_probe_a)
from leakaudit.availability_trace import traces_for               # noqa: E402
from leakaudit.label_probe import (LabelAvailability,             # noqa: E402
                                   RawLabel, run_probe_l2a)
from leakaudit.modes import ColumnMode                            # noqa: E402

T0 = pd.Timestamp("2026-01-01 00:00:00")
SEC = pd.Timedelta(seconds=1)
N = 60
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")


def frames():
    ts = [T0 + i * SEC for i in range(N)]
    rng = np.random.default_rng(19)
    return {"agg": pd.DataFrame({"k": ts, "v": rng.standard_normal(N),
                                 "y": rng.standard_normal(N)})}


def build(raw):
    agg = raw["agg"]
    v = agg["v"].to_numpy()
    return pd.DataFrame({"d": agg["k"].to_numpy(),
                         "x": np.concatenate(([np.nan], v[:-1]))})


def run_a():
    """The whole-frame path -- the one Phase 1's evidence came through."""
    run_probe_a(frames(), build, MODEL, side="A", cohort_stride=7,
                max_cohorts=8)


def run_b():
    """The per-column path -- what the modes wiring added."""
    run_probe_a(frames(), build, MODEL, side="B", cohort_stride=7,
                max_cohorts=8, column_modes={"v": ColumnMode("at_timestamp")})


def run_c():
    """The whole reported-figures path: probe -> eligibility -> traces."""
    raw = frames()
    res = run_probe_a(raw, build, MODEL, side="C", cohort_stride=7,
                      max_cohorts=8)
    built = build(raw)
    d = pd.to_datetime(built["d"])
    picked = sorted(d.dt.floor("s").unique())[::7][:8]
    elig = eligible_cohorts(raw, MODEL, picked, d)
    traces_for(res, elig.eligible, case_id="C")


def run_e():
    """NEW AT R262: the label probe. The set had never been traced with L2a
    executing, so its membership had never been measured in either direction."""
    run_probe_l2a(frames(), build, MODEL, side="E",
                  raw_label=RawLabel("agg", "y"),
                  label_availability=LabelAvailability(
                      base_column="k", horizon=pd.Timedelta(seconds=30)),
                  cohort_stride=7, max_cohorts=5)


RUNS = (("A -- whole-frame path", run_a),
        ("B -- per-column path", run_b),
        ("C -- reported-figures path", run_c),
        ("E -- the label probe (new at R262)", run_e))


def _one(index: int) -> int:
    """Trace exactly one run and print its set as JSON. A CHILD PROCESS."""
    label, fn = RUNS[index]
    with ppg.record_modules() as seen:
        fn()
    print("__TRACE__" + json.dumps({"label": label, "seen": sorted(seen)}))
    return 0


def main() -> int:
    import subprocess

    if len(sys.argv) > 1 and sys.argv[1].startswith("--only="):
        return _one(int(sys.argv[1].split("=", 1)[1]))

    recorded = set(ppg.path_set())
    print("=" * 76)
    print("R262 section 4 -- probe-path membership, traced")
    print("=" * 76)
    print("recorded set: %d module(s), measured at commit %s"
          % (len(recorded), ppg.measured_at()))
    print()
    print("EACH RUN IS TRACED IN ITS OWN PROCESS, and the first version of this")
    print("script did not do that. `record_modules` uses `sys.monitoring`")
    print("PY_START with per-code-object DISABLE, so a code object entered once")
    print("is not reported again -- which makes a RUN'S OWN SET depend on what")
    print("ran before it in the same process. Traced in sequence, run E reported")
    print("one module and reaches four; the union over all runs was still right,")
    print("because a module is recorded on its first sighting, but a per-run")
    print("answer was not. The question here is per-run, so the processes are")
    print("separate.")
    print()

    per_run = {}
    for i, (label, _fn) in enumerate(RUNS):
        r = subprocess.run(
            [sys.executable, __file__, "--only=%d" % i],
            capture_output=True, text=True, encoding="utf-8", cwd=str(REPO),
            env={**__import__("os").environ, "PYTHONPATH": str(REPO)})
        line = [ln for ln in r.stdout.splitlines()
                if ln.startswith("__TRACE__")]
        if r.returncode != 0 or not line:
            print("REFUSED: run %s exited %d and produced no trace: %s"
                  % (label, r.returncode, (r.stderr or "")[-400:]))
            return 1
        seen = set(json.loads(line[0][len("__TRACE__"):])["seen"])
        per_run[label] = seen
        print("%-38s executed %d module(s)" % (label, len(seen)))
        for m in sorted(seen):
            mark = "  " if m in recorded else "NEW"
            print("    %s %s" % (mark, m))
        print()

    l31 = set().union(*(per_run[k] for k in per_run if not k.startswith("E")))
    l2a = per_run["E -- the label probe (new at R262)"]
    print("-" * 76)
    print("UNION over the L3.1 runs (A, B, C): %d module(s)" % len(l31))
    print("  reached and NOT in the recorded set: %s"
          % (sorted(l31 - recorded) or "none"))
    print("  in the recorded set and not reached here: %s"
          % (sorted(recorded - l31) or "none"))
    print()
    print("THE QUESTION R262 section 4 ASKS: is label_probe.py on the path?")
    print("  reached by any L3.1 run (A, B, C)?  %s"
          % ("YES" if "src/leakaudit/label_probe.py" in l31 else "NO"))
    print("  reached by the L2a run (E)?          %s"
          % ("YES" if "src/leakaudit/label_probe.py" in l2a else "NO"))
    print("  modules L2a's own execution reaches that the recorded set holds:")
    for m in sorted(l2a & recorded):
        print("    %s" % m)
    print()
    print("Run D -- the whole-frame fixture guard -- carries its own recorder")
    print("and reports its executed set on every run; it is read from there,")
    print("not restated here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
