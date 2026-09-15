"""The decision clock's zone: converted under a declaration, refused without one. R273 §1(a).

An aware key aligned to naive decision stamps assumes which zone the naive stamps
are in, and a zone is a fact about the world. Until R273 the one alignment
assumed UTC. It now converts only where the model DECLARES `decision_timezone`,
and refuses otherwise, naming the key that would settle it -- because a clock
read hours off is itself a leak, and this tool does not guess one.

THE PAIR. HELD: the frame, its UTC-aware key, the naive decision stamps, the
selected second. VARIED: the declaration.
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

from leakaudit.availability import (AvailabilityModel, ProbeError,  # noqa: E402
                                    select_cells)
from leakaudit.model_file import (SCHEMA_VERSION, ModelFileError,  # noqa: E402
                                  load_model)

T0 = pd.Timestamp("2026-01-15 14:30:00")
SEC = pd.Timedelta(seconds=1)


def _aware_frames():
    k = pd.to_datetime([T0 + i * SEC for i in range(10)]).tz_localize("UTC")
    return {"agg": pd.DataFrame({"k": k, "v": np.arange(10.0)})}


def _naive(start):
    return pd.Series([start + i * SEC for i in range(10)])


def _model(**kw):
    return AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d", **kw)


# --------------------------------------------------------------------------
# the pair
# --------------------------------------------------------------------------

def test_WITHOUT_a_declaration_the_aware_key_is_REFUSED_and_the_key_is_named():
    with pytest.raises(ProbeError) as e:
        select_cells(_aware_frames(), _model(), _naive(T0), seconds={T0 + 5 * SEC})
    msg = str(e.value)
    assert "REFUSED" in msg and "decision_timezone" in msg, msg
    assert "frame 'agg'" in msg and "'k'" in msg, msg


def test_WITH_the_declaration_the_same_key_CONVERTS_exactly():
    sel = select_cells(_aware_frames(), _model(decision_timezone="UTC"),
                       _naive(T0), seconds={T0 + 5 * SEC})
    assert sel.rows_by_frame == {"agg": 1}


def test_a_NON_UTC_declaration_converts_into_THAT_zone_and_the_wrong_zone_misses():
    """Naive decision stamps in America/Chicago (UTC-6 in January): the trade at
    14:30:05 UTC decides at 08:30:05 there. Declared correctly, it is selected.
    Declared as UTC against the same stamps, it lands six hours off and nothing
    is selected -- the silent mismatch the declaration exists to prevent."""
    chicago = T0 - pd.Timedelta(hours=6)
    right = select_cells(_aware_frames(), _model(decision_timezone="America/Chicago"),
                         _naive(chicago), seconds={chicago + 5 * SEC})
    assert right.rows_by_frame == {"agg": 1}
    wrong = select_cells(_aware_frames(), _model(decision_timezone="UTC"),
                         _naive(chicago), seconds={chicago + 5 * SEC})
    assert wrong.rows_by_frame == {"agg": 0}


def test_a_NAIVE_key_against_AWARE_decisions_is_REFUSED_either_way():
    frames = {"agg": pd.DataFrame({"k": [T0 + i * SEC for i in range(10)],
                                   "v": np.arange(10.0)})}
    aware = pd.Series(pd.to_datetime([T0 + i * SEC for i in range(10)]).tz_localize("UTC"))
    for model in (_model(), _model(decision_timezone="UTC")):
        with pytest.raises(ProbeError) as e:
            select_cells(frames, model, aware,
                         seconds={pd.Timestamp(T0 + 5 * SEC).tz_localize("UTC")})
        assert "Localise the key" in str(e.value), str(e.value)
        # R274 §1(a): the refusal names what would lift it.
        assert "per-frame key zone" in str(e.value), str(e.value)


def test_BOTH_AWARE_convert_with_no_declaration():
    aware = pd.Series(pd.to_datetime([T0 + i * SEC for i in range(10)])
                      .tz_localize("UTC").tz_convert("America/Chicago"))
    second = pd.Timestamp(T0 + 5 * SEC).tz_localize("UTC").tz_convert("America/Chicago")
    sel = select_cells(_aware_frames(), _model(), aware, seconds={second})
    assert sel.rows_by_frame == {"agg": 1}


# --------------------------------------------------------------------------
# the file, version 5
# --------------------------------------------------------------------------

def _write(tmp_path, doc):
    p = tmp_path / "m.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def test_the_model_file_carries_the_zone_at_VERSION_5(tmp_path):
    assert SCHEMA_VERSION == 5
    cfg = load_model(_write(tmp_path, {
        "version": 5, "aggregate_frames": {"agg": "k"}, "decision_column": "d",
        "decision_timezone": "UTC"}))
    assert cfg.model.decision_timezone == "UTC"


def test_a_VERSION_4_file_naming_the_zone_is_refused_WITH_THE_VERSION_HINT(tmp_path):
    with pytest.raises(ModelFileError) as e:
        load_model(_write(tmp_path, {
            "version": 4, "aggregate_frames": {"agg": "k"}, "decision_column": "d",
            "decision_timezone": "UTC"}))
    assert "decision_timezone" in str(e.value) and "[5]" in str(e.value), str(e.value)


@pytest.mark.parametrize("zone", ["Mars/Olympus_Mons", "", 5])
def test_an_UNRESOLVABLE_zone_is_REFUSED_at_the_file(tmp_path, zone):
    with pytest.raises(ModelFileError) as e:
        load_model(_write(tmp_path, {
            "version": 5, "aggregate_frames": {"agg": "k"}, "decision_column": "d",
            "decision_timezone": zone}))
    assert "decision_timezone" in str(e.value)


def test_an_UNDECLARED_zone_loads_as_None(tmp_path):
    cfg = load_model(_write(tmp_path, {
        "version": 5, "aggregate_frames": {"agg": "k"}, "decision_column": "d"}))
    assert cfg.model.decision_timezone is None


# --------------------------------------------------------------------------
# the fixture's key, an as-built fact
# --------------------------------------------------------------------------

def test_the_FIXTURE_model_DECLARES_UTC():
    text = (ROOT / "tools" / "wholeframe_guard.py").read_text(encoding="utf-8")
    assert 'decision_timezone="UTC"' in text
    assert "AVAILABILITY_DECLARATION.md" in text, "the fact is cited, not assumed"
