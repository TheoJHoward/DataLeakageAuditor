"""A COMPLETE L3.1 run: passes at offsets, one shared reach. R268 §3(d).

The pair here is the ruling's own: HELD -- the frame, the builder, the model;
VARIED -- `--complete` alone. A default run is incomplete and exits so; the
same run made complete exits clean on a clean builder and still finds on a
leaky one. The library tests pin the three properties a complete run rests on:
offset 0 changes nothing for existing callers, the offsets between them cover
every second exactly once, and a shared reach is used rather than re-measured.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                      # noqa: E402
from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402

N = 300
T0 = pd.Timestamp("2026-01-01 00:00:00")
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")


def _frames():
    secs = pd.date_range(T0, periods=N, freq="1s")
    agg = pd.DataFrame({"k": secs,
                        "v": [float(i % 17) + 1.0 for i in range(N)]})
    dec = pd.DataFrame({"d": secs + pd.Timedelta(milliseconds=500),
                        "row": range(N)})
    return {"agg": agg, "dec": dec}


def _clean(frames):
    """Reads the PREVIOUS second, which has arrived by each decision."""
    agg = frames["agg"].copy()
    agg["k"] = pd.to_datetime(agg["k"])
    lookup = pd.Series(agg["v"].to_numpy(),
                       index=agg["k"] + pd.Timedelta(seconds=1))
    out = frames["dec"].copy()
    out["d"] = pd.to_datetime(out["d"])
    out["feat"] = out["d"].dt.floor("s").map(lookup)
    return out


def _seconds(res):
    return [c.second for c in res.cohorts]


# --------------------------------------------------------------------------
# the library properties
# --------------------------------------------------------------------------

def test_offset_ZERO_selects_exactly_what_the_default_selected():
    """Every existing caller, the whole-frame guard included, is unchanged."""
    kw = dict(side="t", cohort_stride=5, max_cohorts=10 ** 9, reach_samples=0)
    default = run_probe_a(_frames(), _clean, MODEL, **kw)
    zero = run_probe_a(_frames(), _clean, MODEL, cohort_offset=0, **kw)
    assert _seconds(default) == _seconds(zero)
    assert _seconds(default), "the comparison must be over a real selection"


def test_the_OFFSETS_between_them_probe_EVERY_second_EXACTLY_ONCE():
    S = 5
    seen = []
    for offset in range(S):
        r = run_probe_a(_frames(), _clean, MODEL, side="t", cohort_stride=S,
                        max_cohorts=10 ** 9, reach_samples=0,
                        cohort_offset=offset)
        seen.extend(_seconds(r))
    everything = sorted(_clean(_frames())["d"].dt.floor("s").unique())
    assert sorted(seen) == list(everything), "the passes cover every second"
    assert len(seen) == len(set(seen)), "and no second twice"


def test_a_SHARED_reach_is_USED_not_re_measured(monkeypatch):
    first = run_probe_a(_frames(), _clean, MODEL, side="t", max_cohorts=0)
    assert first.reach is not None and first.reach.measured is not None

    import leakaudit.reach as reach_mod

    def refuse(*a, **k):
        raise AssertionError("the reach was re-measured on a pass that was "
                             "handed a shared measurement")
    monkeypatch.setattr(reach_mod, "measure_reach", refuse)
    r = run_probe_a(_frames(), _clean, MODEL, side="t", cohort_stride=5,
                    max_cohorts=10 ** 9, cohort_offset=2, reach=first.reach)
    assert r.reach is first.reach
    assert any("[shared across a complete run's passes]" in n for n in r.notes)


# --------------------------------------------------------------------------
# the CLI pair: default vs --complete, everything else held
# --------------------------------------------------------------------------

PIPELINE = (
    "import pandas as pd\n"
    "\n"
    "def _prep(frames):\n"
    "    agg = frames['agg'].copy()\n"
    "    agg['k'] = pd.to_datetime(agg['k'])\n"
    "    out = frames['dec'].copy()\n"
    "    out['d'] = pd.to_datetime(out['d'])\n"
    "    return agg, out\n"
    "\n"
    "def clean(frames):\n"
    "    agg, out = _prep(frames)\n"
    "    lk = pd.Series(agg['v'].to_numpy(), index=agg['k'] + pd.Timedelta(seconds=1))\n"
    "    out['feat'] = out['d'].dt.floor('s').map(lk)\n"
    "    return out\n"
    "\n"
    "def leaky(frames):\n"
    "    agg, out = _prep(frames)\n"
    "    lk = pd.Series(agg['v'].to_numpy(), index=agg['k'])\n"
    "    out['feat'] = out['d'].dt.floor('s').map(lk)\n"
    "    return out\n")


@pytest.fixture
def work(tmp_path):
    name = "r268_complete_pipe"
    (tmp_path / (name + ".py")).write_text(PIPELINE, encoding="utf-8")
    fr = _frames()
    fr["agg"].to_csv(tmp_path / "agg.csv", index=False)
    fr["dec"].to_csv(tmp_path / "dec.csv", index=False)
    (tmp_path / "m.json").write_text(json.dumps({
        "version": 3, "aggregate_frames": {"agg": "k"},
        "decision_column": "d"}), encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield tmp_path, name
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(name, None)


def _run(work, fn, *extra):
    tmp, name = work
    return cli.main(["run", "--pipeline", "%s:%s" % (name, fn),
                     "--frame", "agg=%s" % (tmp / "agg.csv"),
                     "--frame", "dec=%s" % (tmp / "dec.csv"),
                     "--model", str(tmp / "m.json"), *extra])


def test_THE_PAIR_default_is_INCOMPLETE_and_complete_is_COMPLETE(work, capsys):
    """HELD: frame, builder, model. VARIED: `--complete` only."""
    assert _run(work, "clean") == cli.EXIT_INCOMPLETE_SILENT
    default_out = capsys.readouterr().out
    assert "COMPLETE: NO" in default_out

    assert _run(work, "clean", "--complete") == cli.EXIT_OK_SILENT
    complete_out = capsys.readouterr().out
    assert "COMPLETE: yes" in complete_out
    assert "L3.1 PASS BUDGET" in complete_out


def test_a_complete_run_STILL_FINDS_a_leak(work, capsys):
    """Completeness is not a softer instrument: a leaky builder still finds."""
    assert _run(work, "leaky", "--complete") == cli.EXIT_FINDINGS


def test_the_DEFAULT_run_prints_its_pass_budget_too(work, capsys):
    """§3(d): both budgets printed -- L3.1's in passes, L2a's in cohorts."""
    _run(work, "clean")
    out = capsys.readouterr().out
    assert "L3.1 PASS BUDGET: 1 of" in out


def test_a_complete_run_PREDICTS_its_remaining_time_after_pass_one(work, capsys):
    """R269 §0(a). The plan prints before any pass, and after pass one the time
    left prints as that pass's cost times the passes remaining. Both have to
    precede the verdict, or the warning arrives after the wait it warns of."""
    _run(work, "clean", "--complete")
    out = capsys.readouterr().out
    assert "COMPLETE RUN PLANNED" in out
    assert "pass(es) remaining" in out and "at this pass's cost" in out
    assert out.index("COMPLETE RUN PLANNED") < out.index("pass(es) remaining")
    assert out.index("pass(es) remaining") < out.index("COMPLETE: yes"), (
        "the prediction printed after the result, which is no prediction")
