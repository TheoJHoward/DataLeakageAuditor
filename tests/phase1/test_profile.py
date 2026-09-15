"""A profile: the user's own named declaration, printed per key. R274 §2.

A profile is a file the user writes, in the model file's format at version 5,
carrying only the four world-facing keys something reads today. It is not a
default. Every value it supplies prints in ABOUT THIS RUN as "from profile
<name>", a key the model file also sets is taken from the model file and printed
as overriding it with both values, and a profile never supplies the decision
column, a frame, the label or the split.

THE PAIR, three ways. HELD: frames, builder, model file. VARIED: the profile --
none, one with no override, the same one under one explicit key.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import leakaudit.model_file as mf                                 # noqa: E402
from leakaudit import cli                                         # noqa: E402

FOUR = {"decision_timezone": "UTC", "window_seconds": 2.0,
        "ties_available": True, "bar_duration_seconds": 3.0}
FROM = re.compile(r"^\s*-?\s*(\w+): (.+) from profile (\S+)\s*$", re.M)
OVER = re.compile(r"^\s*-?\s*(\w+): (.+) from the model file, overriding "
                  r"profile (\S+) \((.+)\)\s*$", re.M)


@pytest.fixture
def work(tmp_path):
    secs = pd.date_range("2026-06-06 08:00:00", periods=80, freq="1s")
    rng = np.random.default_rng(7)
    pd.DataFrame({"timestamp": [s + pd.Timedelta(milliseconds=300) for s in secs],
                  "q": rng.standard_normal(80)}).to_csv(tmp_path / "snap.csv",
                                                        index=False)
    pd.DataFrame({"k": secs, "v": rng.standard_normal(80)}).to_csv(
        tmp_path / "agg.csv", index=False)
    (tmp_path / "p.py").write_text(
        "import pandas as pd\n"
        "def build(f):\n"
        "    o = f['snap'].copy()\n"
        "    o['sec'] = pd.to_datetime(o['timestamp']).dt.floor('1s')\n"
        "    a = f['agg'].copy(); a['sec'] = pd.to_datetime(a['k'])\n"
        "    o['x'] = o['sec'].map(a.set_index('sec')['v']).to_numpy()\n"
        "    return o[['timestamp', 'x']]\n", encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    yield tmp_path
    sys.path.remove(str(tmp_path))


def _model(tmp, **extra):
    p = tmp / "m.json"
    p.write_text(json.dumps(dict({"version": 5, "aggregate_frames": {"agg": "k"},
                                  "decision_column": "timestamp"}, **extra)),
                 encoding="utf-8")
    return p


def _profile(tmp, doc, name="mine"):
    p = tmp / ("%s.json" % name)
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def _run(tmp, model, *extra):
    return cli.main(["run", "--pipeline", "p:build",
                     "--frame", "snap=%s" % (tmp / "snap.csv"),
                     "--frame", "agg=%s" % (tmp / "agg.csv"),
                     "--model", str(model), *extra])


# --------------------------------------------------------------------------
# the three print cases, R274 §2(f)
# --------------------------------------------------------------------------

def test_a_profile_with_NO_override_prints_FOUR_from_profile_lines(work, capsys):
    prof = _profile(work, dict({"version": 5}, **FOUR))
    _run(work, _model(work), "--profile", str(prof))
    out = capsys.readouterr().out
    lines = FROM.findall(out)
    assert [k for k, _v, _n in lines] == list(mf.PROFILE_KEYS), out[:3000]
    assert {n for _k, _v, n in lines} == {"mine"}
    assert ('window_seconds', '2.0', 'mine') in lines
    assert not OVER.findall(out)
    assert out.index("from profile mine") > out.index("ABOUT THIS RUN")


def test_ONE_explicit_key_prints_THREE_and_ONE_overriding(work, capsys):
    prof = _profile(work, dict({"version": 5}, **FOUR))
    model = _model(work, window_seconds=1.0)
    _run(work, model, "--profile", str(prof))
    out = capsys.readouterr().out
    assert len(FROM.findall(out)) == 3, out[:3000]
    assert "window_seconds" not in {k for k, _v, _n in FROM.findall(out)}
    assert OVER.findall(out) == [("window_seconds", "1.0", "mine", "2.0")], out[:3000]
    # EXPLICIT WINS, in the value the probe gets and not only in the print.
    cfg = mf.load_model(model, profile=prof)
    assert cfg.model.window == pd.Timedelta(seconds=1)
    assert cfg.bar_duration == pd.Timedelta(seconds=3)


def test_a_run_WITHOUT_a_profile_prints_NONE(work, capsys):
    _run(work, _model(work))
    out = capsys.readouterr().out
    assert "ABOUT THIS RUN" in out
    assert not FROM.findall(out) and not OVER.findall(out)
    assert "profile" not in out.lower()


def test_QUIET_still_prints_every_profile_line(work, capsys):
    prof = _profile(work, dict({"version": 5}, **FOUR))
    _run(work, _model(work), "--profile", str(prof), "--quiet")
    out = capsys.readouterr().out
    assert "ABOUT THIS RUN" not in out
    assert len(FROM.findall(out)) == 4, out


# --------------------------------------------------------------------------
# the four refusals, R274 §2(c), each shown to fire
# --------------------------------------------------------------------------

@pytest.mark.parametrize("key", ["note", "column_modes", "draft_provenance",
                                 "timestamp_column", "skip_intervals"])
def test_a_key_OUTSIDE_the_list_is_REFUSED_and_the_LIST_is_named(tmp_path, key):
    prof = _profile(tmp_path, {"version": 5, "window_seconds": 1.0, key: "x"})
    with pytest.raises(mf.ModelFileError) as e:
        mf.load_profile(prof)
    msg = str(e.value)
    assert "`%s`" % key in msg and "not a key a profile may carry" in msg, msg
    for allowed in mf.PROFILE_KEYS:
        assert "`%s`" % allowed in msg, msg


@pytest.mark.parametrize("key", mf.PROFILE_NEVER)
def test_a_STRUCTURAL_key_gets_ITS_OWN_refusal(tmp_path, key):
    prof = _profile(tmp_path, {"version": 5, "window_seconds": 1.0, key: "x"})
    with pytest.raises(mf.ModelFileError) as e:
        mf.load_profile(prof)
    msg = str(e.value)
    assert "never supplies `%s`" % key in msg, msg
    assert "not a key a profile may carry" not in msg, "not the generic message"


def test_a_profile_path_that_DOES_NOT_RESOLVE_is_REFUSED(work):
    with pytest.raises(mf.ModelFileError) as e:
        mf.load_profile(work / "absent.json")
    assert "names no file that exists" in str(e.value)
    with pytest.raises(SystemExit) as e:
        _run(work, _model(work), "--profile", str(work / "absent.json"))
    assert "names no file that exists" in str(e.value)


@pytest.mark.parametrize("version", [4, 6, "5", None])
def test_a_profile_at_the_WRONG_SCHEMA_VERSION_is_REFUSED(tmp_path, version):
    doc = {"window_seconds": 1.0}
    if version is not None:
        doc["version"] = version
    with pytest.raises(mf.ModelFileError) as e:
        mf.load_profile(_profile(tmp_path, doc))
    assert "read at schema version 5" in str(e.value), str(e.value)


# --------------------------------------------------------------------------
# the edges of the mechanism
# --------------------------------------------------------------------------

def test_a_profile_carrying_NONE_of_the_four_is_REFUSED(tmp_path):
    with pytest.raises(mf.ModelFileError) as e:
        mf.load_profile(_profile(tmp_path, {"version": 5}))
    assert "fill nothing" in str(e.value)


def test_a_profile_VALUE_takes_the_model_file_s_own_check(tmp_path):
    prof = _profile(tmp_path, {"version": 5, "window_seconds": 0})
    with pytest.raises(mf.ModelFileError) as e:
        mf.load_profile(prof)
    assert str(prof) in str(e.value) and "`window_seconds`" in str(e.value)


def test_PROFILE_without_MODEL_is_REFUSED(work, capsys):
    prof = _profile(work, dict({"version": 5}, **FOUR))
    code = cli.main(["run", "--pipeline", "p:build",
                     "--frame", "agg=%s" % (work / "agg.csv"),
                     "--profile", str(prof)])
    assert code == cli.EXIT_USAGE
    assert "--profile needs --model" in capsys.readouterr().err


def test_a_config_WITHOUT_a_profile_carries_no_profile_state(work):
    cfg = mf.load_model(_model(work))
    assert cfg.profile_name is None and mf.profile_lines(cfg) == []


# --------------------------------------------------------------------------
# the template, R274 §2(e)
# --------------------------------------------------------------------------

def test_the_TEMPLATE_loads_and_carries_exactly_the_FOUR_keys():
    prof = mf.load_profile(mf.TEMPLATE_PATH)
    assert prof.name == "TEMPLATE"
    assert set(prof.values) == set(mf.PROFILE_KEYS)


def test_the_TEMPLATE_is_printed_by_leakaudit_schema():
    text = mf.TEMPLATE_PATH.read_text(encoding="utf-8")
    lines = text.strip().splitlines()
    assert len(lines) >= 4, "the template's lines are this assertion's population"
    for line in lines:
        assert "    " + line in mf.SCHEMA_DOC, line
    assert "not found" not in mf.SCHEMA_DOC


def test_the_TEMPLATE_is_the_ONLY_profile_in_the_repository():
    """A JSON object whose keys beyond `version` are all profile keys is a
    profile, whatever it is called. Tracked and untracked files both."""
    names = set()
    for args in (["ls-files"], ["ls-files", "--others", "--exclude-standard"]):
        r = subprocess.run(["git", "-C", str(ROOT), *args, "*.json"],
                           capture_output=True, text=True, encoding="utf-8")
        assert r.returncode == 0, r.stderr
        names |= {l.strip() for l in r.stdout.splitlines() if l.strip()}
    assert len(names) > 10, "the population is this repository's JSON files"
    profiles = []
    for rel in sorted(names):
        p = ROOT / rel
        if not p.is_file() or p.stat().st_size > 1_000_000:
            continue
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError):
            continue
        if isinstance(doc, dict):
            rest = set(doc) - {"version"}
            if rest and rest <= set(mf.PROFILE_KEYS):
                profiles.append(rel.replace("\\", "/"))
    assert profiles == ["src/leakaudit/templates/TEMPLATE.json"], profiles
