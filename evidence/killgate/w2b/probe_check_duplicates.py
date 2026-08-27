"""Is check_duplicates not firing, or is my adapter wrong? READ-ONLY.

The control read `.violations` off whatever `check_duplicates` returned. If it
returns something else -- a list, a stats object, None -- then `getattr(r,
"violations", None)` yields None, the control records "did not fire", and I would
have written down a finding about the TOOL that is actually a finding about MY
CALL. That is precisely the confusion W2b exists to remove, and it applies to my
own adapter before it applies to anyone's tool.

    usage: probe_check_duplicates.py
"""
from __future__ import annotations

import inspect
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

import leakfence

print("=== source ===")
try:
    print(inspect.getsource(leakfence.check_duplicates))
except (OSError, TypeError) as e:
    print("unavailable: %s" % e)

dup_X = [[1, 1], [2, 2], [3, 3], [1, 1], [4, 4], [5, 5]]
uniq_X = [[1, 1], [2, 2], [3, 3], [9, 9], [4, 4], [5, 5]]

for name, X in (("DUPLICATED (row 0 == row 3)", dup_X), ("DISTINCT", uniq_X)):
    print("=" * 74)
    print("=== %s ===" % name)
    for label, kwargs in (("with split", {"train_idx": [0, 1, 2], "test_idx": [3, 4, 5]}),
                          ("no split", {})):
        try:
            r = leakfence.check_duplicates(X, **kwargs)
        except Exception as e:                          # noqa: BLE001
            print("  %-12s RAISED %s: %s" % (label, type(e).__name__, e))
            continue
        print("  %-12s -> %s" % (label, type(r).__name__))
        print("               repr: %s" % repr(r)[:150])
        if hasattr(r, "__dict__"):
            for k, v in vars(r).items():
                print("               .%-18s %s" % (k, repr(v)[:90]))
        elif isinstance(r, (list, tuple, set, frozenset)):
            print("               len=%d  items: %s" % (len(r), repr(list(r))[:110]))

print("=" * 74)
print("=== fingerprint_rows, which the duplicate check is built on ===")
print("  duplicated X -> %d distinct fingerprints for %d rows"
      % (len(leakfence.fingerprint_rows(dup_X)), len(dup_X)))
print("  distinct   X -> %d distinct fingerprints for %d rows"
      % (len(leakfence.fingerprint_rows(uniq_X)), len(uniq_X)))
