"""`--confirm`: isolation, then the split, each predicted; interference is its own exit.

R271 §3, R272 §2(d)(e). Isolation removes a real lookahead leak as surely as it
removes interference: a row at F reading a LATER cohort's unavailable cells moves
in the batch and not alone. So `--confirm` runs in two stages, each predicted
before it runs. Stage one isolates up to the cap. Stage two splits every finding
that vanished -- with the batch's later cohorts only, and with its earlier ones
only -- up to the same cap, and any vanished finding above it is listed as NOT
RE-PROBED with the count, never silently left.

THE PAIRS. HELD: the frames, the model, `--stride 3`, `--confirm`. VARIED: the
builder alone.

  * `leaky` reads its own second's cell. Every finding persists alone:
    CONFIRMED, exit 1.
  * `lagpatch` reads the previous second's cell -- available -- except on
    decision seconds 50..58, where it reads three seconds BACK, still available.
    The batch reports false findings at 51, 54 and 57; alone they vanish; with
    the earlier cohorts they return. INTERFERENCE, every silence `none`, exit 5.
  * `lookahead` reads the previous second except on 50..58, where it reads
    three seconds AHEAD -- unavailable. The batch reports 51 and 54; alone they
    vanish; with the later cohorts they return. CONFIRMED (lookahead), naming the
    later second, exit 1.
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
    name = "r272_confirm_pipe"
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
#: tag and then names a second.
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
            "interference, 0 batched only, 15 not re-probed, "
            "of 20") in out
    assert "CONFIRM STAGE 2 PLANNED" not in out, "nothing vanished, nothing to split"


def test_LAGPATCH_is_INTERFERENCE_and_EXITS_INTERFERENCE(work, capsys):
    code = _run(work, "lagpatch", "--stride", "3", "--confirm")
    cap = capsys.readouterr()
    out = cap.out
    assert _seconds(out, "INTERFERENCE") == [
        "2026-01-01 00:00:51", "2026-01-01 00:00:54", "2026-01-01 00:00:57"], out[-3000:]
    assert not _seconds(out, "CONFIRMED")
    assert "every silence in this run is none(interference detected at stride 3" in out
    assert code == cli.EXIT_INTERFERENCE == 5, (
        "interference is its own exit, not a usage error")
    assert "RUN INTERFERED" in cap.err


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
# the two stages, each predicted before it runs
# --------------------------------------------------------------------------

def test_STAGE_ONE_prints_its_prediction_and_arithmetic_before_running(work, capsys):
    _run(work, "leaky", "--stride", "3", "--confirm")
    out = capsys.readouterr().out
    plan = out.index("CONFIRM STAGE 1 PLANNED")
    assert plan < out.index("CONFIRM SUMMARY")
    assert "107.8 s" in out[plan:plan + 600], out[plan:plan + 600]


def test_STAGE_TWO_prints_N_VANISHED_and_its_cost_before_running(work, capsys):
    _run(work, "lagpatch", "--stride", "3", "--confirm")
    out = capsys.readouterr().out
    m = re.search(r"CONFIRM STAGE 2 PLANNED: (\d+) vanished; split (\d+) of them "
                  r"\(cap (\d+)\) at two re-probes each, ~([\d.]+) min", out)
    assert m, out[-3000:]
    assert (m.group(1), m.group(2), m.group(3)) == ("3", "3", "5")
    assert out.index("CONFIRM STAGE 1 PLANNED") < m.start() < out.index("CONFIRM SUMMARY")


def test_a_vanished_finding_ABOVE_THE_SPLIT_CAP_is_NOT_RE_PROBED_with_the_count(
        work, capsys):
    _run(work, "lagpatch", "--stride", "3", "--confirm", "--confirm-cap", "1")
    out = capsys.readouterr().out
    assert "split 0 of them" not in out
    assert re.search(r"CONFIRM STAGE 2 PLANNED: 1 vanished; split 1 of them", out), out[-3000:]
    # the cap of 1 isolates one finding; with three findings, the two not
    # isolated are NOT RE-PROBED, and the one isolated is split
    assert "NOT RE-PROBED: 2 batched finding" in out, out[-3000:]
    assert len(_seconds(out, "INTERFERENCE")) == 1


def test_THE_SPLIT_INVARIANT_vanished_LE_isolated_LE_cap(work, capsys, monkeypatch):
    """R273 §1(d). A finding vanishes only from the isolated set, and stage one
    isolates at most the cap, so vanished <= isolated <= cap and every vanished
    finding is split. The branch that listed unsplit ones was dead by
    construction and is gone; this pins the invariant that made it dead."""
    import leakaudit.availability as av
    seen = {}
    real_iso, real_split = av.isolate_cohorts, av.split_isolated

    def iso_spy(*a, **k):
        r = real_iso(*a, **k)
        seen["isolated"] = len(r)
        return r

    def split_spy(raw, build, model, results, **k):
        seen["vanished"] = len(results)
        return real_split(raw, build, model, results, **k)

    monkeypatch.setattr(av, "isolate_cohorts", iso_spy)
    monkeypatch.setattr(av, "split_isolated", split_spy)
    for cap in (1, 2, 5):
        seen.clear()
        _run(work, "lagpatch", "--stride", "3", "--confirm", "--confirm-cap", str(cap))
        out = capsys.readouterr().out
        assert seen["vanished"] <= seen["isolated"] <= cap, (cap, seen)
        assert ("CONFIRM STAGE 2 PLANNED: %d vanished; split %d of them (cap %d)"
                % (seen["vanished"], seen["vanished"], cap)) in out, out[-3000:]
        assert "NOT RE-PROBED (split)" not in out and "not split" not in out


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
# the exit table, and its precedence in --help
# --------------------------------------------------------------------------

def test_THE_EXIT_TABLE(work, capsys):
    rows = [
        (("leaky", "--stride", "3"), cli.EXIT_FINDINGS),
        (("lagpatch", "--stride", "3", "--confirm"), cli.EXIT_INTERFERENCE),
        (("leaky", "--confirm"), None),     # without --model: refused, below
    ]
    got = []
    for args, want in rows[:2]:
        got.append((args, _run(work, *args), want))
    assert _run(work, "leaky", "--confirm", model=False) == cli.EXIT_USAGE
    capsys.readouterr()
    for args, code, want in got:
        assert code == want, (args, code, want)
    assert (cli.EXIT_OK_SILENT, cli.EXIT_FINDINGS, cli.EXIT_USAGE,
            cli.EXIT_NOTHING_PROBED, cli.EXIT_INCOMPLETE_SILENT,
            cli.EXIT_INTERFERENCE) == (0, 1, 2, 3, 4, 5)


def test_the_PRECEDENCE_is_in_the_run_help():
    helptext = None
    for action in cli.build_parser()._subparsers._group_actions:
        helptext = action.choices["run"].format_help()
    assert "2 refused" in helptext and "5 interference" in helptext
    order = [helptext.index(s) for s in ("2 refused", "5 interference",
                                          "1 findings", "4 incomplete", "0 clean")]
    assert order == sorted(order), helptext


# --------------------------------------------------------------------------
# the cap, and complete
# --------------------------------------------------------------------------

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
