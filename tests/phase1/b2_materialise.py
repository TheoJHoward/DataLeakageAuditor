"""B-2 step 1 -- materialise the acceptance fixture as comparator inputs.

§9.2 step 3 needs BOTH sides of the acceptance fixture as files the comparators
can read, because each runs in its own virtualenv with conflicting pandas and
scikit-learn pins and cannot be handed an in-process DataFrame.

SC-7(d) IS ENFORCED HERE BY SEQUENCING, NOT BY THE ADAPTER. `fixture_corrected`
is defined as `fixture_contaminated` plus a lag, so the two sides read exactly
the same inputs and nothing structurally stops a caller building both at once.
The rule is one side at a time, so this script BUILDS ONE SIDE, WRITES IT,
DROPS THE REFERENCE, and only then builds the other. The order is recorded.

READS HAPPEN ONCE. `read_inputs` captures the builder's three reads by running it
with the reads intercepted; both sides are then served from that capture, so the
comparators see exactly what the builder loads -- including any column selection
or dtype handling the builder's own read applies.

    usage: b2_materialise.py [outdir]
"""
from __future__ import annotations

import gc
import hashlib
import json
import pathlib
import sys
import time

# BOTH the repo root and `src` go on the path. `leakaudit.contract` imports
# `protocol.runtime_reference`, which lives at the repo root -- and for a SCRIPT
# `sys.path[0]` is the script's own directory, not the working directory. An
# earlier inline `python -c` run succeeded only because `-c` puts the cwd on the
# path, which made the missing entry invisible until this ran as a file.
_ROOT = pathlib.Path(__file__).resolve().parents[2]
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

from leakaudit import fixture_adapter as fa            # noqa: E402

SYM, MONTH = "zc", "2025-01"
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
                   pathlib.Path(__file__).resolve().parents[2] / "b2_inputs")
OUT.mkdir(parents=True, exist_ok=True)

t0 = time.time()
inputs = fa.read_inputs(SYM, MONTH)
print("read_inputs %s %s in %.1fs" % (SYM, MONTH, time.time() - t0))
for k, v in sorted(inputs.frames.items()):
    print("  %-34s %s" % (k, "None" if v is None else "%d x %d" % v.shape))
print()

manifest = {"sym": SYM, "month": MONTH, "order": [], "sides": {}}

# ONE SIDE AT A TIME. The loop body finishes with the frame written and released
# before the next side is built; `gc.collect()` makes that explicit rather than
# leaving it to refcount timing.
for side in ("contaminated", "corrected"):
    t = time.time()
    build = fa.builder_for(inputs, side=side)
    df = build(inputs.raw)
    took = time.time() - t
    path = OUT / ("acceptance_%s_%s_%s.parquet" % (SYM, MONTH, side))
    df.to_parquet(path, index=False)
    b = path.read_bytes()
    rec = {"rows": int(df.shape[0]), "cols": int(df.shape[1]),
           "columns": [str(c) for c in df.columns],
           "dtypes": {str(c): str(t_) for c, t_ in df.dtypes.items()},
           "file": path.name, "bytes": len(b),
           "sha256": hashlib.sha256(b).hexdigest(),
           "build_seconds": round(took, 1)}
    manifest["order"].append(side)
    manifest["sides"][side] = rec
    print("%-13s %6d x %-3d  %8.1fs  %s  %s"
          % (side, df.shape[0], df.shape[1], took, path.name, rec["sha256"][:16]))
    del df, build
    gc.collect()

# The two sides MUST differ. `fixture_corrected` adds a lag; if the files come out
# byte-identical the adapter served the same side twice and every downstream
# comparison would be measuring nothing.
a = manifest["sides"]["contaminated"]["sha256"]
b_ = manifest["sides"]["corrected"]["sha256"]
print()
if a == b_:
    sys.exit("HALT: the two sides are byte-identical -- the harness built one "
             "side twice and no comparator result from these files would mean "
             "anything")
print("the two sides differ: %s vs %s" % (a[:16], b_[:16]))

cols_a = manifest["sides"]["contaminated"]["columns"]
cols_b = manifest["sides"]["corrected"]["columns"]
if cols_a != cols_b:
    print("** the two sides' column sets DIFFER **")
    print("   only contaminated: %s" % sorted(set(cols_a) - set(cols_b)))
    print("   only corrected   : %s" % sorted(set(cols_b) - set(cols_a)))
else:
    print("both sides carry the same %d columns" % len(cols_a))

(OUT / "b2_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print("\nwritten: %s" % (OUT / "b2_manifest.json"))
print("columns: %s" % ", ".join(cols_a[:14]))
