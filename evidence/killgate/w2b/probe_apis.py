"""W2b step 1 -- what each installed comparator actually exposes. READ-ONLY.

BEFORE A CONTROL CAN BE WRITTEN, THE ENTRY POINT MUST BE KNOWN FROM THE PACKAGE,
not from the k6 harness and not from memory. k6's runners are two rounds old and
were written against these versions, but a control that calls an API that has
moved would fail for the wrong reason -- and a control failing for the wrong
reason is exactly what W2b step 2 exists to stop being mistaken for a tool that
does not fire.

So this imports each package in ITS OWN VENV and prints the public surface, the
version, and whether the documented example fixtures W2b names actually exist
(`load_example_leakage_config` for Leakly, deepchecks' own suites).

Runs under whichever interpreter invokes it; the caller supplies the venv.

    usage: <venv-python> probe_apis.py <tool> [<tool> ...]
"""
from __future__ import annotations

import importlib
import inspect
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

# module name -> the callables k6 used, so drift shows up as a missing name
EXPECTED = {
    "leakage_buster": ["api.audit"],
    "leakfence": ["audit_split", "check_duplicates", "lint_pipeline"],
    "temporalcv": ["gates"],
    "leakly": ["MLPipeline", "permute_label", "load_example_leakage_config"],
    "leak_detect": ["base.detect_horizontal_leakage", "base.detect_vertical_leakage"],
    "deepchecks": ["tabular.Dataset", "tabular.suites.data_integrity",
                   "tabular.suites.train_test_validation"],
}


def resolve(mod, dotted):
    obj = mod
    for part in dotted.split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError:
            try:
                obj = importlib.import_module("%s.%s" % (obj.__name__, part))
            except Exception:                           # noqa: BLE001
                return None
    return obj


for name in sys.argv[1:]:
    print("=" * 74)
    print(name)
    print("=" * 74)
    try:
        mod = importlib.import_module(name)
    except Exception as e:                              # noqa: BLE001
        print("  NOT IMPORTABLE: %s: %s" % (type(e).__name__, e))
        continue
    print("  version : %s" % getattr(mod, "__version__", "(none declared)"))
    print("  file    : %s" % getattr(mod, "__file__", "?"))
    pub = sorted(a for a in dir(mod) if not a.startswith("_"))
    print("  public  : %s" % ", ".join(pub[:24]))
    if len(pub) > 24:
        print("            ... and %d more" % (len(pub) - 24))
    print("  entry points k6 used:")
    for dotted in EXPECTED.get(name, []):
        obj = resolve(mod, dotted)
        if obj is None:
            print("      %-42s ** MISSING **" % dotted)
            continue
        try:
            sig = str(inspect.signature(obj))
        except Exception:                               # noqa: BLE001
            sig = "(not a callable / no signature)"
        print("      %-42s %s" % (dotted, sig[:70]))
