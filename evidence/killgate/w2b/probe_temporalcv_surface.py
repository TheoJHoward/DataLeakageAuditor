"""W2b step 2, temporalcv -- read the gates' ACTUAL comparison direction. READ-ONLY.

W2b defect #7 records that k6 fed `gate_suspicious_improvement` an ACCURACY where
the formula expects an ERROR metric, so a mapped gate silently never fired and the
null was read as "no leakage found". R142 §1.3 requires the gate be fed an error
metric AND BE OBSERVED FIRING.

Getting that right means reading the direction out of the SOURCE, not out of the
parameter names. A parameter called `baseline` and one called `candidate` tell you
nothing about which way the inequality runs, and guessing wrong reproduces defect
#7 in the other direction -- a gate that fires on everything, which looks like a
working instrument and is not.

    usage: probe_temporalcv_surface.py
"""
from __future__ import annotations

import inspect
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

import temporalcv
from temporalcv import gates

print("temporalcv %s" % getattr(temporalcv, "__version__", "?"))
print("gates module: %s" % gates.__file__)
print()

print("=== callables in temporalcv.gates ===")
for n in sorted(d for d in dir(gates) if not d.startswith("_")):
    o = getattr(gates, n)
    if not callable(o):
        continue
    try:
        print("  %-34s %s" % (n, str(inspect.signature(o))[:90]))
    except (TypeError, ValueError):
        print("  %-34s (signature unavailable)" % n)

print()
for fn in ("gate_suspicious_improvement", "gate_signal_verification",
           "gate_residual_diagnostics"):
    f = getattr(gates, fn, None)
    if f is None:
        print("=== %s ABSENT ===" % fn)
        continue
    print("=" * 78)
    print("=== SOURCE: %s ===" % fn)
    try:
        print(inspect.getsource(f))
    except (OSError, TypeError) as e:
        print("  source unavailable: %s" % e)
