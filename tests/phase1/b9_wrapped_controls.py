"""B-9 controls THROUGH THE WRAPPED PATH. R153 §4/§6.

R153 §6 makes a control failing through the wrapped path a HALT. The control must
exercise the path the measurement takes, and the measurement now ends at
`resolve_state_pair` -- so the controls must too, not merely at the probe.

Reuses the same synthetic pair as B-6: a builder reading its OWN second
(unavailable) and one reading the PREVIOUS second (available).

    usage: b9_wrapped_controls.py
"""
from __future__ import annotations

import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[2]
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                        # noqa: BLE001
    pass

import numpy as np                                       # noqa: E402
import pandas as pd                                      # noqa: E402

from leakaudit.availability import AvailabilityModel, run_probe_a   # noqa: E402
from leakaudit.availability_trace import resolve_all, traces_for    # noqa: E402

N_SECONDS, ROWS_PER_SECOND, SEED = 4000, 3, 20260828
rng = np.random.default_rng(SEED)
secs = pd.date_range("2026-01-01", periods=N_SECONDS, freq="1s")
agg = pd.DataFrame({"ts_floor": secs, "agg_value": rng.standard_normal(N_SECONDS)})
stamps = [s + pd.Timedelta(milliseconds=200 + 250 * k)
          for s in secs for k in range(ROWS_PER_SECOND)]
snap = pd.DataFrame({"timestamp": stamps, "own": rng.standard_normal(len(stamps))})
RAW = {"snap": snap, "agg": agg}
MODEL = AvailabilityModel(aggregate_frames={"agg": "ts_floor"})


def _merge(raw, shift):
    out = raw["snap"].copy()
    out["ts_floor"] = pd.to_datetime(out["timestamp"]).dt.floor("s")
    key = out["ts_floor"] - pd.Timedelta(seconds=shift)
    out["feature"] = key.map(raw["agg"].set_index("ts_floor")["agg_value"]).to_numpy()
    return out[["timestamp", "own", "feature"]]


build_leaky = lambda raw: _merge(raw, 0)     # noqa: E731 -- reads its OWN second
build_clean = lambda raw: _merge(raw, 1)     # noqa: E731 -- reads the PREVIOUS

print("B-9 controls, through the wrapped path (probe -> traces -> registered resolvers)")
print()

ok = True
for label, build, want in (("POSITIVE", build_leaky, "finding"),
                           ("NEGATIVE", build_clean, "observed_silence")):
    res = run_probe_a(RAW, build, MODEL, side="control-" + label.lower())
    # EVERY probed second here HAS an aggregate row, so all are eligible.
    eligible = [c.second for c in res.cohorts]
    resolved = resolve_all(traces_for(res, eligible, case_id="control_" + label.lower()))
    pres = [r for r in resolved if r["promotion_status"] == "preserving"][0]
    prom = [r for r in resolved if r["promotion_status"] == "promoted"][0]
    good = pres["evidence_outcome"] == want
    ok &= good
    print("  %-9s preserving: %-14s x %-18s cohorts=%-4d findings=%-4d  %s"
          % (label, pres["schedule_state"], pres["evidence_outcome"],
             pres["n_cohorts"], pres["n_findings"],
             "OK" if good else "** EXPECTED %s **" % want))
    print("            promoted  : %-14s x %-18s (no strategy resolves to it)"
          % (prom["schedule_state"], prom["evidence_outcome"]))

print()
print("Every trace above was accepted by `resolve_state_pair` UNMODIFIED -- an "
      "illegal pair or a malformed trace raises, and none did.")
print()
if ok:
    print("WRAPPED CONTROLS HOLD.")
else:
    print("** WRAPPED CONTROLS DO NOT HOLD -- R153 §6 makes this a HALT. **")
sys.exit(0 if ok else 1)
