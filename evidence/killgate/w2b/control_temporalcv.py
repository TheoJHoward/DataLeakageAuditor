"""W2b step 2, temporalcv -- THE CONTROL, and a reproduction of defect #7.

R142 §1.3 requires `gate_suspicious_improvement` be fed an ERROR metric, not an
accuracy, AND BE OBSERVED FIRING. Both halves matter: k6 fed it an accuracy, the
gate silently never fired, and the null was read as "no leakage found".

THE DIRECTION IS READ OUT OF THE SOURCE, NOT GUESSED FROM PARAMETER NAMES:

    improvement = 1 - (model_metric / baseline_metric)      # HALT if > threshold

and the docstring pins the units -- "model_metric : Model's error metric (lower
is better)". So a model that halves the error scores +0.50 and HALTs.

THREE LIMBS, AND THE THIRD IS THE POINT:

  POSITIVE  a genuinely leaky forecaster, fed as MAE          -> must HALT
  NEGATIVE  an honest forecaster, fed as MAE                  -> must PASS
  DEFECT-7  THE SAME leaky scenario, fed as ACCURACY as k6 fed
            it                                                -> observed NOT to fire

The third limb is not decoration. A control that only shows the gate CAN fire
would have passed at k6 too; what k6 needed was evidence that the way it was
being CALLED made it unable to fire. Reproducing that is the difference between
knowing the gate works and knowing the run was valid.

THE SERIES USES phi = 0.95, the vendor's own `gate_synthetic_ar1` default. That
is deliberate: at phi near 1 persistence is nearly optimal, so an HONEST model
beats it only slightly and the negative limb is a real test. At phi = 0.7 an
honest AR(1) model beats persistence by more than 20% and would HALT -- the
negative limb would fail for a reason that has nothing to do with leakage.

    usage: control_temporalcv.py
"""
from __future__ import annotations

import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

import numpy as np
import temporalcv
from temporalcv.gates import GateStatus, gate_suspicious_improvement

OUT = pathlib.Path(__file__).resolve().parent / "control_temporalcv_result.json"
PHI, N, SEED = 0.95, 4000, 20260826       # explicit seed, never hash()

rng = np.random.default_rng(SEED)
eps = rng.standard_normal(N)
y = np.empty(N)
y[0] = eps[0]
for t in range(1, N):
    y[t] = PHI * y[t - 1] + eps[t]

target = y[1:]                 # what is forecast
prev = y[:-1]                  # what is known at forecast time

mae = lambda a, b: float(np.mean(np.abs(np.asarray(a) - np.asarray(b))))

# BASELINE: persistence. yhat[t] = y[t-1].
baseline_mae = mae(target, prev)

# HONEST: the AR(1) one-step forecast, phi estimated from the FIRST HALF only so
# the coefficient is not fitted on the window it scores.
half = len(prev) // 2
phi_hat = float(np.dot(prev[:half], target[:half]) / np.dot(prev[:half], prev[:half]))
honest_mae = mae(target[half:], phi_hat * prev[half:])
baseline_mae_test = mae(target[half:], prev[half:])

# LEAKY: the forecaster peeks at the value it is forecasting. This is the defect
# the gate exists to catch, produced rather than asserted.
leaky_mae = mae(target[half:], 0.98 * target[half:] + 0.02 * prev[half:])

print("temporalcv %s | AR(1) phi=%.2f, n=%d, seed=%d"
      % (getattr(temporalcv, "__version__", "?"), PHI, N, SEED))
print("  phi estimated on the first half only: %.4f" % phi_hat)
print("  persistence MAE (test half) : %.4f" % baseline_mae_test)
print("  honest  MAE (test half)     : %.4f" % honest_mae)
print("  leaky   MAE (test half)     : %.4f" % leaky_mae)
print()

results = {}


def limb(label, model_metric, baseline_metric, metric_name, expect, why):
    r = gate_suspicious_improvement(model_metric, baseline_metric,
                                    metric_name=metric_name)
    got = r.status.name if isinstance(r.status, GateStatus) else str(r.status)
    ratio = r.details.get("improvement_ratio")
    ok = (got == expect)
    print("%-9s %-8s model=%.4f baseline=%.4f -> improvement %+.3f -> %s  %s"
          % (label, metric_name, model_metric, baseline_metric,
             ratio if ratio is not None else float("nan"), got,
             "OK" if ok else "** EXPECTED %s **" % expect))
    print("            %s" % why)
    print("            gate said: %s" % r.message)
    results[label] = {"status": got, "expected": expect, "ok": ok,
                      "improvement_ratio": ratio, "message": r.message,
                      "model_metric": model_metric,
                      "baseline_metric": baseline_metric,
                      "metric_name": metric_name}
    return ok


pos = limb("POSITIVE", leaky_mae, baseline_mae_test, "MAE", "HALT",
           "a forecaster that peeks at its own target; the gate must catch it")
print()
neg = limb("NEGATIVE", honest_mae, baseline_mae_test, "MAE", "PASS",
           "an honest AR(1) fitted out-of-sample; near phi=1 it beats "
           "persistence only slightly")
print()

# DEFECT #7, REPRODUCED. The same leaky model, expressed the way k6 expressed it:
# as an accuracy-style score where HIGHER IS BETTER. The gate's own formula then
# reads the strong model as having a WORSE metric and reports no improvement.
leaky_acc, baseline_acc = 0.97, 0.55
d7 = limb("DEFECT-7", leaky_acc, baseline_acc, "accuracy", "PASS",
          "THE SAME LEAKAGE, fed as accuracy as k6 fed it -- higher-is-better "
          "inverts the ratio, so the gate cannot fire")
print()

print("=== VERDICT ===")
print("  POSITIVE limb (leaky must HALT)      : %s"
      % ("FIRES" if pos else "** DID NOT FIRE **"))
print("  NEGATIVE limb (honest must PASS)     : %s"
      % ("SILENT" if neg else "** ALSO FIRES **"))
print("  DEFECT-7 limb (accuracy cannot fire) : %s"
      % ("REPRODUCED" if d7 else "** did not reproduce **"))

verdict = "DISCRIMINATING" if (pos and neg) else "NOT ESTABLISHED"
print()
if verdict == "DISCRIMINATING":
    print("RESULT: DISCRIMINATING when fed an ERROR metric. The gate HALTs on a "
          "peeking forecaster and passes an honest one.")
else:
    print("RESULT: NOT ESTABLISHED. temporalcv's acceptance-fixture result is "
          "`uninterpretable`, NOT a null.")
if d7:
    print("AND: defect #7 is REPRODUCED. Fed the identical leakage as an accuracy, "
          "the gate returns %s with improvement %+.3f -- k6's null was an unfired "
          "instrument, not a clean result."
          % (results["DEFECT-7"]["status"],
             results["DEFECT-7"]["improvement_ratio"]))

OUT.write_text(json.dumps({
    "tool": "temporalcv", "version": getattr(temporalcv, "__version__", "2.3.0"),
    "phi": PHI, "n": N, "seed": SEED, "phi_hat": phi_hat,
    "baseline_mae_test": baseline_mae_test, "honest_mae": honest_mae,
    "leaky_mae": leaky_mae, "limbs": results, "verdict": verdict,
    "defect7_reproduced": d7,
}, indent=2), encoding="utf-8")
print("\nwritten: %s" % OUT.name)
sys.exit(0 if verdict == "DISCRIMINATING" else 1)
