"""`--confirm`: every batched finding re-probed alone, and classed. R270 §2(b).

THE PAIR. HELD: the frames, the model, `--stride 3`, `--confirm`. VARIED: the
builder alone.

  * `leaky` reads its own second's cell, unavailable at the decision instant.
    Every batched finding is the cohort's own, and every one is CONFIRMED.
  * `lagpatch` reads the previous second's cell -- available -- except on
    decision seconds 50..58, where it reads three seconds back, still
    available. The default reach control samples seconds 15, 30 and 45, which
    see only the one-second lookback, so stride 3 clears the measured reach.
    Inside the patch a row reads the cell corrupted for the cohort three
    seconds earlier and the batch reports false findings at 51, 54 and 57.
    Probed alone, none of them is a finding: all BATCHED ONLY, none dropped.

The patch stands in for the reading R270 §1(c) tests on the fixture: a builder
whose reach somewhere exceeds what a lower-bound measurement saw.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                      # noqa: E402

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
    "def lagpatch(frames):\n"
    "    agg, out = _prep(frames)\n"
    "    v = pd.Series(agg['v'].to_numpy(), index=agg['k'])\n"
    "    s = out['d'].dt.floor('s')\n"
    "    idx = ((s - s.min()) / pd.Timedelta(seconds=1)).astype(int)\n"
    "    lag = pd.Series(np.where((idx >= 50) & (idx <= 58), 3, 1), index=s.index)\n"
    "    out['feat'] = (s - pd.to_timedelta(lag, unit='s')).map(v)\n"
    "    return out\n")


@pytest.fixture
def work(tmp_path):
    name = "r270_confirm_pipe"
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


#: Notes render as `  - <text>`; a class line is one whose text STARTS with the
#: tag, so "NOT CONFIRMED" inside a BATCHED ONLY line is not counted as one.
_LEAD = r"^[ \t]*-?[ \t]*"


def _count(out, tag):
    return len(re.findall(_LEAD + r"%s\s" % re.escape(tag), out, re.M))


# --------------------------------------------------------------------------
# the pair
# --------------------------------------------------------------------------

def test_LEAKY_every_batched_finding_is_CONFIRMED(work, capsys):
    code = _run(work, "leaky", "--stride", "3", "--confirm")
    out = capsys.readouterr().out
    assert code == cli.EXIT_FINDINGS
    confirmed = _count(out, "CONFIRMED")
    assert confirmed >= 10, out[-3000:]
    assert _count(out, "BATCHED ONLY -- NOT CONFIRMED") == 0
    assert "CONFIRM SUMMARY: %d confirmed, 0 batched only, 0 not re-probed" % confirmed in out


def test_LAGPATCH_batched_interference_is_BATCHED_ONLY_and_KEPT(work, capsys):
    code = _run(work, "lagpatch", "--stride", "3", "--confirm")
    out = capsys.readouterr().out
    only = re.findall(r"BATCHED ONLY -- NOT CONFIRMED\s+(\S+ \S+):", out)
    assert only == ["2026-01-01 00:00:51", "2026-01-01 00:00:54",
                    "2026-01-01 00:00:57"], out[-3000:]
    assert _count(out, "CONFIRMED") == 0
    assert "CONFIRM SUMMARY: 0 confirmed, 3 batched only, 0 not re-probed, of 3" in out
    assert code == cli.EXIT_FINDINGS, (
        "a finding that failed isolation is kept and counted, not dropped")


def test_WITHOUT_confirm_the_same_run_prints_no_classes(work, capsys):
    _run(work, "lagpatch", "--stride", "3")
    out = capsys.readouterr().out
    assert "CONFIRM" not in out


# --------------------------------------------------------------------------
# the cap, and complete
# --------------------------------------------------------------------------

def test_ABOVE_THE_CAP_the_rest_are_NOT_RE_PROBED_and_first_and_last_are_in(
        work, capsys):
    _run(work, "leaky", "--stride", "3", "--confirm", "--confirm-cap", "2")
    out = capsys.readouterr().out
    got = re.findall(_LEAD + r"CONFIRMED\s+(\S+ \S+):", out, re.M)
    assert len(got) == 2
    assert "over the cap of 2" in out
    m = re.search(r"NOT RE-PROBED: (\d+) batched finding", out)
    assert m and int(m.group(1)) >= 8
    assert got[0] < got[1]


def test_COMPLETE_and_confirm_together(work, capsys):
    code = _run(work, "leaky", "--complete", "--confirm", "--confirm-cap", "3")
    out = capsys.readouterr().out
    assert code == cli.EXIT_FINDINGS
    assert _count(out, "CONFIRMED") == 3
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
