"""B-6 controls -- Probe A's known positive and known negative. R151 §4/§6.

A FAILING KNOWN-POSITIVE IS A HALT. These run before Probe A is pointed at the
acceptance fixture, and they are SYNTHETIC ON PURPOSE: R151 requires a control
built independently of the thing under measurement, "so the probe's own test does
not depend on the thing under measurement." If the only positive were the
fixture's own contamination, a probe that fired would be evidence of nothing but
itself.

  POSITIVE  a builder that reads its OWN second's aggregate -- a cell the model
            marks unavailable, since the aggregate over [F, F+1s) completes at
            F+1s and the decision instant lies inside F. Probe must FIRE, and
            fire IN-SECOND.
  NEGATIVE  a builder that reads the PREVIOUS second's aggregate -- available,
            since its instant is F and the decision instant is >= F. Probe must
            be silent IN-SECOND.

THE NEGATIVE'S SECOND REQUIREMENT, AND IT IS THE ONE THAT MATTERS. Silence
in-second is worthless unless the corruption reached the build at all. So the
negative must MOVE THE FOLLOWING SECOND'S ROWS: that proves the probe is live,
the corruption landed, and the only thing separating the two builders is WHEN
they read. A negative that moves nothing anywhere is a probe testing itself.

    usage: b6_probe_a_controls.py
"""
from __future__ import annotations

import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[2]
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import numpy as np                                       # noqa: E402
import pandas as pd                                      # noqa: E402

from leakaudit.availability import (                     # noqa: E402
    AvailabilityModel, run_probe_a)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                        # noqa: BLE001
    pass

N_SECONDS, ROWS_PER_SECOND, SEED = 4000, 3, 20260828
rng = np.random.default_rng(SEED)

# --- the raw frames -------------------------------------------------------
start = pd.Timestamp("2026-01-01 00:00:00")
secs = pd.date_range(start, periods=N_SECONDS, freq="1s")

# The aggregate frame: one row per wall-clock second, keyed by ts_floor. Its
# declared availability instant is ts_floor + 1s.
agg = pd.DataFrame({"ts_floor": secs, "agg_value": rng.standard_normal(N_SECONDS)})

# The decision frame: rows stamped INSIDE each second, never at its end -- which
# is the condition under which the aggregate is unavailable.
stamps, offs = [], []
for s in secs:
    for k in range(ROWS_PER_SECOND):
        stamps.append(s + pd.Timedelta(milliseconds=200 + 250 * k))
        offs.append(k)
snap = pd.DataFrame({"timestamp": stamps, "own": rng.standard_normal(len(stamps))})

RAW = {"snap": snap, "agg": agg}
MODEL = AvailabilityModel(aggregate_frames={"agg": "ts_floor"},
                          decision_column="timestamp")


def _merge(raw, shift_seconds):
    """Attach each row the aggregate of second (its own second - shift)."""
    snap_, agg_ = raw["snap"], raw["agg"]
    out = snap_.copy()
    out["ts_floor"] = pd.to_datetime(out["timestamp"]).dt.floor("s")
    key = out["ts_floor"] - pd.Timedelta(seconds=shift_seconds)
    m = agg_.set_index("ts_floor")["agg_value"]
    out["feature"] = key.map(m).to_numpy()
    return out[["timestamp", "own", "feature"]]


def build_leaky(raw):
    """READS ITS OWN SECOND. The aggregate completes at F+1s; the decision
    instant is inside F. Unavailable."""
    return _merge(raw, 0)


def build_clean(raw):
    """READS THE PREVIOUS SECOND. Its instant is F, the decision instant >= F.
    Available under the locked tie rule."""
    return _merge(raw, 1)


def report(name, res, expect_fire):
    infd = sum(c.moved_in_second for c in res.cohorts)
    nxt = sum(c.moved_next_second for c in res.cohorts)
    fired = bool(res.findings)
    ok = (fired == expect_fire)
    print("  %-9s verdict=%-20s in-second moved=%-6d next-second moved=%-6d  %s"
          % (name, res.verdict(), infd, nxt, "OK" if ok else "** MISMATCH **"))
    for n in res.notes:
        print("            note: %s" % n)
    return ok, infd, nxt


print("Probe A controls -- %d seconds, %d rows/second, seed %d"
      % (N_SECONDS, ROWS_PER_SECOND, SEED))
print()

pos = run_probe_a(RAW, build_leaky, MODEL, side="control-positive")
neg = run_probe_a(RAW, build_clean, MODEL, side="control-negative")

ok_p, p_in, p_next = report("POSITIVE", pos, True)
ok_n, n_in, n_next = report("NEGATIVE", neg, False)

print()
print("=== VERDICT ===")
print("  positive fires IN-SECOND        : %s" % ("YES" if p_in > 0 else "** NO **"))
print("  negative silent IN-SECOND       : %s" % ("YES" if n_in == 0 else "** NO **"))
# THE LIVENESS CHECK. Without it, a negative that silently never reached the
# build would read as a clean pass.
print("  negative MOVED the next second  : %s  <- proves the corruption landed"
      % ("YES" if n_next > 0 else "** NO -- the silence is vacuous **"))

good = ok_p and ok_n and p_in > 0 and n_in == 0 and n_next > 0
print()
if good:
    print("CONTROLS HOLD. The probe fires on a cell the model marks unavailable, "
          "stays silent on an available one, and the silence is not vacuous.")
else:
    print("** CONTROLS DO NOT HOLD -- R151 §6 makes this a HALT. Probe A is not "
          "pointed at the fixture. **")
sys.exit(0 if good else 1)
