"""The Track B classification is TOTAL, and a new lesson fails until it is placed.

R224 §4 item 3 asked for a classification made by hand, with its membership list.
A hand-made list is a claim about a file that drifts from it -- which is the
failure this project keeps recording -- so the claim is held here by measurement
instead: the entries are read from the file, the membership lines are read from
the file, and the two are required to agree exactly.

THE TOTALITY SHAPE, the same one `PROBE_PATH_SET.json`'s on-path/off-path lists
and the config-key complement use. Disjoint and jointly covering: every entry in
exactly one family, no family naming an entry that does not exist. A
classification with an unassigned entry has not classified anything, and the
twenty-second lesson will fail this file until somebody decides where it goes --
which is the point, because deciding where it goes is the work.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LESSONS = ROOT / "evidence/session/TRACKB_LESSONS.md"
MARKER = "THE CLASSIFICATION"


def _text() -> str:
    return LESSONS.read_text(encoding="utf-8")


def _entries(text: str) -> set[str]:
    return set(re.findall(r"^## (TB-\d\d)", text, re.M))


def _families(text: str) -> dict[str, set[str]]:
    """family heading -> the TB ids its Members line names."""
    section = text.split(MARKER)[-1]
    out: dict[str, set[str]] = {}
    current = None
    for line in section.splitlines():
        m = re.match(r"^## (F\d) — (.+)$", line)
        if m:
            current = "%s %s" % (m.group(1), m.group(2))
            continue
        if current and line.startswith(("**Members:", "**Member:")):
            out[current] = set(re.findall(r"TB-\d\d", line))
            current = None
    return out


def test_the_classification_section_exists_at_all():
    assert MARKER in _text(), (
        "the hand-made classification is gone from %s, so the membership list "
        "this file checks does not exist" % LESSONS.name)


def test_every_lesson_is_classified():
    text = _text()
    entries = _entries(text)
    assert entries, "no TB entries found; the heading form must have changed"
    classified = set().union(*_families(text).values())
    unassigned = entries - classified
    assert not unassigned, (
        "these lessons are in the file and in no family, so the classification "
        "is silent about them -- place each one or say why it has no family: %s"
        % sorted(unassigned))


def test_no_family_names_a_lesson_that_does_not_exist():
    text = _text()
    phantom = set().union(*_families(text).values()) - _entries(text)
    assert not phantom, (
        "these are named in a membership list and are not entries in the file, "
        "so the list is a claim about lessons that are not there: %s"
        % sorted(phantom))


def test_the_families_are_DISJOINT():
    """An entry in two families is a classification nobody has made."""
    fams = _families(_text())
    seen: dict[str, str] = {}
    doubled = []
    for name, members in fams.items():
        for tb in members:
            if tb in seen:
                doubled.append("%s is in both %r and %r" % (tb, seen[tb], name))
            seen[tb] = name
    assert not doubled, doubled


def test_every_family_names_members_and_the_section_states_the_TOTAL():
    """A membership list without its denominator is a figure without its frame.

    The denominator is asserted at the SECTION level rather than per family: the
    families write their counts in prose ("Five of twenty-one"), and a test that
    demanded digits in each line would be a checker dictating the writing rather
    than checking the claim -- the shape R218 ruled against when a docstring was
    reworded to satisfy a parser.
    """
    text = _text()
    total = len(_entries(text))
    section = text.split(MARKER)[-1]
    for name, members in _families(text).items():
        assert members, "%s names no members" % name
    assert re.search(r"\b%d\b" % total, section), (
        "the classification does not state, in digits, how many entries it is "
        "classifying, so no reader can tell whether it covers all of them. The "
        "file holds %d." % total)
