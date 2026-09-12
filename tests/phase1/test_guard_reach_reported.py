"""The guard carries the reach, prints it, and never compares it. R268 §4.

The ruling has two halves and each is a way to get it wrong. Reach DISABLED in
the guard would make the guard stop running what a user runs -- cheaper, and a
different instrument. Reach COMPARED as a ninth term would turn a finding about
the fixture's builder into a red guard, when a moved reach is a ruling and not a
regression. These tests read the guard's source, because the guard itself costs
fifteen minutes and needs the fixture; the properties pinned are structural.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import wholeframe_guard as wg                                    # noqa: E402

SRC = (ROOT / "tools" / "wholeframe_guard.py").read_text(encoding="utf-8")


def _comparison_block() -> str:
    start = SRC.index("COMPARISON, term by term")
    end = SRC.index("if moved:", start)
    return SRC[start:end]


def test_the_comparison_is_EXACTLY_the_frozen_four_per_side():
    """Four keys, two sides: eight terms. The block is found by its own text, so
    an empty match would fail the equality rather than pass it."""
    # `features` is compared as `sorted(b[...])`, so the baseline side may sit
    # inside a call. The first version of this pattern required `b[` directly
    # and found three keys, which is how a structural pin misreports the
    # structure it pins; the equality below is what caught it.
    keys = re.findall(r'\(\s*"([a-z_]+)"\s*,\s*(?:sorted\()?b\[',
                      _comparison_block())
    assert keys == ["verdict", "eligible", "records", "features"], keys


def test_REACH_IS_NOT_A_COMPARED_TERM():
    assert "reach" not in _comparison_block().lower(), (
        "the reach reached the comparison. A reach that moves is a finding about "
        "the fixture's builder and a ruling, not a red guard (R268 section 4)")


def test_the_reach_is_held_OUTSIDE_the_dict_the_comparison_reads():
    assert isinstance(wg.REACH_SEEN, dict)
    start = SRC.index("out[side] = {")
    end = SRC.index("}", start)
    assert "reach" not in SRC[start:end], (
        "the reach went into out[side], where any loop over the compared terms "
        "could pick it up")


def test_the_reach_is_PRINTED_before_the_comparison_so_a_halt_cannot_hide_it():
    assert "REACH, REPORTED AND NOT COMPARED" in SRC
    assert SRC.index("REACH, REPORTED AND NOT COMPARED") < SRC.index(
        "COMPARISON, term by term")


def test_the_reach_is_NOT_DISABLED_in_the_guard():
    """The guard runs what a user runs. `reach_samples=0` here would make it
    cheaper and a different instrument."""
    call = SRC[SRC.index("res = run_probe_a("):]
    call = call[:call.index(")") + 1]
    assert "reach_samples" not in call, call
