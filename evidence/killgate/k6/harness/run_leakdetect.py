"""Run leak-detect 0.0.1 against the eligible cases.

Eligible per PRE_RUN_RECORD 4.7: C5 (T5, horizontal probe) and C6 (T6, vertical probe).
C2/C3 are additionally exercised as SUPPLEMENTARY (declared ineligible; not scored).

Scored probe-wise per PRE_RUN_RECORD 6.3:
  - default configuration only_nan=False -> exercises BOTH the NaN probe and the complex probe.
    The complex probe calls np.complex (base.py:76 / base.py:209), removed in NumPy >= 1.24.
    Its failure is captured verbatim and published as an item-5 crash-abstention.
  - only_nan=True (documented public parameter) -> NaN probe alone; result scored on merit.
"""
import contextlib
import io
import json
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.abspath(os.path.join(HERE, "..", "raw"))

import case_defs as cd  # noqa: E402
from leak_detect.base import detect_horizontal_leakage, detect_vertical_leakage  # noqa: E402

# probe wiring per case: which raw cols feed the builder, which built cols are checked
WIRING = {
    "C6": dict(probe="vertical", input_feature_cols=["x"], output_feature_cols=["win5"]),
    "C5": dict(probe="horizontal", target_cols=["target"], output_feature_cols=["risk_score"]),
    "C2": dict(probe="vertical", input_feature_cols=["f0", "f1", "f2", "f3"],
               output_feature_cols=["f0", "f1", "f2", "f3"]),
    "C3": dict(probe="vertical", input_feature_cols=[f"f{i}" for i in range(30)],
               output_feature_cols=None),  # resolved at run time to the built frame's cols
}


def one(case, side, only_nan):
    w = WIRING[case]
    d = cd.get(case, side)
    raw, build = d["raw"], d["build"]
    buf = io.StringIO()
    rec = dict(tool="leak-detect", version="0.0.1", case=case, side=side,
               config=dict(only_nan=only_nan, probe=w["probe"],
                           check_row_number="default int(len(data)/2)=200",
                           direction="upward" if w["probe"] == "vertical" else None))
    try:
        with contextlib.redirect_stdout(buf):
            if w["probe"] == "vertical":
                ocols = w["output_feature_cols"]
                if ocols is None:
                    ocols = [c for c in build(raw).columns if c != "target"]
                fired = detect_vertical_leakage(
                    build, raw.copy(), w["input_feature_cols"], ocols,
                    only_nan=only_nan, direction="upward")
            else:
                fired = detect_horizontal_leakage(
                    build, raw.copy(), w["target_cols"], w["output_feature_cols"],
                    only_nan=only_nan)
        rec.update(status="ran", fired=bool(fired), stdout=buf.getvalue())
    except Exception as e:
        rec.update(status="crash", fired=None, stdout=buf.getvalue(),
                   error=f"{type(e).__name__}: {e}",
                   traceback=traceback.format_exc()[-1500:])
    return rec


def main():
    out = []
    for case in ["C6", "C5", "C2", "C3"]:
        for only_nan in [False, True]:
            for side in cd.SIDES:
                r = one(case, side, only_nan)
                out.append(r)
                print(f"{case:3s} {side:13s} only_nan={str(only_nan):5s} -> "
                      f"{r['status']:5s} fired={r.get('fired')}"
                      + (f"  ERR={r.get('error','')[:70]}" if r["status"] == "crash" else ""))
    with open(os.path.join(OUT, "leak-detect.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
