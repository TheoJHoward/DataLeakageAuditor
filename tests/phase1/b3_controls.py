"""B-3 -- controls through the FINAL adapter path. R149 §1.2 / §2.2.

Step 2's controls each called their tool directly, from their own script. Three
adapters in `b2_run_one.py` were then REBUILT -- complete-case filtering for
leakage-buster, a subject and a degenerate-subject guard for leakfence, a
Ridge-vs-persistence comparison for temporalcv. **So the controls no longer test
what the measurement does**, and a control that does not exercise the
measurement's path has not tested the measurement.

THIS SCRIPT WRITES A POSITIVE AND A NEGATIVE FRAME AND RUNS THEM THROUGH
`b2_run_one.py` ITSELF -- the same CLI, the same adapters, the same CSV
transport and dtype sidecar the fixture rows used. Nothing here calls a tool
directly.

THE PAIR, and why one pair serves four tools:

  POSITIVE  `leak` is EXACTLY the target -> every tool's mechanism has something
            to find: a target-correlated column (leakage-buster, deepchecks), a
            perfectly predictable target (temporalcv), and -- separately --
            duplicated rows spanning the split plus a repeated `ts_floor` group
            on both sides (leakfence's two checks).
  NEGATIVE  the same shape with `leak` replaced by noise, no duplicated rows,
            and `ts_floor` groups kept disjoint across the cut.

The frames are built with an EXPLICIT SEED. `hash()` is salted on `str` by
PYTHONHASHSEED and would make these unreproducible across processes.

    usage: b3_controls.py <outdir>
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
N, SEED = 6000, 20260828
TARGET = "fwd_move_ticks_5s"          # the real run's name, so the adapter's
                                      # sibling-exclusion logic behaves the same
rng = np.random.default_rng(SEED)


PHI = 0.79            # the acceptance fixture's own lag-1 autocorrelation


def ar1(n, phi=PHI):
    """An AR(1) target, because A CONTROL MUST BE DRAWN FROM THE REGIME THE
    MEASUREMENT OPERATES IN.

    The first negative control used iid noise, and temporalcv HALTed on it --
    correctly, arithmetically, and with no leakage present: for an iid series the
    mean predictor beats persistence by ~29%, past the gate's 20% threshold. That
    was a defect in the CONTROL, not the adapter. The acceptance fixture's target
    has lag-1 autocorrelation 0.794, where persistence is a strong baseline and
    the gate is in its intended regime, so the control is built at phi = 0.79.
    """
    e = rng.standard_normal(n)
    y = np.empty(n)
    y[0] = e[0]
    for i in range(1, n):
        y[i] = phi * y[i - 1] + e[i]
    return y


def base(n):
    t = pd.date_range("2026-01-01", periods=n, freq="1s")
    return pd.DataFrame({
        "timestamp": t,
        "feat_a": rng.standard_normal(n),
        "feat_b": rng.standard_normal(n),
        "feat_c": rng.integers(0, 7, n).astype(float),
        TARGET: ar1(n),
    })


# --- POSITIVE --------------------------------------------------------------
pos = base(N)
pos["leak"] = pos[TARGET]                       # the leak: a copy of the target
# A REPEATED GROUP THAT SPANS THE 80/20 CUT, so leakfence's group check both
# ARMS (not one-group-per-row) and has something to find.
cut = int(N * 0.8)
grp = np.arange(N) // 10
grp[cut:cut + 40] = grp[cut - 40:cut]           # the same buckets on both sides
pos["ts_floor"] = pd.to_datetime("2026-01-01") + pd.to_timedelta(grp, unit="s")
# EXACT ROW DUPLICATES spanning the cut, for check_duplicates.
pos.iloc[cut:cut + 25] = pos.iloc[0:25].values

# --- NEGATIVE --------------------------------------------------------------
neg = base(N)
neg["leak"] = rng.standard_normal(N)            # noise, not the target
g2 = np.arange(N) // 10                          # groups strictly increasing:
neg["ts_floor"] = pd.to_datetime("2026-01-01") + pd.to_timedelta(g2, unit="s")
# no duplicated rows, and no group straddles the cut

for name, d in (("positive", pos), ("negative", neg)):
    assert d.isna().sum().sum() == 0, "control frames must carry no NaN"
    p = OUT / ("b3_%s.csv" % name)
    d.to_csv(p, index=False)
    (OUT / ("b3_%s.dtypes.json" % name)).write_text(
        json.dumps({"datetime_columns": ["timestamp", "ts_floor"],
                    "all": {c: str(d[c].dtype) for c in d.columns}}, indent=2),
        encoding="utf-8")
    ug = d["ts_floor"].nunique()
    print("%-9s %d x %d | ts_floor groups %d (%.1f rows each) | exact dup rows %d"
          % (name, d.shape[0], d.shape[1], ug, len(d) / ug, d.duplicated().sum()))

print()
print("corr(leak, target): positive %.3f | negative %.3f"
      % (pos["leak"].corr(pos[TARGET]), neg["leak"].corr(neg[TARGET])))
print("written to %s" % OUT)
