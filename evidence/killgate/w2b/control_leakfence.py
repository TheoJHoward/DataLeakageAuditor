"""W2b step 2, leakfence -- THE CONTROL. Two independent pairs.

NO VENDOR FIXTURE. Unlike Leakly, leakfence ships no example leakage config and
no clean counterpart (`sample_size` is a module, not a fixture). BOTH LIMBS ARE
THEREFORE CONSTRUCTED HERE, and R143 §4 requires that difference be recorded
rather than smoothed over: a negative we wrote ourselves is weaker evidence than
one the vendor supplied, because we chose what "clean" means and could have
chosen something the tool happens not to look at.

TWO PAIRS, NOT ONE. `audit_split` and `check_duplicates` detect different things,
and a tool can be alive on one surface and dead on another. Testing only the
first would license a null from the second.

  PAIR 1  audit_split      positive: a subject appears in BOTH train and test
                           negative: subjects are disjoint
  PAIR 2  check_duplicates positive: identical rows on both sides of the split
                           negative: every row distinct

WHAT WOULD FALSIFY EACH, stated before running: a positive that raises no
violation means the tool did not fire and its acceptance-fixture result is
UNINTERPRETABLE; a negative that raises one means the tool flags clean splits and
its positive proves nothing.

    usage: control_leakfence.py
"""
from __future__ import annotations

import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

import leakfence

OUT = pathlib.Path(__file__).resolve().parent / "control_leakfence_result.json"
print("leakfence %s  |  vendor fixture: NONE -- both limbs constructed here"
      % getattr(leakfence, "__version__", "?"))
print()

results = {}


def violations_of(report):
    """Violations, whatever shape the entry point returns them in.

    A first version read `.violations` and nothing else. `audit_split` returns an
    AuditReport, which has it; `check_duplicates` returns a plain TUPLE
    `(groups, violations)`, which does not. So the probe recorded
    check_duplicates as NOT FIRING on a byte-identical row that it had in fact
    detected -- a finding about MY CALL written down as a finding about the TOOL.
    That is the precise confusion W2b exists to remove, and it applies to this
    adapter before it applies to any vendor.

    The shape is therefore resolved explicitly, and an UNRECOGNISED shape raises
    rather than returning [] -- an empty list here reads as "clean", and a
    silently-empty result is how the original defect looked.
    """
    if hasattr(report, "violations"):
        return list(report.violations or [])
    if isinstance(report, tuple):
        for part in reversed(report):
            if isinstance(part, list):
                return part
        raise TypeError("tuple return carries no violations list: %r" % (report,))
    if isinstance(report, list):
        return report
    raise TypeError("unrecognised return shape %s -- refusing to read it as "
                    "'no violations'" % type(report).__name__)


def limb(pair, label, expect_fire, fn, why):
    """Run one limb. `expect_fire` says whether a violation SHOULD appear."""
    try:
        report = fn()
        vs = violations_of(report)
        raised = None
    except leakfence.LeakageError as e:                 # a raise IS a firing
        vs, raised = [], type(e).__name__
    except Exception as e:                              # noqa: BLE001
        print("  %-9s %-9s ** RAISED %s: %s **" % (pair, label, type(e).__name__, e))
        results["%s/%s" % (pair, label)] = {"error": "%s: %s" % (type(e).__name__, e)}
        return False
    fired = bool(vs) or raised is not None
    ok = (fired == expect_fire)
    detail = ("; ".join(getattr(x, "check", str(x)) for x in vs) or raised or "none")
    print("  %-9s %-9s fired=%-5s expected=%-5s  %s"
          % (pair, label, fired, expect_fire, "OK" if ok else "** MISMATCH **"))
    print("        %s" % why)
    print("        violations: %s" % detail[:96])
    results["%s/%s" % (pair, label)] = {"fired": fired, "expected": expect_fire,
                                        "ok": ok, "violations": detail}
    return ok


# --- PAIR 1: audit_split, subject overlap ----------------------------------
# Twelve windows, six subjects, two windows each. The leaky split puts subject 0
# on BOTH sides; the clean split keeps every subject wholly on one side.
subj = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
p1a = limb("audit", "POSITIVE", True,
           lambda: leakfence.audit_split(train_idx=[0, 2, 3, 4, 5],
                                         test_idx=[1, 6, 7, 8, 9], subject=subj),
           "subject 0 has window 0 in train and window 1 in test")
p1b = limb("audit", "NEGATIVE", False,
           lambda: leakfence.audit_split(train_idx=[0, 1, 2, 3, 4, 5],
                                         test_idx=[6, 7, 8, 9, 10, 11], subject=subj),
           "subjects 0-2 train, 3-5 test -- disjoint, nothing to find")
print()

# --- PAIR 2: check_duplicates ----------------------------------------------
dup_X = [[1, 1], [2, 2], [3, 3], [1, 1], [4, 4], [5, 5]]     # row 0 == row 3
uniq_X = [[1, 1], [2, 2], [3, 3], [9, 9], [4, 4], [5, 5]]
p2a = limb("dupes", "POSITIVE", True,
           lambda: leakfence.check_duplicates(dup_X, train_idx=[0, 1, 2],
                                              test_idx=[3, 4, 5]),
           "row 0 in train is byte-identical to row 3 in test")
p2b = limb("dupes", "NEGATIVE", False,
           lambda: leakfence.check_duplicates(uniq_X, train_idx=[0, 1, 2],
                                              test_idx=[3, 4, 5]),
           "the same shape with every row distinct")
print()

pairs = {"audit_split": (p1a, p1b), "check_duplicates": (p2a, p2b)}
print("=== VERDICT ===")
alive = []
for name, (pos, neg) in pairs.items():
    state = ("DISCRIMINATING" if pos and neg
             else "NOT ESTABLISHED (positive did not fire)" if not pos
             else "NOT ESTABLISHED (fires on the clean case too)")
    print("  %-18s %s" % (name, state))
    alive.append(pos and neg)

verdict = "DISCRIMINATING" if all(alive) else "NOT ESTABLISHED"
print()
if verdict == "DISCRIMINATING":
    print("RESULT: DISCRIMINATING on both surfaces. leakfence's acceptance-fixture "
          "result is interpretable -- with the caveat that BOTH limbs were "
          "constructed here, since the vendor ships no fixture.")
else:
    print("RESULT: NOT ESTABLISHED. leakfence's acceptance-fixture result is "
          "`uninterpretable`, NOT a null.")

OUT.write_text(json.dumps({
    "tool": "leakfence", "version": getattr(leakfence, "__version__", "0.5.0"),
    "vendor_fixture": False, "vendor_negative": False,
    "limbs": results, "verdict": verdict,
}, indent=2), encoding="utf-8")
print("\nwritten: %s" % OUT.name)
sys.exit(0 if verdict == "DISCRIMINATING" else 1)
