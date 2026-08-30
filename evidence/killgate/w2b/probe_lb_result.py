"""W2b step 2 -- what shape does leakage_buster's audit actually return? READ-ONLY.

The leakfence control recorded a live detection as a non-firing tool because the
adapter read `.violations` off a plain tuple. That was a finding about MY CALL
written down as a finding about the TOOL. The lesson generalises: read the
result's shape before writing the control that interprets it.

    usage: probe_lb_result.py
"""
from __future__ import annotations

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

import pandas as pd
import leakage_buster.api as api

n = 300
rng = pd.Series(range(n))
leaky = pd.DataFrame({
    "feat_a": [(i * 7) % 13 for i in range(n)],
    "feat_b": [(i * 3) % 5 for i in range(n)],
    "y": [i % 2 for i in range(n)],
})
leaky["target_copy"] = leaky["y"]          # a column that IS the target

clean = leaky.drop(columns=["target_copy"])

for name, df in (("LEAKY (target_copy == y)", leaky), ("CLEAN", clean)):
    print("=" * 74)
    print("=== %s -- columns %s ===" % (name, list(df.columns)))
    try:
        r = api.audit(df, target="y")
    except Exception as e:                              # noqa: BLE001
        print("  RAISED %s: %s" % (type(e).__name__, e))
        continue
    print("  type: %s" % type(r).__name__)
    data = getattr(r, "data", None)
    print("  .data type: %s" % type(data).__name__)
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, list):
                print("    %-20s list, %d item(s)" % (k, len(v)))
                for item in v[:4]:
                    print("        %s" % repr(item)[:150])
            else:
                print("    %-20s %s" % (k, repr(v)[:110]))
    meta = getattr(r, "meta", None)
    if isinstance(meta, dict):
        print("  .meta keys: %s" % list(meta.keys())[:12])
