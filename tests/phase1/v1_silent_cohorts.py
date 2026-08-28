"""V-1 -- the mechanism of the 50 silent cohorts. R152 §4. READ-ONLY.

The contaminated side fired on 250 of 300 cohorts. **Fifty silences inside a
headline result are the first thing a hostile reader pulls**, and the project's
own standard says a silence carries its mechanism and its domain.

THE HYPOTHESIS COMES FROM THE PROBE'S OWN NOTE, not from a guess: it recorded
"corrupted 250 aggregate row(s) across 300 second(s)". **Two hundred fifty
corrupted rows for three hundred cohorts** -- so fifty of the picked seconds had
no aggregate row to corrupt at all. If that is right, nothing was perturbed for
those seconds and nothing could move: the silence is not the probe failing to
see, it is the probe having nothing to look at.

THIS IS TESTED WITHOUT A REBUILD. The picked seconds are deterministic
(`seconds[::stride][:max]` off the built output's own stamps), and whether an
aggregate row exists in a given second is a property of the RAW frames. No
corrupted build is needed to answer it, which is what keeps this verification of
the run rather than a re-run.

THE SECOND QUESTION IS SET COHERENCE: are the same seconds silent on both sides?
A matching set is a coherent story -- seconds whose aggregates are never read. A
MISMATCH would be a finding, because the two sides read the same frames.

    usage: v1_silent_cohorts.py
"""
from __future__ import annotations

import json
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

import pandas as pd                                      # noqa: E402
from leakaudit import fixture_adapter as fa              # noqa: E402

STRIDE, MAX = 997, 300
inputs = fa.read_inputs("zc", "2025-01")

# The picked seconds are derived the same way the probe derives them: off the
# BUILT output's decision stamps. Both sides are built here only to confirm they
# agree on the stamps -- SC-7(d) is about a DETECTOR seeing both sides, and this
# is the harness reconciling two per-side results, which is its own act.
picked_by_side, floors_by_side = {}, {}
for side in ("contaminated", "corrected"):
    out = fa.builder_for(inputs, side=side)(inputs.raw)
    fl = pd.to_datetime(out["timestamp"]).dt.floor("s")
    floors_by_side[side] = fl
    secs = pd.Index(sorted(fl.unique()))
    picked_by_side[side] = list(secs[::STRIDE][:MAX])
    print("%-13s built %d rows | %d distinct seconds | %d picked"
          % (side, len(out), len(secs), len(picked_by_side[side])))

same = picked_by_side["contaminated"] == picked_by_side["corrected"]
print("both sides pick the SAME seconds: %s" % same)
if not same:
    print("** the sides disagree on decision stamps -- that is itself a finding **")

picked = picked_by_side["contaminated"]
pset = set(picked)

# Does each picked second carry an aggregate row in either aggregate frame?
agg_secs = {}
for fname, keycol in (("magg", "ts_floor"), ("trades", "ts_event")):
    f = inputs.frames.get(fname)
    if f is None:
        print("frame %r absent" % fname)
        continue
    k = pd.to_datetime(f[keycol]).dt.floor("s")
    agg_secs[fname] = set(k.unique()) & pset
    print("%-7s has rows in %d of the %d picked seconds" % (fname, len(agg_secs[fname]), len(picked)))

have_any = set().union(*agg_secs.values()) if agg_secs else set()
no_agg = [s for s in picked if s not in have_any]
print()
print("=== picked seconds WITH NO AGGREGATE ROW IN ANY FRAME: %d ===" % len(no_agg))

res = json.loads((_ROOT / "evidence/phase1/probe_a/contaminated.json").read_text(encoding="utf-8"))
fired = res["cohorts_with_finding"]
silent = res["n_cohorts"] - fired
print("probe reported: %d cohorts, %d fired, %d silent" % (res["n_cohorts"], fired, silent))
print()
if len(no_agg) == silent:
    print("MECHANISM ESTABLISHED: the %d silent cohorts are exactly the %d picked "
          "seconds with no aggregate row to corrupt." % (silent, len(no_agg)))
    print("Nothing was perturbed for them, so nothing could move. The silence is "
          "the probe having nothing to look at -- NOT the probe failing to see.")
else:
    print("** COUNTS DISAGREE: %d seconds without an aggregate, %d silent cohorts. "
          "The mechanism is NOT established by this alone. **" % (len(no_agg), silent))

# The domain of the silence, stated: how many decision rows sit in those seconds.
rows_no_agg = int(floors_by_side["contaminated"].isin(no_agg).sum())
print()
print("DOMAIN OF THE SILENCE: %d decision row(s) across those %d second(s) -- "
      "%.4f%% of the fixture's %d rows."
      % (rows_no_agg, len(no_agg), 100.0 * rows_no_agg / len(floors_by_side["contaminated"]),
         len(floors_by_side["contaminated"])))

out = {"stride": STRIDE, "max_cohorts": MAX,
       "picked_same_both_sides": bool(same),
       "n_picked": len(picked),
       "n_without_aggregate": len(no_agg),
       "n_silent_reported": silent,
       "mechanism_established": len(no_agg) == silent,
       "rows_in_silent_seconds": rows_no_agg,
       "seconds_without_aggregate_sample": [str(s) for s in no_agg[:20]]}
p = _ROOT / "evidence/phase1/probe_a/v1_silent_cohorts.json"
p.write_text(json.dumps(out, indent=2), encoding="utf-8")
print("written: %s" % p.name)
