"""R261 §4. The label probe from the COMMAND LINE, on a leak, end to end.

    PYTHONPATH=. py -3.12 <this file>

The library tests cover the probe. This asks the question the backlog's own
mandate test asks -- can a stranger with their own pandas pipeline probe label
leakage? -- by writing a model file, a pipeline and two CSVs and running the
installed command over them, with nothing imported from the test suite.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

import json
import pathlib
import sys
import tempfile

import numpy as np
import pandas as pd

REPO = pathlib.Path.cwd()
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from leakaudit import cli                                          # noqa: E402

PIPELINE = """\
import numpy as np
import pandas as pd


def build(f):
    lab = f['lab'].copy()
    y = lab['y'].to_numpy()
    lagged = np.concatenate(([np.nan], y[:-1]))
    return pd.DataFrame({'d': pd.to_datetime(lab['ts']), 'x': lagged})
"""


def main() -> int:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="l2a_cli_"))
    ts = pd.date_range("2026-01-01 00:00:00", periods=90, freq="1s")
    y = np.random.default_rng(11).standard_normal(90)
    pd.DataFrame({"ts": ts, "y": y}).to_csv(tmp / "lab.csv", index=False)
    (tmp / "p.py").write_text(PIPELINE, encoding="utf-8")

    def model(horizon):
        return {
            "version": 4,
            "aggregate_frames": {"lab": "ts"},
            "decision_column": "d",
            "raw_label": {"frame": "lab", "column": "y"},
            "label_availability": {"base_column": "ts",
                                   "horizon_seconds": horizon},
        }

    sys.path.insert(0, str(tmp))
    for label, horizon in (("HORIZON 60s -- the lagged label is not realized", 60.0),
                           ("HORIZON 0s  -- the same lagged label IS realized", 0.0)):
        (tmp / "m.json").write_text(json.dumps(model(horizon)), encoding="utf-8")
        print("=" * 74)
        print(label)
        print("=" * 74)
        try:
            cli.main(["run", "--pipeline", "p:build",
                      "--frame", "lab=%s" % (tmp / "lab.csv"),
                      "--model", str(tmp / "m.json"),
                      "--stride", "7", "--max-cohorts", "10"])
        except SystemExit as e:
            print("(exit %s)" % e.code)
        print()

    print("=" * 74)
    print("NEITHER KEY DECLARED -- L2a reports unsupported, never a pass")
    print("=" * 74)
    m = model(60.0)
    del m["raw_label"], m["label_availability"]
    (tmp / "m.json").write_text(json.dumps(m), encoding="utf-8")
    try:
        cli.main(["run", "--pipeline", "p:build",
                  "--frame", "lab=%s" % (tmp / "lab.csv"),
                  "--model", str(tmp / "m.json"),
                  "--stride", "7", "--max-cohorts", "10"])
    except SystemExit as e:
        print("(exit %s)" % e.code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
