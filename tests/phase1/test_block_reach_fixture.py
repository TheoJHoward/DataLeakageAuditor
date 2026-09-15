"""R271 §2(d)(f) -- the block-reach floor's positive at FIXTURE SCALE, opt-in.

THE PAIR. HELD: the acceptance fixture's corrected side (zc 2025-01), its model,
the seed, and ONE shared single-second and block-reach measurement. VARIED: the
stride alone.

  * STRIDE 16. R270's complete run at this stride reported 163,143 finding
    cohorts on a builder with no leak (D-V30A-114). It cannot be reproduced
    now, because the run REFUSES that stride against the block reach -- which
    is the repair. The figure stands in the record, as R263's stride-1 figure
    stands beside the refusal that replaced it.
  * THE STRIDE THE FLOOR GIVES. One pass through `_probe_complete`, timed, with
    the plan, both spreads and the prediction printed as a user sees them. It
    has to be silent with rows moving: no finding, liveness above zero.

COST, WHICH IS WHY THIS IS OPT-IN: about twenty minutes -- the capture, two clean
builds, ten single-second samples and ten block positions at ~40 s each, one
pass, and two more clean builds before the refusal. Run with
`LEAKAUDIT_FIXTURE=1`. `block_reach_fixture_record.json` beside this file records
when it ran, on which commit and with what figures, and the always-on test below
fails if that record does not cover every opt-in test here.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import time
import types
from contextlib import redirect_stdout
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                      # noqa: E402
from leakaudit import fixture_adapter as fa                   # noqa: E402
from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402
from leakaudit.reach import ReachError                        # noqa: E402

RECORD = Path(__file__).with_name("block_reach_fixture_record.json")
FIXTURE = os.environ.get("LEAKAUDIT_FIXTURE") == "1"
# R273 §1(a), accepted R274 §1(d): as-built declaration added -- the naive decision stamps are UTC.
MODEL = AvailabilityModel(aggregate_frames={"magg": "ts_floor", "trades": "ts_event"},
                          decision_column="timestamp", decision_timezone="UTC")
R270_STRIDE, R270_FINDINGS = 16, 163143


def _why_skipped():
    if not fa.F2_DIR.exists():
        return ("the acceptance fixture's producing code is not at %s. The last "
                "recorded result is in %s." % (fa.F2_DIR, RECORD.name))
    if not FIXTURE:
        return ("opt in with LEAKAUDIT_FIXTURE=1: about twenty minutes on the "
                "acceptance fixture. The last recorded result is in %s."
                % RECORD.name)
    return ""


needs_fixture = pytest.mark.skipif(bool(_why_skipped()), reason=_why_skipped())


@needs_fixture
def test_FIXTURE_stride_16_is_REFUSED_and_the_floors_stride_is_SILENT():
    t0 = time.time()
    cap = fa.read_inputs("zc", "2025-01")
    build = fa.builder_for(cap, "corrected")
    config = types.SimpleNamespace(column_modes=None, bar_duration=None)

    buf = io.StringIO()
    with redirect_stdout(buf):
        res, note = cli._probe_complete(cap.raw, build, MODEL, config, None,
                                        None, None, max_passes=1)
    out = buf.getvalue()
    sys.__stdout__.write(out + "\n" + note + "\n")
    m = re.search(r"COMPLETE RUN PLANNED: (\d+) pass\(es\) at stride (\d+)", out)
    assert m, out
    stride = int(m.group(2))
    assert stride > R270_STRIDE, out
    assert "elapsed so far" in out and "BLOCK REACH SPREAD" in out, out
    assert not res.findings, (
        "the floor's stride reported findings on a builder with no leak: %s"
        % [str(c.second) for c in res.findings[:10]])
    assert res.liveness > 0, "a silence with nothing moving is not this positive"

    t1 = time.time()
    with pytest.raises(ReachError) as e:
        run_probe_a(cap.raw, build, MODEL, side="corrected",
                    cohort_stride=R270_STRIDE, max_cohorts=10 ** 9,
                    reach=res.reach, block_reach=res.block_reach)
    assert "BLOCK REACH" in str(e.value), str(e.value)
    sys.__stdout__.write(
        "\nFIXTURE PAIR: stride %d REFUSED (%.0f s); stride %d pass 1 of %s: "
        "%d cohorts, 0 findings, liveness %d; total %.0f s\n"
        % (R270_STRIDE, time.time() - t1, stride, m.group(1), res.n_cohorts,
           res.liveness, time.time() - t0))


# --------------------------------------------------------------------------
# Always-on: the opt-in test has a recorded result, and the record carries the
# pair's figures. A skipped positive nobody recorded is a claim nobody can check.
# --------------------------------------------------------------------------

def test_the_fixture_pair_HAS_a_recorded_result():
    rec = json.loads(RECORD.read_text(encoding="utf-8"))
    src = Path(__file__).read_text(encoding="utf-8")
    opt_in = set(re.findall(r"^@needs_fixture\s*\ndef\s+(\w+)", src, re.M))
    assert opt_in, "no opt-in tests found; the extractor is broken, not the record"
    recorded = {r["test"]: r["result"] for r in rec["results"]}
    missing = opt_in - set(recorded)
    assert not missing, "opt-in test(s) with no recorded result: %s" % sorted(missing)
    assert all(recorded[t] == "PASS" for t in opt_in), recorded
    assert rec["date"] and rec["commit"]
    assert rec["r270_stride_16_findings"] == R270_FINDINGS
    assert rec["stride"] > R270_STRIDE
    assert rec["pass_1_findings"] == 0 and rec["pass_1_liveness"] > 0
