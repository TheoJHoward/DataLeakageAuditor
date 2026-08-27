"""W2b step 2, leak-detect -- THE CONTROL, and the return value is not the signal.

leak-detect works by NaN propagation: it calls a data-creation function with a
sentinel injected into a source column and asks whether the sentinel reaches an
output feature. That is the same mechanism as our own `nullread` detector.

ITS DOCSTRING SAYS IT "PRINTS OUT" THE LEAKED COLUMNS. So the signal may be
STDOUT rather than a return value -- and an adapter that reads only the return
value would record every run as a null. Both are captured here and BOTH are
reported, so which one carries the answer is established rather than assumed.
This is the leakfence lesson again: the shape of the answer is read before it is
interpreted.

NO VENDOR FIXTURE, and no declared __version__ either (recorded at step 1). Both
limbs are constructed here.

  POSITIVE  the created feature is computed FROM the target column
  NEGATIVE  the created feature is computed only from an input feature

    usage: control_leak_detect.py
"""
from __future__ import annotations

import contextlib
import io
import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

import pandas as pd
import leak_detect

OUT = pathlib.Path(__file__).resolve().parent / "control_leak_detect_result.json"
N = 200

input_data = pd.DataFrame({
    "feat_a": [float((i * 7) % 13) for i in range(N)],
    "feat_b": [float((i * 3) % 5) for i in range(N)],
    "y": [float(i % 2) for i in range(N)],
})


def leaky_creation(df):
    """The created feature is a function of the TARGET -- this is the leak."""
    out = df.copy()
    out["made_feature"] = df["y"] * 2.0 + df["feat_a"] * 0.0
    return out


def clean_creation(df):
    """The created feature is a function of an INPUT FEATURE only."""
    out = df.copy()
    out["made_feature"] = df["feat_a"] * 2.0
    return out


print("leak-detect %s  |  vendor fixture: NONE -- both limbs constructed here"
      % (getattr(leak_detect, "__version__", None) or "(no __version__ declared)"))
print()

results = {}


def limb(label, func, expect_fire, why, only_nan=True):
    """One limb. `only_nan=True` runs the NaN pass alone.

    THE DEFAULT IS only_nan=False, AND IT CRASHES. That mode adds a
    complex-number pass which uses `np.complex`, removed from NumPy in 1.24; the
    installed NumPy is 1.26.4. The first run of this control used the default,
    got a correct NaN result printed to stdout and THEN an AttributeError, and
    scored both limbs as mismatches. That verdict would have been recorded as
    "leak-detect does not discriminate" when what had actually happened is that
    the tool's default mode is broken against a NumPy of this age -- a different
    finding with a different consequence.
    """
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            ret = leak_detect.detect_horizontal_leakage(
                data_creation_func=func,
                input_data=input_data,
                target_cols=["y"],
                output_feature_cols=["made_feature"],
                only_nan=only_nan)
        err = None
    except Exception as e:                              # noqa: BLE001
        ret, err = None, "%s: %s" % (type(e).__name__, e)
    printed = buf.getvalue().strip()

    # WHICH SIGNAL CARRIES THE ANSWER IS ESTABLISHED, NOT ASSUMED -- and the
    # answer turned out to be A BOOL RETURN: True on the leaky frame, False on
    # the clean one.
    #
    # A first version tested `ret is not None and not (len(ret) == 0)`. For
    # `ret = False` that is True -- `False is not None`, and a bool has no
    # `__len__` -- so the NEGATIVE limb scored as FIRING and the tool was about
    # to be recorded as non-discriminating. A RETURNED FALSE IS AN ANSWER, NOT AN
    # ABSENCE, and a truthiness test that cannot tell those apart will always
    # read the clean case as positive.
    #
    # `bool` is checked BEFORE the generic branch because `False` is falsy and
    # would otherwise fall through to the same confusion.
    if isinstance(ret, bool):
        fired, signal = ret, "return(bool)"
    elif ret is not None and not (hasattr(ret, "__len__") and len(ret) == 0):
        fired, signal = True, "return"
    elif printed and "made_feature" in printed:
        fired, signal = True, "stdout"
    else:
        fired, signal = False, "none"
    ret_signal = signal.startswith("return")
    out_signal = signal == "stdout"
    ok = (fired == expect_fire) and err is None

    print("  %-9s expected=%-5s fired=%-5s  %s"
          % (label, expect_fire, fired, "OK" if ok else "** MISMATCH **"))
    print("        %s" % why)
    print("        return : %s%s" % (type(ret).__name__, "" if ret is None else " -> %s" % repr(ret)[:70]))
    print("        stdout : %s" % (printed.replace("\n", " | ")[:110] or "(empty)"))
    if err:
        print("        ** RAISED %s **" % err)
    results[label] = {"expected": expect_fire, "fired": fired, "ok": ok,
                      "return_type": type(ret).__name__, "return_repr": repr(ret)[:200],
                      "stdout": printed[:400], "error": err,
                      "signal": signal}
    return ok


pos = limb("POSITIVE", leaky_creation, True,
           "made_feature = y * 2 -- computed straight from the target")
print()
neg = limb("NEGATIVE", clean_creation, False,
           "made_feature = feat_a * 2 -- the target is never read")
print()

# THIRD LIMB: the vendor's OWN DEFAULT, recorded because it is what an adapter
# written from the signature would use. Expected to raise; the limb passes when
# it does, because the point is to document the breakage, not to pass around it.
buf = io.StringIO()
default_err = None
try:
    with contextlib.redirect_stdout(buf):
        leak_detect.detect_horizontal_leakage(
            data_creation_func=leaky_creation, input_data=input_data,
            target_cols=["y"], output_feature_cols=["made_feature"])
except Exception as e:                                  # noqa: BLE001
    default_err = "%s: %s" % (type(e).__name__, str(e).split("\n")[0])
print("  %-9s only_nan=False (THE VENDOR DEFAULT)" % "DEFAULT")
print("        stdout before the raise: %s"
      % (buf.getvalue().strip().replace("\n", " | ")[:96] or "(empty)"))
print("        %s" % (("** RAISES %s **" % default_err) if default_err
                      else "completed -- the default is NOT broken here"))
results["DEFAULT"] = {"only_nan": False, "raised": default_err,
                      "stdout": buf.getvalue().strip()[:400]}
print()

verdict = "DISCRIMINATING" if (pos and neg) else "NOT ESTABLISHED"
print("=== VERDICT ===")
print("  POSITIVE limb : %s" % ("FIRES" if pos else "** DID NOT FIRE **"))
print("  NEGATIVE limb : %s" % ("SILENT" if neg else "** ALSO FIRES **"))
print("  DEFAULT mode  : %s" % (("BROKEN -- %s" % default_err.split(":")[0])
                                if default_err else "usable"))
print("  signal carried by: POSITIVE=%s  NEGATIVE=%s"
      % (results["POSITIVE"]["signal"], results["NEGATIVE"]["signal"]))
print()
if verdict == "DISCRIMINATING":
    print("RESULT: DISCRIMINATING. leak-detect's acceptance-fixture result is "
          "interpretable -- provided the adapter reads the signal it actually "
          "emits.")
else:
    print("RESULT: NOT ESTABLISHED. leak-detect's acceptance-fixture result is "
          "`uninterpretable`, NOT a null.")

OUT.write_text(json.dumps({
    "tool": "leak-detect",
    "version": getattr(leak_detect, "__version__", None) or "0.0.1 (none declared)",
    "vendor_fixture": False, "vendor_negative": False,
    "limbs": results, "verdict": verdict,
}, indent=2), encoding="utf-8")
print("\nwritten: %s" % OUT.name)
sys.exit(0 if verdict == "DISCRIMINATING" else 1)
