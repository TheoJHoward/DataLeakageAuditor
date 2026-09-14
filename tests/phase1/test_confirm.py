"""`--confirm`: every batched finding re-probed alone, split, and classed. R271 §3.

Isolation removes a real lookahead leak as surely as it removes interference: a
row at F reading a LATER cohort's unavailable cells moves in the batch and not
alone. So a finding that does not persist alone is re-probed twice more -- with
the batch's later cohorts only, and with its earlier cohorts only -- and that
split is the instrument.

THE PAIRS. HELD: the frames, the model, `--stride 3`, `--confirm`. VARIED: the
builder alone.

  * `leaky` reads its own second's cell. Every finding persists alone:
    CONFIRMED.
  * `lagpatch` reads the previous second's cell -- available -- except on
    decision seconds 50..58, where it reads three seconds BACK, still available.
    The batch reports false findings at 51, 54 and 57; alone they vanish; with
    the earlier cohorts they return. INTERFERENCE, and the run's silences stop
    being licensed: every one is `none`, and the run exits refused.
  * `lookahead` reads the previous second except on 50..58, where it reads
    three seconds AHEAD -- unavailable. The batch reports 51 and 54; alone they
    vanish; with the later cohorts they return. CONFIRMED (lookahead), naming
    the later second, and the run exits on its findings.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                      # noqa: E402
from leakaudit.availability import (                           # noqa: E402
    CohortResult, IsolationResult, ProbeAResult)

N = 60
T0 = pd.Timestamp("2026-01-01 00:00:00")

PIPELINE = (
    "import numpy as np\n"
    "import pandas as pd\n"
    "\n"
    "def _prep(frames):\n"
    "    agg = frames['agg'].copy()\n"
    "    agg['k'] = pd.to_datetime(agg['k'])\n"
    "    out = frames['dec'].copy()\n"
    "    out['d'] = pd.to_datetime(out['d'])\n"
    "    return agg, out\n"
    "\n"
    "def leaky(frames):\n"
    "    agg, out = _prep(frames)\n"
    "    v = pd.Series(agg['v'].to_numpy(), index=agg['k'])\n"
    "    out['feat'] = out['d'].dt.floor('s').map(v)\n"
    "    return out\n"
    "\n"
    "def _patched(frames, patch_lag):\n"
    "    agg, out = _prep(frames)\n"
    "    v = pd.Series(agg['v'].to_numpy(), index=agg['k'])\n"
    "    s = out['d'].dt.floor('s')\n"
    "    idx = ((s - s.min()) / pd.Timedelta(seconds=1)).astype(int)\n"
    "    lag = pd.Series(np.where((idx >= 50) & (idx <= 58), patch_lag, 1), index=s.index)\n"
    "    out['feat'] = (s - pd.to_timedelta(lag, unit='s')).map(v)\n"
    "    return out\n"
    "\n"
    "def lagpatch(frames):\n"
    "    return _patched(frames, 3)\n"
    "\n"
    "def lookahead(frames):\n"
    "    return _patched(frames, -3)\n")


@pytest.fixture
def work(tmp_path):
    name = "r271_confirm_pipe"
    (tmp_path / (name + ".py")).write_text(PIPELINE, encoding="utf-8")
    secs = pd.date_range(T0, periods=N, freq="1s")
    pd.DataFrame({"k": secs, "v": [float(i % 17) + 1.0 for i in range(N)]}
                 ).to_csv(tmp_path / "agg.csv", index=False)
    pd.DataFrame({"d": secs + pd.Timedelta(milliseconds=500), "row": range(N)}
                 ).to_csv(tmp_path / "dec.csv", index=False)
    (tmp_path / "m.json").write_text(json.dumps({
        "version": 3, "aggregate_frames": {"agg": "k"},
        "decision_column": "d"}), encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield tmp_path, name
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(name, None)


def _run(work, fn, *extra, model=True):
    tmp, name = work
    argv = ["run", "--pipeline", "%s:%s" % (name, fn),
            "--frame", "agg=%s" % (tmp / "agg.csv"),
            "--frame", "dec=%s" % (tmp / "dec.csv")]
    if model:
        argv += ["--model", str(tmp / "m.json")]
    return cli.main(argv + list(extra))


#: Notes render as `  - <text>`. A class line is one whose text STARTS with its
#: tag and then names a second, so CONFIRMED does not also count
#: "CONFIRMED (lookahead)", and "NOT CONFIRMED" inside another line is not one.
_LEAD = r"^[ \t]*-?[ \t]*"


def _seconds(out, tag):
    return re.findall(_LEAD + re.escape(tag) + r"\s+(\d{4}-\d\d-\d\d \S+):",
                      out, re.M)


# --------------------------------------------------------------------------
# the three builders
# --------------------------------------------------------------------------

def test_LEAKY_findings_are_CONFIRMED_within_the_derived_cap(work, capsys):
    code = _run(work, "leaky", "--stride", "3", "--confirm")
    out = capsys.readouterr().out
    assert code == cli.EXIT_FINDINGS
    assert len(_seconds(out, "CONFIRMED")) == 5, out[-3000:]
    assert "default cap 5 (600 s target" in out, out[-3000:]
    assert ("CONFIRM SUMMARY: 5 confirmed, 0 confirmed (lookahead), 0 "
            "interference, 0 batched only, 15 not re-probed, of 20") in out


def test_LAGPATCH_is_INTERFERENCE_and_the_run_is_REFUSED(work, capsys):
    code = _run(work, "lagpatch", "--stride", "3", "--confirm")
    cap = capsys.readouterr()
    out = cap.out
    assert _seconds(out, "INTERFERENCE") == [
        "2026-01-01 00:00:51", "2026-01-01 00:00:54", "2026-01-01 00:00:57"], out[-3000:]
    assert not _seconds(out, "CONFIRMED")
    assert "every silence in this run is none(interference detected at stride 3" in out
    assert code == cli.EXIT_USAGE, "an interference class makes the run refused"
    assert "RUN REFUSED" in cap.err


def test_LOOKAHEAD_is_CONFIRMED_and_names_the_later_second(work, capsys):
    code = _run(work, "lookahead", "--stride", "3", "--confirm")
    out = capsys.readouterr().out
    assert _seconds(out, "CONFIRMED (lookahead)") == [
        "2026-01-01 00:00:51", "2026-01-01 00:00:54"], out[-3000:]
    assert "later second 2026-01-01 00:00:54" in out, out[-3000:]
    assert "later second 2026-01-01 00:00:57" in out
    assert not _seconds(out, "INTERFERENCE")
    assert code == cli.EXIT_FINDINGS


def test_WITHOUT_confirm_the_same_run_prints_no_classes(work, capsys):
    _run(work, "lagpatch", "--stride", "3")
    out = capsys.readouterr().out
    assert "CONFIRM" not in out


# --------------------------------------------------------------------------
# the class rule, on its own
# --------------------------------------------------------------------------

def _iso(persisted=False, later=None, earlier=None):
    c = CohortResult(second=T0, rows_in_second=1,
                     moved_in_second=1 if persisted else 0, moved_next_second=1)
    r = ProbeAResult(side="t", n_cohorts=1, cohorts=[c])
    return IsolationResult(second=T0, result=r, later_finding=later,
                           earlier_finding=earlier)


@pytest.mark.parametrize("kw,klass", [
    (dict(persisted=True), "CONFIRMED"),
    (dict(later=True, earlier=False), "CONFIRMED (lookahead)"),
    (dict(later=True, earlier=True), "CONFIRMED (lookahead)"),
    (dict(later=False, earlier=True), "INTERFERENCE"),
    (dict(later=False, earlier=False), "BATCHED ONLY"),
])
def test_the_CLASS_RULE(kw, klass):
    assert _iso(**kw).klass == klass


def test_a_non_persisting_finding_WITHOUT_the_split_is_not_classed_BATCHED_ONLY():
    """R271 §5: a batched-only finding classed without the split is a halt."""
    with pytest.raises(ValueError):
        _iso().klass


# --------------------------------------------------------------------------
# the cap, and complete
# --------------------------------------------------------------------------

def test_the_cap_prints_its_ARITHMETIC_and_its_PREDICTION_before_running(work, capsys):
    _run(work, "leaky", "--stride", "3", "--confirm")
    out = capsys.readouterr().out
    plan = out.index("CONFIRM PLANNED")
    assert plan < out.index("CONFIRM SUMMARY")
    assert "107.8 s" in out[plan:plan + 600], out[plan:plan + 600]


def test_ABOVE_THE_CAP_the_rest_are_NOT_RE_PROBED_and_first_and_last_are_in(
        work, capsys):
    _run(work, "leaky", "--stride", "3", "--confirm", "--confirm-cap", "2")
    out = capsys.readouterr().out
    got = _seconds(out, "CONFIRMED")
    assert len(got) == 2
    assert "over the cap of 2" in out
    m = re.search(r"NOT RE-PROBED: (\d+) batched finding", out)
    assert m and int(m.group(1)) >= 8
    assert got[0] < got[1]


def test_COMPLETE_and_confirm_together(work, capsys):
    code = _run(work, "leaky", "--complete", "--confirm", "--confirm-cap", "3")
    out = capsys.readouterr().out
    assert code == cli.EXIT_FINDINGS
    assert len(_seconds(out, "CONFIRMED")) == 3
    assert "COMPLETE RUN PLANNED" in out


# --------------------------------------------------------------------------
# refusals
# --------------------------------------------------------------------------

def test_confirm_WITHOUT_model_is_refused(work, capsys):
    assert _run(work, "leaky", "--confirm", model=False) == cli.EXIT_USAGE
    assert "--confirm needs --model" in capsys.readouterr().err


def test_a_cap_WITHOUT_confirm_is_refused(work, capsys):
    assert _run(work, "leaky", "--confirm-cap", "5") == cli.EXIT_USAGE
    assert "--confirm-cap without --confirm" in capsys.readouterr().err


def test_a_cap_BELOW_ONE_is_refused(work, capsys):
    assert _run(work, "leaky", "--confirm", "--confirm-cap", "0") == cli.EXIT_USAGE
    assert "--confirm-cap" in capsys.readouterr().err
