"""The complement, MEASURED, as a standing guard. R217 §1.

WHAT THIS REPLACES. `test_no_key_is_read_and_ignored.py` holds a hand-written map
of key -> "consumed by X". A hand-written map is a claim about the code that
drifts from it, which is the failure this project keeps recording. This file
makes the same assertion by MEASUREMENT: it runs the tool end to end with every
key set, records which key-carrying attributes are actually fetched, and requires
every unfetched key to be declared unconsumed with a reason.

WHY MEASUREMENT AND NOT A GREP. A grep finds the string. The question is whether
the value is FETCHED when the tool runs, and three keys have now been found that
a grep would call present -- each was mentioned in the loader, validated, and
documented, while nothing read it.

THE TOTALITY SHAPE, which is the point. Exactly as `PROBE_PATH_SET.json`'s
on-path and off-path lists are disjoint and jointly cover every module on disk:
every key the loader accepts is in exactly one of THREE states, each with a
reason: MEASURED AS READ; `DECLARED_UNCONSUMED` -- it loads and nothing reads it,
deliberately; or `DECLARED_REFUSED` -- the loader rejects a file that sets it,
naming what to use instead. A key added to the loader without a classification
fails, so the defect found three times cannot reach a fourth. Accepted-and-
ignored is the one state that is not legal, and it is the whole subject here.

THE AS-FOUND POPULATION, recorded so the number is not a recollection. At commit
a023011, before the R216 fixes: 10 accepted, 5 read, 5 unread -- `column_modes`,
`ties_available`, `timestamp_column`, plus `note` and `version` which are
declared. At HEAD after R218: 10 accepted, 7 read, 3 unread -- two declared unconsumed
and one, `timestamp_column`, DECLARED REFUSED: R218 §2 made the loader reject a
file that sets it rather than accept and ignore it. **Zero unexplained**, so the
incremental discovery had reached the end -- which nobody could have known
without taking the complement.
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

import leakaudit.model_file as mf                                 # noqa: E402
from leakaudit import cli                                         # noqa: E402
from leakaudit.availability import AvailabilityModel              # noqa: E402

# Where each accepted key's value comes to rest, so the trace can watch it.
KEY_TO_ATTR = {
    "version":          ("config", "version"),
    "aggregate_frames": ("model", "aggregate_frames"),
    "decision_column":  ("model", "decision_column"),
    "window_seconds":   ("model", "window"),
    "ties_available":   ("model", "ties_available"),
    "label_column":     ("config", "label_column"),
    "split":            ("config", "train_idx"),
    "column_modes":     ("config", "column_modes"),
    "bar_duration_seconds": ("config", "bar_duration"),
    "note":             (None, None),
}

# THE THIRD STATE. A key kept in the version's key set specifically SO THAT the
# loader can refuse it with a message naming what to use instead -- rather than
# dropped from the set, which would give the generic unknown-key refusal and tell
# the user nothing. Refused is a legal classification; accepted-and-ignored is
# not, and the difference is the whole subject of this file.
DECLARED_REFUSED = {
    "timestamp_column": (
        "R218 §2. It reached nothing: each aggregate frame's clock is the key "
        "named for it in `aggregate_frames`, bound from the model and "
        "independent of this. Wiring it would give the probe two clocks per "
        "frame with nothing to arbitrate, so it is refused, and the refusal "
        "names `aggregate_frames` as what to use instead. D-V30A-50."),
}

# A key here is accepted, LOADS, and is deliberately not read at run time. Each
# entry is the REASON, and an entry without one is not a classification.
DECLARED_UNCONSUMED = {
    "version": (
        "consumed INSIDE the loader, which is where it belongs: it gates whether "
        "the file is read at all, and refuses a version this build does not "
        "know. Nothing reads it afterwards because nothing should."),
    "note": (
        "reader-only by design, and `leakaudit schema` says so. It exists for "
        "whoever opens the file next."),
}


def _measure_read_keys(tmp_path) -> set[str]:
    """Run the tool end to end with every key set; return the keys FETCHED."""
    read: set[str] = set()

    def install(cls, kind):
        original = cls.__getattribute__

        def watching(self, name):
            for k, (kd, at) in KEY_TO_ATTR.items():
                if kd == kind and at == name:
                    read.add(k)
            return original(self, name)

        cls.__getattribute__ = watching
        return original

    secs = pd.date_range("2026-06-06 08:00:00", periods=80, freq="1s")
    rng = np.random.default_rng(7)
    pd.DataFrame({"timestamp": [s + pd.Timedelta(milliseconds=300) for s in secs],
                  "q": rng.standard_normal(80)}).to_csv(tmp_path / "snap.csv",
                                                        index=False)
    pd.DataFrame({"k": secs, "v": rng.standard_normal(80),
                  "w": rng.standard_normal(80)}).to_csv(tmp_path / "agg.csv",
                                                        index=False)
    (tmp_path / "p.py").write_text(
        "import pandas as pd\n"
        "def build(f):\n"
        "    o = f['snap'].copy()\n"
        "    o['sec'] = pd.to_datetime(o['timestamp']).dt.floor('1s')\n"
        "    a = f['agg'].copy(); a['sec'] = pd.to_datetime(a['k'])\n"
        "    o['x'] = o['sec'].map(a.set_index('sec')['v']).to_numpy()\n"
        "    o['target'] = (o['x'] > 0).astype(int)\n"
        "    return o[['timestamp', 'x', 'target']]\n", encoding="utf-8")
    (tmp_path / "m.json").write_text(json.dumps({
        "version": 3, "aggregate_frames": {"agg": "k"},
        "decision_column": "timestamp", "window_seconds": 1.0,
        "ties_available": True, "label_column": "target",
        "split": {"train": [0, 1, 2, 3], "test": [4, 5]},
        "column_modes": {"v": "at_timestamp"},
        "bar_duration_seconds": 1.0,
        "note": "every key set, so the trace sees every one that is fetched",
    }), encoding="utf-8")

    sys.path.insert(0, str(tmp_path))
    a = install(mf.LoadedConfig, "config")
    b = install(AvailabilityModel, "model")
    try:
        for cmd in ("run", "check"):
            try:
                cli.main([cmd, "--pipeline", "p:build",
                          "--frame", "snap=%s" % (tmp_path / "snap.csv"),
                          "--frame", "agg=%s" % (tmp_path / "agg.csv"),
                          "--model", str(tmp_path / "m.json")])
            except SystemExit:
                pass
    finally:
        mf.LoadedConfig.__getattribute__ = a
        AvailabilityModel.__getattribute__ = b
        sys.path.remove(str(tmp_path))
    return read


def accepted_keys() -> set[str]:
    keys = set(mf._V1_KEYS)
    for v in mf._KEYS_BY_VERSION.values():
        keys |= set(v)
    return keys


def test_every_accepted_key_is_watchable():
    """A key with no attribute mapping cannot be measured, so it cannot be
    classified, so it must not pass silently."""
    missing = accepted_keys() - set(KEY_TO_ATTR) - set(DECLARED_REFUSED)
    assert not missing, (
        "these keys are accepted and this file does not know where their value "
        "rests, so it cannot measure whether anything reads them: %s"
        % sorted(missing))


def test_THE_COMPLEMENT_is_empty_of_unexplained_keys(tmp_path):
    """The whole population in one assertion."""
    read = _measure_read_keys(tmp_path)
    unread = accepted_keys() - read
    unexplained = unread - set(DECLARED_UNCONSUMED) - set(DECLARED_REFUSED)
    assert not unexplained, (
        "these keys are accepted by the loader, documented to users, and NOTHING "
        "READS THEM when the tool runs. Each is a user declaring something and "
        "being silently ignored -- P0's defect, which is what Phase 2 opened to "
        "fix. Wire it, or add it to DECLARED_UNCONSUMED with a reason and say so "
        "in `leakaudit schema`: %s" % sorted(unexplained))


def test_no_key_is_declared_unconsumed_AND_read(tmp_path):
    """The other direction. A stale 'unconsumed' entry is a false statement
    about the tool, and it would quietly excuse a real regression later."""
    read = _measure_read_keys(tmp_path)
    wrong = read & set(DECLARED_UNCONSUMED)
    assert not wrong, (
        "these are declared unconsumed and ARE read at run time, so the "
        "declaration is false and `leakaudit schema` is telling users something "
        "untrue: %s" % sorted(wrong))


def test_the_declared_unconsumed_set_names_only_ACCEPTED_keys():
    stray = set(DECLARED_UNCONSUMED) - accepted_keys()
    assert not stray, (
        "declared unconsumed but not accepted by the loader -- a leftover from a "
        "key that was removed: %s" % sorted(stray))


@pytest.mark.parametrize("key", sorted(DECLARED_UNCONSUMED))
def test_every_declared_unconsumed_key_carries_a_REASON(key):
    reason = DECLARED_UNCONSUMED[key]
    assert len(reason) > 60, (
        "%r is declared unconsumed with no real reason. 'Unconsumed' without a "
        "reason is the same silence as being unwired: %r" % (key, reason))


def test_the_three_that_were_FOUND_are_now_read(tmp_path):
    """The regression guard for R216's fixes and R217's measurement.

    `column_modes` and `ties_available` were in the complement at a023011 and
    are out of it now. If either returns, a user declaring it is silently
    ignored again.
    """
    read = _measure_read_keys(tmp_path)
    for k in ("column_modes", "ties_available"):
        assert k in read, (
            "%r is accepted and no longer read. It was fixed at R216 and has "
            "regressed; a user declaring it is being silently ignored." % k)

def test_every_REFUSED_key_is_actually_refused(tmp_path):
    """A key declared refused that quietly loads is the worst of the three
    states: the classification says the user is protected and they are not."""
    import json as _json

    from leakaudit.model_file import ModelFileError, load_model

    for key, reason in DECLARED_REFUSED.items():
        assert len(reason) > 60, "%r is declared refused with no reason" % key
        p = tmp_path / ("%s.json" % key)
        p.write_text(_json.dumps({
            "version": 3, "aggregate_frames": {"a": "k"}, key: "anything"}),
            encoding="utf-8")
        with pytest.raises(ModelFileError) as e:
            load_model(str(p))
        assert key in str(e.value), (
            "%r is declared refused and its refusal does not name it: %s"
            % (key, e.value))


def test_a_refused_key_is_NOT_also_declared_unconsumed():
    """The three states are exclusive. A key in two of them is a classification
    that has not been made."""
    both = set(DECLARED_REFUSED) & set(DECLARED_UNCONSUMED)
    assert not both, sorted(both)
