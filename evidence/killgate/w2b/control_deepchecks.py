"""W2b step 2, deepchecks -- THE CONTROL, two pairs, plus the AGPL determination.

TWO PAIRS, because deepchecks is a suite of independent checks and a tool can be
alive on one and dead on another:

  PAIR 1  IndexTrainTestLeakage     positive: index values shared across the split
                                    negative: disjoint indices
  PAIR 2  FeatureLabelCorrelation   positive: a feature that IS the label
                                    negative: features independent of it

NO VENDOR FIXTURE PAIR. deepchecks ships datasets, but not a matched
leaky/clean pair for these checks, so both limbs are constructed here. Recorded
per R144 §4, as for leakfence, leakage-buster and leak-detect -- only Leakly
supplied a vendor pair.

THE SHAPE OF THE ANSWER IS RESOLVED EXPLICITLY. Three adapter defects earlier in
this sweep -- a tuple read as an object, a bool `False` read as an absence, a
vendor default that crashed -- each produced a plausible, wrong finding about
someone else's software. `CheckResult.value` is read by type, and an
unrecognised shape RAISES rather than scoring as "no leakage", because an empty
result reads as clean and that is the failure this whole exercise exists to
prevent.

    usage: control_deepchecks.py
"""
from __future__ import annotations

import json
import pathlib
import sys
import warnings

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

warnings.filterwarnings("ignore")

import importlib.metadata as md
import pandas as pd
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import FeatureLabelCorrelation, IndexTrainTestLeakage

OUT = pathlib.Path(__file__).resolve().parent / "control_deepchecks_result.json"
N = 200

meta = md.metadata("deepchecks")
licence = next((c for c in (meta.get_all("Classifier") or []) if "License" in c),
               "(no licence classifier)")
print("deepchecks %s" % meta.get("Version"))
print("  licence classifier: %s" % licence)
print("  License field     : %s  <- unset; the classifier is the authority"
      % meta.get("License"))
print("  vendor fixture pair: NONE -- both limbs constructed here")
print()

results = {}


def scalar(value, label):
    """A comparable magnitude from CheckResult.value, resolved BY TYPE.

    Raises on an unrecognised shape. Returning 0.0 for "I don't know how to read
    this" would score every unknown as clean.
    """
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        nums = [v for v in value.values() if isinstance(v, (int, float))]
        return float(max(nums)) if nums else 0.0
    if isinstance(value, pd.Series):
        return float(value.max()) if len(value) else 0.0
    if hasattr(value, "__len__"):
        return float(len(value))
    raise TypeError("%s: CheckResult.value is %s -- refusing to read it as "
                    "'no leakage'" % (label, type(value).__name__))


def limb(pair, label, check, train, test, expect_fire, why, threshold=0.0):
    try:
        r = check.run(train_dataset=train, test_dataset=test)
        v = scalar(r.value, label)
        err = None
    except Exception as e:                              # noqa: BLE001
        print("  %-6s %-9s ** RAISED %s: %s **"
              % (pair, label, type(e).__name__, str(e)[:70]))
        results["%s/%s" % (pair, label)] = {"error": "%s: %s" % (type(e).__name__, e)}
        return False
    fired = v > threshold
    ok = fired == expect_fire
    print("  %-6s %-9s value=%-8.4f fired=%-5s expected=%-5s  %s"
          % (pair, label, v, fired, expect_fire, "OK" if ok else "** MISMATCH **"))
    print("         %s" % why)
    results["%s/%s" % (pair, label)] = {"value": v, "fired": fired,
                                        "expected": expect_fire, "ok": ok,
                                        "raw_type": type(r.value).__name__}
    return ok


# --- PAIR 1: IndexTrainTestLeakage -----------------------------------------
common = {"feat_a": [float((i * 7) % 13) for i in range(N)],
          "y": [i % 2 for i in range(N)]}
tr = pd.DataFrame(dict(common, idx=list(range(N))))
te_leak = pd.DataFrame(dict(common, idx=list(range(N))))          # same indices
te_clean = pd.DataFrame(dict(common, idx=list(range(N, 2 * N))))  # disjoint

d_tr = Dataset(tr, label="y", index_name="idx")
p1a = limb("index", "POSITIVE", IndexTrainTestLeakage(), d_tr,
           Dataset(te_leak, label="y", index_name="idx"), True,
           "every test index also appears in train")
p1b = limb("index", "NEGATIVE", IndexTrainTestLeakage(), d_tr,
           Dataset(te_clean, label="y", index_name="idx"), False,
           "test indices are disjoint from train")
print()

# --- PAIR 2: FeatureLabelCorrelation ---------------------------------------
lk = pd.DataFrame({"feat_a": [float((i * 7) % 13) for i in range(N)],
                   "leaky": [float(i % 2) for i in range(N)],
                   "y": [i % 2 for i in range(N)]})
cl = lk.drop(columns=["leaky"])
def single_limb(pair, label, check, ds, expect_fire, why, threshold=0.5):
    """FeatureLabelCorrelation is a SingleDatasetCheck.

    It takes `dataset=`, not `train_dataset=`/`test_dataset=`. Calling it the
    train/test way raises TypeError, and the first run of this control scored
    that as "the positive did not fire" -- the FOURTH time in this sweep that my
    own call, not the tool, produced the negative result. A raise is never
    evidence about a tool; it is evidence the call did not happen.
    """
    try:
        r = check.run(dataset=ds)
        v = scalar(r.value, label)
        err = None
    except Exception as e:                              # noqa: BLE001
        print("  %-6s %-9s ** RAISED %s: %s **"
              % (pair, label, type(e).__name__, str(e)[:70]))
        results["%s/%s" % (pair, label)] = {"error": "%s: %s" % (type(e).__name__, e)}
        return False
    fired = v > threshold
    ok = fired == expect_fire
    print("  %-6s %-9s value=%-8.4f fired=%-5s expected=%-5s  %s"
          % (pair, label, v, fired, expect_fire, "OK" if ok else "** MISMATCH **"))
    print("         %s" % why)
    results["%s/%s" % (pair, label)] = {"value": v, "fired": fired,
                                        "expected": expect_fire, "ok": ok,
                                        "raw_type": type(r.value).__name__}
    return ok


p2a = single_limb("corr", "POSITIVE", FeatureLabelCorrelation(),
                  Dataset(lk, label="y"), True, "column 'leaky' IS the label")
p2b = single_limb("corr", "NEGATIVE", FeatureLabelCorrelation(),
                  Dataset(cl, label="y"), False,
                  "that column removed; feat_a carries no label information")
print()

pairs = {"IndexTrainTestLeakage": (p1a, p1b), "FeatureLabelCorrelation": (p2a, p2b)}
print("=== VERDICT ===")
alive = []
for name, (pos, neg) in pairs.items():
    state = ("DISCRIMINATING" if pos and neg
             else "NOT ESTABLISHED (positive did not fire)" if not pos
             else "NOT ESTABLISHED (fires on the clean case too)")
    print("  %-26s %s" % (name, state))
    alive.append(pos and neg)

verdict = "DISCRIMINATING" if all(alive) else "NOT ESTABLISHED"
print()
print("=== AGPL-3.0-or-later DETERMINATION ===")
print("  deepchecks is AGPLv3+ (classifier above). It is INVOKED AS A SEPARATE")
print("  PROGRAM in its own virtualenv; no deepchecks source is copied into this")
print("  repository, none is modified, and nothing is redistributed. The project")
print("  reads its printed results as data. INTEROPERATION IS NOT VENDORING, and")
print("  AGPL §13's network clause is not engaged because nothing here offers")
print("  deepchecks to users over a network. RECORDED, not assumed: if a later")
print("  round vendors, modifies or redistributes it, this determination lapses")
print("  and must be redone.")
print()
if verdict == "DISCRIMINATING":
    print("RESULT: DISCRIMINATING on both checks. deepchecks' acceptance-fixture "
          "result is interpretable.")
else:
    print("RESULT: NOT ESTABLISHED. deepchecks' acceptance-fixture result is "
          "`uninterpretable`, NOT a null.")

OUT.write_text(json.dumps({
    "tool": "deepchecks", "version": meta.get("Version"),
    "licence_classifier": licence, "license_field": meta.get("License"),
    "licence_determination": "AGPL-3.0-or-later. Invoked as a separate program "
                             "in its own venv; not vendored, modified or "
                             "redistributed; §13 network clause not engaged. "
                             "Lapses if any of those change.",
    "vendor_fixture": False, "vendor_negative": False,
    "limbs": results, "verdict": verdict,
}, indent=2), encoding="utf-8")
print("\nwritten: %s" % OUT.name)
sys.exit(0 if verdict == "DISCRIMINATING" else 1)
