"""The column probe counts the cells it corrupts, per frame. R273 §1(b).

The counting half of the one corruption entry point, applied to the column
dependency probe: its selection is by column rather than time, so the alignment
half does not apply, but a frame no strategy changed a single cell of has had no
probe, and its silence is `none` -- said in the run's own output.

THE PAIR. HELD: one builder, one call. VARIED: the frame -- one with values to
corrupt, one with no column to corrupt at all.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.contract import audit                           # noqa: E402
from leakaudit.probe import probe_columns                      # noqa: E402


def _frames():
    return {"a": pd.DataFrame({"x": np.arange(20.0)}),
            "empty": pd.DataFrame(index=range(20))}


def _build(fr):
    return pd.DataFrame({"y": fr["a"]["x"].to_numpy() * 2.0})


def test_cells_are_COUNTED_per_frame_and_a_ZERO_frame_is_NONE():
    r = probe_columns(_frames(), _build)
    assert r.cells_by_frame["a"] > 0, r.cells_by_frame
    assert r.cells_by_frame["empty"] == 0, r.cells_by_frame
    assert any(n.startswith("NONE FOR FRAME 'empty'") for n in r.notes), r.notes
    assert not any(n.startswith("NONE FOR FRAME 'a'") for n in r.notes)
    assert r.notes[0].startswith("cells corrupted per input frame")


def test_the_count_REACHES_the_printed_result():
    """The line is in `explain()`, not only on the library object: `notes` is
    rendered unless it begins `NOT PROBED:`, which this one does not."""
    text = str(audit(_frames(), _build))
    assert "NONE FOR FRAME 'empty'" in text, text
    assert "cells corrupted per input frame" in text
