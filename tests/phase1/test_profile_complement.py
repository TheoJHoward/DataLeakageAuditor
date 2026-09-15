"""A profile's population, MEASURED, and its print, TOTAL. R274 §2(d).

`test_config_key_complement.py` places every key a model file accepts in one of
three states. A profile is a second input with its own population: the
`--profile` flag, and every key a user could write into a profile file, which is
every key the model file knows. Each is MEASURED AS READ when a run takes it from
a profile, DECLARED UNCONSUMED with a reason, or DECLARED REFUSED -- the loader
rejects a profile carrying it, naming it. Read-and-ignored is not legal.

AND THE PRINT IS TOTAL. The keys a profile filled are exactly the keys printed
"from profile", and the keys the model file overrode are exactly those printed
"overriding" -- a filled value with no line is a value landing silently.
"""
from __future__ import annotations

import argparse
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

import leakaudit.model_file as mf                                 # noqa: E402
from leakaudit import cli                                         # noqa: E402
from leakaudit.availability import AvailabilityModel              # noqa: E402

#: Where each read member's value rests, so the trace can watch it fetched.
ATTR = {
    "--profile":            ("args", "profile"),
    "decision_timezone":    ("model", "decision_timezone"),
    "window_seconds":       ("model", "window"),
    "ties_available":       ("model", "ties_available"),
    "bar_duration_seconds": ("config", "bar_duration"),
}

DECLARED_UNCONSUMED = {
    "version": (
        "consumed INSIDE the profile loader, which refuses any profile not at "
        "version 5: it decides whether the profile is read at all, and nothing "
        "reads it afterwards because nothing should."),
}

_STRUCTURAL = ("a profile NEVER supplies it and the loader refuses it with its "
               "own message: it describes the user's data, not the world the "
               "data came from, so it stays in the model file (R269 section 3).")
_OUTSIDE = ("not a world-facing key with a consumer, so the loader refuses a "
            "profile carrying it and lists the four a profile may carry; "
            "accepted, it would be loaded and ignored.")


def model_file_keys() -> set:
    keys = set()
    for v in mf._KEYS_BY_VERSION.values():
        keys |= set(v)
    return keys


DECLARED_REFUSED = {
    k: (_STRUCTURAL if k in mf.PROFILE_NEVER else _OUTSIDE)
    for k in sorted(model_file_keys() - set(mf.PROFILE_KEYS) - {"version"})
}

POPULATION = {"--profile"} | model_file_keys()

#: Distinct from every default, so a value read is visibly the profile's.
VALUES = {"decision_timezone": "UTC", "window_seconds": 2.0,
          "ties_available": False, "bar_duration_seconds": 3.0}
EXPLICIT = {"decision_timezone": "UTC", "window_seconds": 1.0,
            "ties_available": True, "bar_duration_seconds": 1.0}
FROM = re.compile(r"^\s*-?\s*(\w+): .+ from profile \S+\s*$", re.M)
OVER = re.compile(r"^\s*-?\s*(\w+): .+ from the model file, overriding profile "
                  r"\S+ \(.+\)\s*$", re.M)


@pytest.fixture
def work(tmp_path):
    secs = pd.date_range("2026-06-06 08:00:00", periods=80, freq="1s")
    rng = np.random.default_rng(11)
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


def _files(tmp, explicit=()):
    model = dict({"version": 5, "aggregate_frames": {"agg": "k"},
                  "decision_column": "timestamp"},
                 **{k: EXPLICIT[k] for k in explicit})
    (tmp / "m.json").write_text(json.dumps(model), encoding="utf-8")
    (tmp / "prof.json").write_text(json.dumps(dict({"version": 5}, **VALUES)),
                                   encoding="utf-8")
    return tmp / "m.json", tmp / "prof.json"


def _run(tmp, m, prof):
    return cli.main(["run", "--pipeline", "p:build",
                     "--frame", "snap=%s" % (tmp / "snap.csv"),
                     "--frame", "agg=%s" % (tmp / "agg.csv"),
                     "--model", str(m), "--profile", str(prof)])


def _measure_read(tmp) -> set:
    """Run end to end, every profile key FROM THE PROFILE; return what is fetched."""
    read: set = set()

    def install(cls, kind):
        original = cls.__getattribute__

        def watching(self, name):
            for k, (kd, at) in ATTR.items():
                if kd == kind and at == name:
                    read.add(k)
            return original(self, name)

        cls.__getattribute__ = watching
        return original

    m, prof = _files(tmp)
    a = install(mf.LoadedConfig, "config")
    b = install(AvailabilityModel, "model")
    c = install(argparse.Namespace, "args")
    try:
        _run(tmp, m, prof)
    finally:
        mf.LoadedConfig.__getattribute__ = a
        AvailabilityModel.__getattribute__ = b
        argparse.Namespace.__getattribute__ = c
    return read


# --------------------------------------------------------------------------
# the population, in three states
# --------------------------------------------------------------------------

def test_the_THREE_STATES_are_DISJOINT_and_cover_the_POPULATION():
    read_by_design = set(ATTR)
    assert not read_by_design & set(DECLARED_UNCONSUMED)
    assert not read_by_design & set(DECLARED_REFUSED)
    assert not set(DECLARED_UNCONSUMED) & set(DECLARED_REFUSED)
    assert read_by_design | set(DECLARED_UNCONSUMED) | set(DECLARED_REFUSED) == POPULATION
    assert set(ATTR) - {"--profile"} == set(mf.PROFILE_KEYS)


def test_every_READ_member_is_MEASURED_read_and_carries_the_PROFILE_value(work):
    read = _measure_read(work)
    unread = POPULATION - read
    unexplained = unread - set(DECLARED_UNCONSUMED) - set(DECLARED_REFUSED)
    assert not unexplained, (
        "accepted from a profile and NOTHING READS IT when the tool runs: %s"
        % sorted(unexplained))
    assert not read & (set(DECLARED_UNCONSUMED) | set(DECLARED_REFUSED)), read
    # Fetched, and what was fetched is the profile's: the model file set none.
    m, prof = _files(work)
    cfg = mf.load_model(m, profile=prof)
    assert cfg.model.decision_timezone == "UTC"
    assert cfg.model.window == pd.Timedelta(seconds=2)
    assert cfg.model.ties_available is False
    assert cfg.bar_duration == pd.Timedelta(seconds=3)


@pytest.mark.parametrize("key", sorted(DECLARED_REFUSED))
def test_every_REFUSED_key_is_refused_BY_NAME(tmp_path, key):
    p = tmp_path / "p.json"
    p.write_text(json.dumps({"version": 5, "window_seconds": 1.0, key: "x"}),
                 encoding="utf-8")
    with pytest.raises(mf.ModelFileError) as e:
        mf.load_profile(p)
    assert "`%s`" % key in str(e.value), str(e.value)
    assert len(DECLARED_REFUSED[key]) > 60


def test_the_UNCONSUMED_version_is_consumed_by_the_LOADER(tmp_path):
    p = tmp_path / "p.json"
    p.write_text(json.dumps({"window_seconds": 1.0}), encoding="utf-8")
    with pytest.raises(mf.ModelFileError):
        mf.load_profile(p)
    assert len(DECLARED_UNCONSUMED["version"]) > 60


# --------------------------------------------------------------------------
# the print, total
# --------------------------------------------------------------------------

@pytest.mark.parametrize("explicit", [(), ("window_seconds",),
                                      ("ties_available", "bar_duration_seconds"),
                                      tuple(mf.PROFILE_KEYS)])
def test_FILLED_equals_PRINTED_from_profile_and_OVERRIDDEN_equals_PRINTED_overriding(
        work, capsys, explicit):
    m, prof = _files(work, explicit)
    _run(work, m, prof)
    out = capsys.readouterr().out
    cfg = mf.load_model(m, profile=prof)
    filled, overridden = set(cfg.profile_filled), set(cfg.profile_overridden)
    assert filled == set(FROM.findall(out)), out[:3000]
    assert overridden == set(OVER.findall(out)), out[:3000]
    assert filled | overridden == set(VALUES) and not filled & overridden
    assert overridden == set(explicit)
