"""W2b step 2, leakage-buster -- THE CONTROL, with the label mapping made explicit.

NO VENDOR FIXTURE. leakage-buster ships no example leakage frame and no clean
counterpart, so both limbs are constructed here. R144 §4 requires that difference
be recorded: a negative we wrote ourselves is weaker evidence than a vendor's,
because we chose what "clean" means.

THE LABEL MAPPING IS THE WHOLE DIFFICULTY, AND IT IS RECORDED RATHER THAN
ASSUMED. `audit` returns risks on a CLEAN frame too -- two of them, "KFold
leakage risk (use GroupKFold)" and "CV strategy recommendation", both
medium/low. They are ADVISORY: they describe how one ought to cross-validate,
not a leak that exists in the data. So:

    ANY risk == fired      -> the clean frame "fires", the tool is declared
                              non-discriminating, and a working instrument is
                              written off. WRONG.
    HIGH severity == fired -> separates cleanly. This is the mapping used.

That distinction is not cosmetic. Mapping every advisory to a leakage finding
would also mean that in the real run a frame with no leak reports leakage, and
`could_not_run` -> `covered_with_exclusion` reasoning would be applied to a
result that is not a finding at all.

THE DETAIL STRINGS ARE IN CHINESE. Recorded because a label mapping that keys on
English substrings would silently match nothing here -- an empty match set reads
as "no leakage", which is exactly the never-fired-reads-as-clean failure.
Severity keys are ASCII (`high`/`medium`/`low`) and are what this control uses.

    usage: control_leakage_buster.py
"""
from __future__ import annotations

import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

import pandas as pd
import leakage_buster
import leakage_buster.api as api

OUT = pathlib.Path(__file__).resolve().parent / "control_leakage_buster_result.json"
N = 300

base = pd.DataFrame({
    "feat_a": [(i * 7) % 13 for i in range(N)],
    "feat_b": [(i * 3) % 5 for i in range(N)],
    "y": [i % 2 for i in range(N)],
})
leaky = base.copy()
leaky["target_copy"] = leaky["y"]          # a column that IS the target
clean = base.copy()

print("leakage-buster %s  |  vendor fixture: NONE -- both limbs constructed here"
      % getattr(leakage_buster, "__version__", "?"))
print()


def risks_of(result):
    """The risk list, with the shape resolved EXPLICITLY.

    An unrecognised shape RAISES rather than returning [] -- an empty list here
    reads as 'clean', and a silently-empty result is how the leakfence adapter
    turned a live detection into a non-firing tool.
    """
    data = getattr(result, "data", None)
    if not isinstance(data, dict):
        raise TypeError("AuditResult.data is %s, not a dict -- refusing to read "
                        "it as 'no risks'" % type(data).__name__)
    risks = data.get("risks")
    if risks is None:
        raise KeyError("AuditResult.data has no 'risks' key: %s" % list(data))
    if not isinstance(risks, list):
        raise TypeError("'risks' is %s, not a list" % type(risks).__name__)
    return risks


results = {}


def limb(label, df, expect_fire, why):
    risks = risks_of(api.audit(df, target="y"))
    high = [r for r in risks if str(r.get("severity", "")).lower() == "high"]
    other = [r for r in risks if r not in high]
    fired = bool(high)
    ok = fired == expect_fire
    print("  %-9s risks=%d  high=%d  fired=%-5s expected=%-5s  %s"
          % (label, len(risks), len(high), fired, expect_fire,
             "OK" if ok else "** MISMATCH **"))
    print("        %s" % why)
    for r in high:
        cols = r.get("evidence", {})
        print("        HIGH    %-38s %s" % (r.get("name", "?"), repr(cols)[:60]))
    for r in other:
        print("        %-7s %s" % (str(r.get("severity", "?")).upper(),
                                   r.get("name", "?")[:64]))
    results[label] = {"n_risks": len(risks), "n_high": len(high),
                      "fired": fired, "expected": expect_fire, "ok": ok,
                      "high_names": [r.get("name") for r in high],
                      "other_names": [r.get("name") for r in other]}
    return ok


pos = limb("POSITIVE", leaky, True,
           "a column identical to the target -- the leak the tool exists to find")
print()
neg = limb("NEGATIVE", clean, False,
           "the same frame without that column; the advisories below are NOT leaks")
print()

verdict = "DISCRIMINATING" if (pos and neg) else "NOT ESTABLISHED"
print("=== VERDICT ===")
print("  POSITIVE limb (target copy must fire) : %s" % ("FIRES" if pos else "** DID NOT FIRE **"))
print("  NEGATIVE limb (clean must stay silent): %s" % ("SILENT" if neg else "** ALSO FIRES **"))
print()
if verdict == "DISCRIMINATING":
    print("RESULT: DISCRIMINATING on HIGH severity. leakage-buster's "
          "acceptance-fixture result is interpretable, PROVIDED the mapping keys "
          "on severity: the clean frame still returns %d advisory risk(s), and "
          "treating those as leakage findings would make every frame positive."
          % results["NEGATIVE"]["n_risks"])
else:
    print("RESULT: NOT ESTABLISHED. leakage-buster's acceptance-fixture result is "
          "`uninterpretable`, NOT a null.")

OUT.write_text(json.dumps({
    "tool": "leakage-buster", "version": getattr(leakage_buster, "__version__", "1.0.2"),
    "vendor_fixture": False, "vendor_negative": False,
    "label_mapping": "severity == 'high' is a leakage finding; medium/low are "
                     "advisory (CV strategy). detail strings are Chinese; "
                     "severity keys are ASCII.",
    "limbs": results, "verdict": verdict,
}, indent=2), encoding="utf-8")
print("\nwritten: %s" % OUT.name)
sys.exit(0 if verdict == "DISCRIMINATING" else 1)
