"""W2b step 2 -- read leakfence's and leakage-buster's surfaces. READ-ONLY.

A control written against a remembered API fails for the wrong reason, and a
control that fails for the wrong reason is indistinguishable from a tool that
does not fire. That is the exact confusion W2b exists to remove, so the surface
is read before either control is written.

Neither vendor is known to ship a negative fixture. R143 §4 requires recording
WHICH tools had a vendor negative and which did not -- that difference belongs in
the coverage table, because a control whose negative limb we had to construct
ourselves is weaker evidence than one the vendor supplied.

    usage: probe_lf_lb_surface.py
"""
from __future__ import annotations

import inspect
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass


def surface(modname):
    print("=" * 78)
    try:
        mod = __import__(modname)
    except Exception as e:                              # noqa: BLE001
        print("%s FAILED TO IMPORT: %s: %s" % (modname, type(e).__name__, e))
        return None
    print("%s %s" % (modname, getattr(mod, "__version__", "(no __version__)")))
    print("  file: %s" % getattr(mod, "__file__", "?"))
    for n in sorted(d for d in dir(mod) if not d.startswith("_")):
        o = getattr(mod, n)
        try:
            sig = str(inspect.signature(o)) if callable(o) else "(%s)" % type(o).__name__
        except (TypeError, ValueError):
            sig = "(signature unavailable)"
        print("    %-32s %s" % (n, sig[:86]))
    return mod


lf = surface("leakfence")
lb = surface("leakage_buster")

print("=" * 78)
print("=== fixture-shaped names in either package (a vendor negative, if one exists) ===")
for mod in (lf, lb):
    if mod is None:
        continue
    found = [n for n in dir(mod)
             if any(k in n.lower() for k in
                    ("example", "sample", "demo", "fixture", "toy", "synthetic",
                     "clean", "nonleak", "no_leak"))]
    print("  %-18s %s" % (getattr(mod, "__name__", "?"), found or "NONE -- the negative must be constructed"))

print()
print("=== signatures the controls will call ===")
for mod, names in ((lf, ("audit_split", "check_duplicates", "lint_pipeline")),
                   (lb, ("audit",))):
    if mod is None:
        continue
    for n in names:
        o = getattr(mod, n, None)
        if o is None:
            o = getattr(getattr(mod, "api", None), n, None)
        if o is None:
            print("  %s.%s ABSENT" % (getattr(mod, "__name__", "?"), n))
            continue
        try:
            print("  %s.%s%s" % (getattr(mod, "__name__", "?"), n, inspect.signature(o)))
        except (TypeError, ValueError):
            print("  %s.%s (signature unavailable)" % (getattr(mod, "__name__", "?"), n))
        doc = (inspect.getdoc(o) or "").strip().split("\n")
        for d in doc[:6]:
            print("        %s" % d[:92])
