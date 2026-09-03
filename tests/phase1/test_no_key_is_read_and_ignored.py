"""What survives of the hand-written key sweep. R219 §3.

PARTIALLY RETIRED, AND THE SUCCESSOR IS NAMED: `test_config_key_complement.py`.

This file began as a hand-written map of key -> "consumed by X". A hand-written
map is a claim about the code that drifts from it, so the map was replaced by a
MEASUREMENT — the complement runs the tool end to end with every key set and
records which key-carrying attributes are actually fetched. Two of the five tests
here were strict subsets of that and are retired:

    test_every_accepted_key_is_accounted_for
        -> superseded by `test_every_accepted_key_is_watchable`, which asks the
           same question of a measured set rather than of a hand-maintained one.

    test_ties_available_is_NOT_in_the_inert_set_any_more
        -> superseded by `test_the_three_that_were_FOUND_are_now_read`, which
           asserts the same regression guard from the measurement.

THE RETIREMENT IS RECORDED RATHER THAN SILENT. A deleted test with no record is
indistinguishable from coverage quietly dropping, and in six months nobody can
tell the two apart. The two names above are written here so the question "was
that ever checked?" has an answer.

THREE ASSERTIONS SURVIVE, because the complement does not make them:

  (1) THE SCHEMA SURFACE. The complement classifies keys in a Python dict. It
      does not check that `leakaudit schema` tells the USER a key does nothing.
      A docstring that lies misleads a contributor, who has the code beside it;
      a schema surface that lies misleads a user, who has nothing else to read,
      at the moment they are trying to configure the tool correctly.

  (2) OBSERVABLE EFFECT, not merely a fetch. The complement measures that
      `column_modes` is READ. This measures that reading it CHANGES THE OUTPUT --
      the per-column fallback note the probe emits only when modes are present.
      A value fetched and then dropped would pass the complement and fail here.

  (3) THE TYPE REFUSAL, which is about the loader's validation rather than about
      consumption, and is outside the complement's subject entirely.
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

from leakaudit.model_file import (                                # noqa: E402
    SCHEMA_DOC, ModelFileError, load_model)

# Keys that load and are deliberately read by nothing. `timestamp_column` was
# here until R218 and is not any more: it is now REFUSED rather than inert, so
# the complement's third state holds it and the schema names the refusal.
DECLARED_INERT = {"note"}


@pytest.mark.parametrize("key", sorted(DECLARED_INERT))
def test_every_INERT_key_declares_its_inertness_to_the_USER(key):
    """(1) The schema surface, which the complement does not read."""
    m = re.search(r"^\s*%s\s{2,}(.+?)(?=^\s{2}\w+\s{2,}|\Z)" % re.escape(key),
                  SCHEMA_DOC, re.M | re.S)
    assert m, "%s has no reference entry in the schema doc" % key
    window = " ".join(m.group(1).split()).lower()
    assert any(w in window for w in ("inert", "ignored", "reaches nothing",
                                     "not yet consumed")), (
        "`%s` is documented to users without saying it reaches nothing:\n%s"
        % (key, window[:300]))


def test_the_REFUSED_key_says_so_in_the_schema_too(tmp_path):
    """The same obligation for the third state, since a user reads one surface.

    A key that is refused and documented as though it works sends someone to
    write it and be rejected, which is the schema telling them something untrue
    at the moment they are acting on it.
    """
    m = re.search(r"^\s*timestamp_column\s{2,}(.+?)(?=^\s{2}\w+\s{2,}|\Z)",
                  SCHEMA_DOC, re.M | re.S)
    assert m, "timestamp_column has no reference entry"
    window = " ".join(m.group(1).split()).lower()
    assert "refused" in window, window[:300]
    assert "aggregate_frames" in window, (
        "the schema declines the key without naming what to use instead: %s"
        % window[:300])


def test_column_modes_REACHES_the_probe_through_the_CLI(tmp_path, monkeypatch,
                                                        capsys):
    """(2) Observable EFFECT, not merely a fetch.

    The per-column fallback note is emitted only when `column_modes` is
    non-empty, so its absence was the symptom of the plumbing defect and its
    presence is the fix. A value fetched and dropped would pass the complement's
    attribute trace and fail this.
    """
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
        "the per-column fallback note is absent, so `column_modes` reached the "
        "probe without changing anything, or did not reach it:\n%s" % out[-900:])


def test_the_loader_still_refuses_a_non_boolean_tie(tmp_path):
    """(3) Validation, which is outside the complement's subject."""
    p = tmp_path / "m.json"
    p.write_text(json.dumps({"version": 3, "aggregate_frames": {"a": "k"},
                             "ties_available": "yes"}), encoding="utf-8")
    with pytest.raises(ModelFileError, match="ties_available"):
        load_model(str(p))
