"""The availability model file, and its refusals. R202 §1.

EVERY REFUSAL HAS A NEGATIVE CONTROL. A rule that refused every file would also
never read a model wrong, and would be useless — that failure looks safer than
the one it replaces, which is why it is the one almost nobody tests for. So each
refusal below is paired with a file that differs in exactly the refused respect
and is accepted.

THE VERSION IS THE ONE THAT MATTERS. A model read under a schema the build does
not understand is a probe that looks like it ran and did not check what the user
wrote down.
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

from leakaudit.model_file import (                                # noqa: E402
    SCHEMA_DOC, SCHEMA_VERSION, SUPPORTED_VERSIONS, ModelFileError, load_model)

GOOD = {
    "version": SCHEMA_VERSION,
    "aggregate_frames": {"trades": "ts_event"},
    "decision_column": "timestamp",
    "window_seconds": 1.0,
    "ties_available": True,
    "note": "for whoever reads this next",
}


def _write(tmp_path: Path, obj, name="m.json") -> Path:
    p = tmp_path / name
    p.write_text(json.dumps(obj) if not isinstance(obj, str) else obj,
                 encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# The negative control, first
# ---------------------------------------------------------------------------

def test_a_well_formed_model_loads(tmp_path):
    m = load_model(_write(tmp_path, GOOD))
    assert m.aggregate_frames == {"trades": "ts_event"}
    assert m.decision_column == "timestamp"
    assert m.window == pd.Timedelta(seconds=1)
    assert m.ties_available is True


def test_only_the_required_keys_are_required(tmp_path):
    m = load_model(_write(tmp_path, {"version": SCHEMA_VERSION,
                                     "aggregate_frames": {"a": "k"}}))
    assert m.decision_column == "timestamp"
    assert m.window == pd.Timedelta(seconds=1)
    assert m.ties_available is True


# ---------------------------------------------------------------------------
# The version, refused rather than negotiated
# ---------------------------------------------------------------------------

def test_an_unknown_version_is_refused_naming_what_it_expected(tmp_path):
    bad = dict(GOOD, version=999)
    with pytest.raises(ModelFileError) as e:
        load_model(_write(tmp_path, bad))
    msg = str(e.value)
    assert "999" in msg
    assert "REFUSED, not read best-effort" in msg
    assert str(list(SUPPORTED_VERSIONS)) in msg


def test_a_missing_version_is_refused(tmp_path):
    bad = {k: v for k, v in GOOD.items() if k != "version"}
    with pytest.raises(ModelFileError, match="no `version` field"):
        load_model(_write(tmp_path, bad))


def test_the_supported_version_is_accepted(tmp_path):
    """The pair to both above."""
    assert load_model(_write(tmp_path, GOOD)) is not None


# ---------------------------------------------------------------------------
# Unknown keys, refused rather than ignored
# ---------------------------------------------------------------------------

def test_an_unknown_key_is_refused_not_ignored(tmp_path):
    """A typo in a key name is otherwise a setting written and not applied."""
    with pytest.raises(ModelFileError) as e:
        load_model(_write(tmp_path, dict(GOOD, decison_column="timestamp")))
    assert "decison_column" in str(e.value)
    assert "Refused rather than ignored" in str(e.value)


def test_every_known_key_is_accepted(tmp_path):
    assert load_model(_write(tmp_path, GOOD)) is not None


# ---------------------------------------------------------------------------
# The rest, each with its pair
# ---------------------------------------------------------------------------

def test_a_file_that_is_not_json_is_refused(tmp_path):
    with pytest.raises(ModelFileError, match="not valid JSON"):
        load_model(_write(tmp_path, "{not json"))


def test_a_missing_file_is_refused(tmp_path):
    with pytest.raises(ModelFileError, match="no such file"):
        load_model(tmp_path / "absent.json")


def test_a_non_object_top_level_is_refused(tmp_path):
    with pytest.raises(ModelFileError, match="top level is list"):
        load_model(_write(tmp_path, [1, 2, 3]))


def test_empty_aggregate_frames_is_refused(tmp_path):
    with pytest.raises(ModelFileError, match="non-empty"):
        load_model(_write(tmp_path, dict(GOOD, aggregate_frames={})))


def test_a_non_string_frame_mapping_is_refused(tmp_path):
    with pytest.raises(ModelFileError, match="not string -> string"):
        load_model(_write(tmp_path, dict(GOOD, aggregate_frames={"a": 7})))


@pytest.mark.parametrize("bad", [0, -1, "wide"])
def test_a_window_that_describes_no_span_is_refused(tmp_path, bad):
    with pytest.raises(ModelFileError):
        load_model(_write(tmp_path, dict(GOOD, window_seconds=bad)))


def test_a_positive_window_is_accepted_and_carried(tmp_path):
    m = load_model(_write(tmp_path, dict(GOOD, window_seconds=2.5)))
    assert m.window == pd.Timedelta(seconds=2.5)


def test_a_non_boolean_tie_rule_is_refused(tmp_path):
    with pytest.raises(ModelFileError, match="true or false"):
        load_model(_write(tmp_path, dict(GOOD, ties_available="yes")))


def test_the_tie_rule_is_carried_when_it_is_false(tmp_path):
    assert load_model(_write(tmp_path, dict(GOOD, ties_available=False))
                      ).ties_available is False


def test_an_empty_decision_column_is_refused(tmp_path):
    with pytest.raises(ModelFileError, match="column name was expected"):
        load_model(_write(tmp_path, dict(GOOD, decision_column="")))


# ---------------------------------------------------------------------------
# It is a tool config and says so
# ---------------------------------------------------------------------------

def test_the_schema_doc_says_it_is_not_the_registered_declaration():
    assert "NOT A REGISTERED DECLARATION" in SCHEMA_DOC
    assert "supersedes nothing" in SCHEMA_DOC
    assert "not a gate result" in SCHEMA_DOC


def test_the_schema_doc_explains_the_unnamed_frame_case():
    """The silence rule reaches the user-facing documentation, not only the code."""
    assert "`none`, not `observed_silence`" in SCHEMA_DOC
