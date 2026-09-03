"""Every config key the loader accepts either reaches a consumer or says it does
not. R216 §0 and §5.

THE HALT LIST RUN BACKWARDS. "A config key the loader reads and ignores" has been
on this project's halt list since R203. A halt list stops a failure going
FORWARD; it does nothing about instances already resident, and nobody had ever
run it backwards over the code. The first effective run returned three hits:

  ties_available    parsed, validated, documented -- comparator had NO CALLER.
                    Wired at R216 §2, with a discriminating positive.
  column_modes      parsed, validated with four distinct refusals, documented at
                    length -- and the CLI never passed it to the probe, so a user
                    declaring per-column modes silently got the whole-frame path.
                    The two paths give DIFFERENT answers (25 findings against 0,
                    measured at R205). Plumbed at R216 §0.
  timestamp_column  stored and read by nothing. NOT wired, because the probe uses
                    each frame's declared key as its clock; documented as inert
                    instead, which is the other honest option.

THIS FILE IS THE STANDING VERSION OF THAT SWEEP, so the next key added is caught
by a test rather than by someone chasing an unrelated question two months later.
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

from leakaudit.model_file import SCHEMA_DOC, load_model            # noqa: E402

# Every key the loader accepts, and what makes it non-inert. A key added to the
# loader and not to this map fails `test_every_accepted_key_is_accounted_for`.
KEYS = {
    "version":          "consumed: refuses a version this build does not know",
    "aggregate_frames": "consumed: the probe's perturbation domain",
    "decision_column":  "consumed: the probe's decision series",
    "window_seconds":   "consumed as `model.window`",
    "ties_available":   "consumed: the comparator branch, wired at R216",
    "label_column":     "consumed: the label checks",
    "split":            "consumed: the split checks",
    "column_modes":     "consumed: per-column availability, plumbed at R216",
    "timestamp_column": "INERT, and the schema says so",
    "note":             "INERT by design, and the schema says so",
}

DECLARED_INERT = {"timestamp_column", "note"}


def test_every_accepted_key_is_accounted_for():
    from leakaudit.model_file import _V1_KEYS, _KEYS_BY_VERSION

    accepted = set(_V1_KEYS)
    for v in _KEYS_BY_VERSION.values():
        accepted |= set(v)
    missing = accepted - set(KEYS)
    assert not missing, (
        "these keys are accepted by the loader and are not accounted for here. "
        "Each is either consumed -- name what by -- or inert, and an inert one "
        "must say so in `leakaudit schema`: %s" % sorted(missing))


@pytest.mark.parametrize("key", sorted(DECLARED_INERT))
def test_every_INERT_key_declares_its_inertness_to_the_USER(key):
    """A docstring that lies misleads a contributor, who has the code beside it.

    A `schema` surface that lies misleads a USER, who has nothing else to read --
    at the exact moment they are trying to configure the tool correctly. So an
    inert key says so where the user meets it, not only in a comment.
    """
    # Anchor on the REFERENCE ENTRY, not the worked example at the top -- the
    # example mentions every key and says nothing about any of them, so matching
    # the first occurrence tests the wrong text. The entry is the line where the
    # key is followed by two or more spaces and its description.
    import re

    m = re.search(r"^\s*%s\s{2,}(.+?)(?=^\s{2}\w+\s{2,}|\Z)" % re.escape(key),
                  SCHEMA_DOC, re.M | re.S)
    assert m, "%s has no reference entry in the schema doc" % key
    window = " ".join(m.group(1).split()).lower()
    assert any(w in window for w in ("inert", "ignored", "reaches nothing",
                                     "not yet consumed")), (
        "`%s` is documented without saying it reaches nothing:\n%s"
        % (key, window[:300]))


def test_ties_available_is_NOT_in_the_inert_set_any_more():
    """The regression guard for the wiring. If someone unwires it, this fails
    before the schema quietly becomes true again."""
    assert "ties_available" not in DECLARED_INERT
    from leakaudit.availability import AvailabilityModel
    m = AvailabilityModel(aggregate_frames={"a": "k"}, ties_available=False)
    assert m.available(pd.Timestamp("2026-01-01"),
                       pd.Timestamp("2026-01-01")) is np.False_ or \
        m.available(pd.Timestamp("2026-01-01"),
                    pd.Timestamp("2026-01-01")) is False


def test_column_modes_REACHES_the_probe_through_the_CLI(tmp_path, monkeypatch,
                                                        capsys):
    """The plumbing hit. Its observable is R205's fallback note, which the probe
    emits only when `column_modes` is non-empty -- so its absence was the
    symptom and its presence is the fix."""
    secs = pd.date_range("2026-05-05 10:00:00", periods=60, freq="1s")
    rng = np.random.default_rng(3)
    pd.DataFrame({"timestamp": [s + pd.Timedelta(milliseconds=300) for s in secs],
                  "q": rng.standard_normal(60)}).to_csv(tmp_path / "snap.csv",
                                                        index=False)
    pd.DataFrame({"k": secs, "v": rng.standard_normal(60),
                  "w": rng.standard_normal(60)}).to_csv(tmp_path / "agg.csv",
                                                         index=False)
    (tmp_path / "p.py").write_text(
        "import pandas as pd\n"
        "def build(f):\n"
        "    o = f['snap'].copy()\n"
        "    o['sec'] = pd.to_datetime(o['timestamp']).dt.floor('1s')\n"
        "    a = f['agg'].copy(); a['sec'] = pd.to_datetime(a['k'])\n"
        "    o['x'] = o['sec'].map(a.set_index('sec')['v']).to_numpy()\n"
        "    return o[['timestamp', 'x']]\n", encoding="utf-8")
    (tmp_path / "m.json").write_text(json.dumps({
        "version": 3, "aggregate_frames": {"agg": "k"},
        "decision_column": "timestamp",
        "column_modes": {"v": "at_timestamp"}}), encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    sys.path.insert(0, str(tmp_path))
    try:
        from leakaudit import cli
        cli.main(["run", "--pipeline", "p:build",
                  "--frame", "snap=%s" % (tmp_path / "snap.csv"),
                  "--frame", "agg=%s" % (tmp_path / "agg.csv"),
                  "--model", str(tmp_path / "m.json")])
    finally:
        sys.path.remove(str(tmp_path))

    out = capsys.readouterr().out
    assert "took the FRAME rule" in out, (
        "the per-column fallback note is absent, so `column_modes` did not "
        "reach the probe. A user declaring modes is silently getting the "
        "whole-frame path:\n%s" % out[-900:])


def test_the_loader_still_refuses_a_non_boolean_tie(tmp_path):
    from leakaudit.model_file import ModelFileError

    p = tmp_path / "m.json"
    p.write_text(json.dumps({"version": 3, "aggregate_frames": {"a": "k"},
                             "ties_available": "yes"}), encoding="utf-8")
    with pytest.raises(ModelFileError, match="ties_available"):
        load_model(str(p))
