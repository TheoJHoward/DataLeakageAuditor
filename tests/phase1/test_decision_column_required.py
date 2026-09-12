"""An undeclared decision column produced a false silence. R235 §1.

**THE MEASUREMENT THAT MADE THIS A DEFECT RATHER THAN A GAP.** One frame set, one
pipeline, two model files differing only in whether `decision_column` was
declared:

    undeclared -> the loader defaulted to "timestamp" -> observed_silence, exit 0
    declared   -> 3 findings, exit 1

**A real leak reported as `observed_silence`** — the tool's affirmative *"I looked
over a stated population and found nothing. This is evidence."* Not a crash and
not a warning: the wrong answer in the tool's most confident state, because a
column happened to be called `timestamp` and sat two seconds from the true
decision instant.

**AND THE GUARD THAT FIRED ON A CRUDER VERSION IS NOT A CHECK ON THIS.** With the
wrong clock a whole hour away, `frame matched NO corrupted second` refuses — but
that guard exists for timezone and resolution mismatch and fires only because
nothing overlapped. **Two seconds is enough to defeat it**, and two seconds is the
realistic error: a load stamp beside an event stamp, a column named plausibly.

**WHY THE POSITIVE IS THE OVERLAPPING CASE AND NOT THE HOUR.** A test built on the
hour-apart frames would have passed before the fix, because the downstream guard
caught it — a positive every plausible wrong implementation also survives. R215
§0's refinement: the discriminating case is the one where the existing machinery
does *not* save you.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                        # noqa: E402
from leakaudit.model_file import FILL_ME, ModelFileError, load_model  # noqa: E402

PIPE = "decisioncol_pipeline"
BUILD = (
    "import pandas as pd\n"
    "def build(frames):\n"
    "    o = frames['dec'].copy()\n"
    "    o['timestamp'] = pd.to_datetime(o['timestamp'])\n"
    "    o['decided_at'] = pd.to_datetime(o['decided_at'])\n"
    "    a = frames['agg'].copy()\n"
    "    a['sec'] = pd.to_datetime(a['k']).dt.floor('1s')\n"
    "    o['sec'] = o['decided_at'].dt.floor('1s')\n"
    "    o['x'] = o['sec'].map(a.set_index('sec')['v']).fillna(0)\n"
    "    return o[['timestamp', 'decided_at', 'q', 'x']]\n")


@pytest.fixture
def work(tmp_path, monkeypatch):
    """Two clocks that OVERLAP. `timestamp` is two seconds early; same range,
    same resolution, same timezone. Nothing about it looks wrong."""
    secs = pd.date_range("2026-04-01 08:00:00", periods=200, freq="1s")
    rng = np.random.default_rng(5)
    pd.DataFrame({"k": secs, "v": rng.standard_normal(200)}).to_csv(
        tmp_path / "agg.csv", index=False)
    pd.DataFrame({
        "timestamp": secs + pd.Timedelta(milliseconds=300)
        - pd.Timedelta(seconds=2),
        "decided_at": secs + pd.Timedelta(milliseconds=300),
        "q": rng.standard_normal(200),
    }).to_csv(tmp_path / "dec.csv", index=False)
    (tmp_path / (PIPE + ".py")).write_text(BUILD, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    # TB-26: a fixture that names a module must assume another fixture named it
    # too. `sys.modules` caches by name, not path.
    yield tmp_path
    sys.modules.pop(PIPE, None)


def _model(work, name, obj):
    p = work / name
    p.write_text(json.dumps(obj), encoding="utf-8")
    return str(p)


def _run(work, model):
    argv = ["run", "--pipeline", PIPE + ":build",
            "--frame", "agg=%s" % (work / "agg.csv"),
            "--frame", "dec=%s" % (work / "dec.csv"), "--model", model]
    try:
        return cli.main(argv), ""
    except SystemExit as e:
        return (e.code if isinstance(e.code, int) else 2), str(e)


BASE = {"version": 3, "aggregate_frames": {"agg": "k"}, "window_seconds": 1.0}


def test_the_TRUE_clock_finds_three(work, capsys):
    """The other half of the pair. Without this, the refusal below could be
    refusing a frame set that has nothing to find."""
    rc, msg = _run(work, _model(work, "true.json",
                                dict(BASE, decision_column="decided_at")))
    assert rc == cli.EXIT_FINDINGS, msg
    text = capsys.readouterr().out
    assert "3 finding(s)" in text, text[:600]


def test_an_UNDECLARED_decision_column_is_REFUSED_not_defaulted(work):
    """What this replaces: the same file produced `observed_silence`, exit 0."""
    rc, msg = _run(work, _model(work, "none.json", dict(BASE)))
    assert rc == cli.EXIT_USAGE, "the audit ran without a declared clock"
    assert "no decision column is declared" in msg
    assert "observed_silence" in msg


def test_the_WRONG_clock_declared_EXPLICITLY_still_runs(work, capsys):
    """THE POINT IS NOT THAT `timestamp` IS FORBIDDEN. A user may declare it and
    be wrong; that is a declaration this tool cannot check, and it is a different
    thing from a default nobody chose. What the fix removes is the silent pick,
    not the user's freedom to be mistaken."""
    rc, _ = _run(work, _model(work, "wrong.json",
                              dict(BASE, decision_column="timestamp")))
    # EXIT_INCOMPLETE_SILENT is a way of running, not a failure of it: since
    # R268 §3 a default-stride run that finds nothing exits incomplete, and that
    # is the declared clock producing whatever that clock produces.
    assert rc in (cli.EXIT_OK_SILENT, cli.EXIT_INCOMPLETE_SILENT,
                  cli.EXIT_FINDINGS, cli.EXIT_USAGE)
    if rc in (cli.EXIT_OK_SILENT, cli.EXIT_INCOMPLETE_SILENT):
        text = capsys.readouterr().out
        assert "observed_silence" in text, (
            "declaring the wrong clock should still produce whatever that clock "
            "produces -- the user's declaration is theirs")


def test_the_refusal_does_NOT_fire_without_an_availability_model(work):
    """Scope. `leakaudit check` needs no decision instant, so demanding one
    would be friction with no purchase."""
    c = load_model(_model(work, "checks.json",
                          {"version": 3, "label_column": "q"}))
    assert not c.has_availability_model


def test_a_DRAFTED_file_scaffolds_the_decision_column(work):
    """R235 §1: the skeleton gains the field, so the refusal names a place that
    exists in the file."""
    from leakaudit.inference import draft, write_draft
    frames = {"agg": pd.read_csv(work / "agg.csv"),
              "dec": pd.read_csv(work / "dec.csv")}
    out = work / "drafted.json"
    write_draft(draft(frames), out, generated_by="t", commit="c",
                source_frames={k: (len(v), len(v.columns))
                               for k, v in frames.items()})
    body = json.loads(out.read_text(encoding="utf-8"))
    assert body["decision_column"] == FILL_ME
    ev = body["draft_provenance"]["column_mode_evidence"]
    assert "(decision) decision_column" in ev
    assert "never runs your pipeline" in ev["(decision) decision_column"], (
        "the evidence does not say why the draft cannot name candidates, which "
        "is the honest half: it reads frames and has not seen the output")


def test_the_drafted_sentinel_is_refused_by_the_loader(work):
    with pytest.raises(ModelFileError) as e:
        load_model(_model(work, "sent.json",
                          dict(BASE, decision_column=FILL_ME)))
    assert "UNFILLED FIELD, NOT A COLUMN NAME" in str(e.value)
