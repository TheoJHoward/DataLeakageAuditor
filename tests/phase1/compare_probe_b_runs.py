"""Compare two merged Probe B runs, cohort for cohort.

WHY THIS EXISTS. R134 found that the perturbation seed was
`abs(hash((frame, column, strategy)))`, which CPython salts per process. Every
run therefore drew a different permutation, and B8.3's recorded result cannot be
reproduced from its own inputs. The seed is fixed now, but fixing it does not
tell you what the old one cost -- for that the sweep has to be run again and the
two results put side by side.

WHAT A DIFFERENCE MEANS, AND WHAT IT DOES NOT. A difference here is NOT a defect
in the pipeline and NOT a defect in the detector. Any permutation is a
legitimate shuffle, so two draws are two valid probes. What the comparison
measures is **how much the draw could move the answer** -- which cohorts are
seed-sensitive, and therefore how much of B8.3's 33-fired/14-silent split was a
property of the pipeline rather than of one unrepeatable draw.

    identical  -> the draw never mattered on this fixture. B8.3's numbers stand
                  as reported, and the seed defect cost reproducibility only.
    differing  -> the named cohorts flipped. Each one is a cohort whose reported
                  outcome depended on which permutation was drawn, and
                  `observed_silence` there was a coin toss.

THE BASELINE DIGEST MUST BE IDENTICAL EITHER WAY. The baseline is built from
unperturbed input, so no seed can reach it. If the two runs disagree on it, the
difference is not the seed and this comparison is measuring something else --
which is a halt, not a finding.

    usage: compare_probe_b_runs.py <recorded.json> <rerun.json>
"""
from __future__ import annotations

import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass


def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


a = load(sys.argv[1])
b = load(sys.argv[2])
NA, NB = pathlib.Path(sys.argv[1]).name, pathlib.Path(sys.argv[2]).name

print("=" * 78)
print("POPULATION, ASSERTED BEFORE ANYTHING IS COMPARED")
print("=" * 78)
for name, d in ((NA, a), (NB, b)):
    print("  %-26s cohorts=%-3d shards=%-2d baseline=%s"
          % (name, d["cohorts"], d["shards"], d["baseline_sha256"][:16]))

if a["baseline_sha256"] != b["baseline_sha256"]:
    sys.exit("\nHALT: the two runs disagree on the BASELINE digest. The baseline "
             "is built from unperturbed input and no seed can reach it, so the "
             "difference between these runs is not the seed. Comparing their "
             "findings would attribute that difference to the wrong cause.")
print("  baselines agree -- the only thing that changed is the draw.")

if a["cohorts"] != b["cohorts"]:
    sys.exit("\nHALT: %d cohorts vs %d. Different populations are not comparable."
             % (a["cohorts"], b["cohorts"]))

# ---- trace level ----------------------------------------------------------
print()
print("=" * 78)
print("TRACES")
print("=" * 78)
trace_diffs = []
for k in sorted(set(a["traces"]) | set(b["traces"])):
    ta, tb = a["traces"].get(k, {}), b["traces"].get(k, {})
    same = ta == tb
    trace_diffs += [] if same else [k]
    print("  %-11s %s" % (k, "IDENTICAL" if same else "DIFFERS"))
    for f in ("schedule_state", "reason", "evidence_outcome", "cohorts",
              "records", "valid_records"):
        va, vb = ta.get(f), tb.get(f)
        mark = "  " if va == vb else "->"
        print("      %-18s %-24s %s %s" % (f, va, mark, vb if va != vb else ""))

# ---- cohort level ---------------------------------------------------------
da, db = a["dependency_map"], b["dependency_map"]
fired_a, fired_b = set(da), set(db)
silent_a = set(a["silent_cohorts"])
silent_b = set(b["silent_cohorts"])

print()
print("=" * 78)
print("COHORTS")
print("=" * 78)
print("  fired   %-4d -> %-4d" % (len(fired_a), len(fired_b)))
print("  silent  %-4d -> %-4d" % (len(silent_a), len(silent_b)))

became_silent = sorted(fired_a - fired_b)
became_fired = sorted(fired_b - fired_a)
feature_moves = []
for cid in sorted(fired_a & fired_b):
    if set(da[cid]) != set(db[cid]):
        feature_moves.append((cid, sorted(set(da[cid]) - set(db[cid])),
                              sorted(set(db[cid]) - set(da[cid]))))

if became_silent:
    print()
    print("  FIRED IN %s, SILENT IN %s -- the draw decided the outcome:" % (NA, NB))
    for cid in became_silent:
        print("      %-34s was: %s" % (cid, ", ".join(da[cid])[:70]))
if became_fired:
    print()
    print("  SILENT IN %s, FIRED IN %s:" % (NA, NB))
    for cid in became_fired:
        print("      %-34s now: %s" % (cid, ", ".join(db[cid])[:70]))
if feature_moves:
    print()
    print("  FIRED IN BOTH, DIFFERENT FEATURES:")
    for cid, lost, gained in feature_moves:
        print("      %-34s -%s +%s" % (cid, lost or "-", gained or "-"))

# ---- verdict --------------------------------------------------------------
n = len(became_silent) + len(became_fired) + len(feature_moves)
print()
print("=" * 78)
print("VERDICT")
print("=" * 78)
if n == 0 and not trace_diffs:
    print("  IDENTICAL, cohort for cohort and trace for trace.")
    print("  The permutation draw never changed an outcome on this fixture, so")
    print("  the salted seed cost REPRODUCIBILITY and nothing else. B8.3's")
    print("  numbers stand exactly as reported.")
else:
    print("  %d cohort(s) and %d trace field group(s) differ." % (n, len(trace_diffs)))
    print("  Each named cohort's reported outcome depended on which permutation")
    print("  was drawn. `observed_silence` at those cohorts was a coin toss, and")
    print("  B8.3's report must say so for them by name.")
sys.exit(0)
