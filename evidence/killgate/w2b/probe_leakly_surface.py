"""W2b step 2, Leakly -- read the surface the control will use. READ-ONLY.

Leakly is the one vendor that ships BOTH fixtures, so its control can be a PAIR:
a documented positive and a documented negative. A positive alone shows only
REACHABILITY -- that the tool can fire. Only the pair shows DISCRIMINATION, and a
tool that fires on both has told us nothing about the run it is being trusted to
interpret.

This script does not run the control. It reads the signatures the control must
call, because a control written against a remembered API fails for the wrong
reason -- which is exactly what would be mistaken for a tool that does not fire.

    usage: probe_leakly_surface.py
"""
from __future__ import annotations

import inspect
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

import leakly

print("leakly %s from %s" % (getattr(leakly, "__version__", "?"), leakly.__file__))
print()

print("=== module surface ===")
for n in sorted(d for d in dir(leakly) if not d.startswith("_")):
    o = getattr(leakly, n)
    kind = type(o).__name__
    try:
        sig = str(inspect.signature(o)) if callable(o) else ""
    except (TypeError, ValueError):
        sig = "(signature unavailable)"
    print("  %-34s %-10s %s" % (n, kind, sig[:78]))

print()
print("=== the two fixtures, and what they actually return ===")
for fn in ("load_example_leakage_config", "load_example_nonleakage_config"):
    f = getattr(leakly, fn, None)
    if f is None:
        print("  %-34s ABSENT" % fn)
        continue
    try:
        cfg = f()
    except Exception as e:                              # noqa: BLE001
        print("  %-34s RAISED %s: %s" % (fn, type(e).__name__, e))
        continue
    print("  %-34s -> %s" % (fn, type(cfg).__name__))
    if hasattr(cfg, "__dict__"):
        for k, v in vars(cfg).items():
            print("        %-24s %s" % (k, repr(v)[:88]))
    elif isinstance(cfg, dict):
        for k, v in cfg.items():
            print("        %-24s %s" % (k, repr(v)[:88]))

print()
print("=== MLPipeline / permute_label ===")
for n in ("MLPipeline", "permute_label"):
    o = getattr(leakly, n, None)
    if o is None:
        print("  %s ABSENT" % n)
        continue
    try:
        print("  %s%s" % (n, inspect.signature(o)))
    except (TypeError, ValueError):
        print("  %s (signature unavailable)" % n)
    if inspect.isclass(o):
        for m in sorted(d for d in dir(o) if not d.startswith("_")):
            try:
                print("      .%-28s %s" % (m, inspect.signature(getattr(o, m))))
            except (TypeError, ValueError):
                print("      .%s" % m)
