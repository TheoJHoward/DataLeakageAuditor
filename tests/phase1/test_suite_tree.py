"""The suite's tree record, and the refusals it makes possible. R267 §1.1.

D-V30A-102's remaining half. The step set says the suite runs on the committed
tree; nothing made that true. These pin the three ways a recorded run can fail
to describe the shipped tree, each with a negative beside it so a refusal that
fires on everything is distinguishable from one that discriminates.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import suite_tree as st                                      # noqa: E402


def _rec(commit="abc1234", clean=True, args=None, dirty=None):
    return {"what": "test", "last": {
        "when": "2026-01-01 00:00", "commit": commit, "clean": clean,
        "dirty_paths": dirty or [], "args": args or ["tests"],
        "full_suite": st.is_full_suite(args or ["tests"]),
        "exitstatus": 0, "counts": {"passed": 1}}}


# -- the known positive R267 §1.1 names: suite, commit anything, certify -----

def test_THE_KNOWN_POSITIVE_a_commit_after_the_suite_REFUSES():
    """Run the suite, commit anything, certify -> refused."""
    problems = st.check(_rec(commit="aaaaaaa"), current="bbbbbbb")
    assert problems, "a moved HEAD must refuse"
    assert any("describes a tree that is not the one being certified" in p
               for p in problems)
    assert any("aaaaaaa" in p and "bbbbbbb" in p for p in problems), (
        "the refusal names BOTH hashes, or a reader cannot tell which way it "
        "is stale")


def test_the_NEGATIVE_beside_it_an_unmoved_HEAD_passes():
    """Without this, a check that refuses everything would look identical."""
    assert st.check(_rec(commit="aaaaaaa"), current="aaaaaaa") == []


def test_a_suite_that_ran_over_a_DIRTY_tree_REFUSES():
    problems = st.check(_rec(commit="a", clean=False, dirty=["src/x.py"]),
                        current="a")
    assert any("DIRTY" in p for p in problems)
    assert any("src/x.py" in p for p in problems), "it names what was dirty"


def test_a_SUBSET_run_REFUSES_even_when_the_hash_matches():
    """`pytest tests/phase1/test_slicing.py` is a real run and is not the suite."""
    sub = ["tests/phase1/test_slicing.py"]
    problems = st.check(_rec(commit="a", args=sub), current="a")
    assert any("not the whole suite" in p for p in problems)


def test_a_MISSING_record_REFUSES_rather_than_passing_over_nothing():
    problems = st.check({}, current="a")
    assert problems, "no record is not a pass"


def test_an_UNREADABLE_record_file_REFUSES(monkeypatch, tmp_path):
    monkeypatch.setattr(st, "RECORD", tmp_path / "nope.json")
    monkeypatch.setattr(st, "REPO", tmp_path)
    problems = st.check()
    assert any("no usable suite record" in p for p in problems)


# -- scope detection, both directions ---------------------------------------

@pytest.mark.parametrize("args,expected", [
    (["tests"], True),
    ([str(ROOT / "tests")], True),
    (["."], True),
    ([], False),
    (["tests/phase1"], False),
    (["tests/phase1/test_slicing.py"], False),
    (["tests", "tests/phase1/test_slicing.py"], False),
])
def test_full_suite_detection(args, expected):
    assert st.is_full_suite(args) is expected


# -- the record itself -------------------------------------------------------

def test_the_record_ROUND_TRIPS_through_the_checker(tmp_path, monkeypatch):
    monkeypatch.setattr(st, "RECORD", tmp_path / "rec.json")
    monkeypatch.setattr(st, "dirty_paths", lambda: [])
    monkeypatch.setattr(st, "head", lambda: "deadbee")
    doc = st.record(["tests"], 0, {"passed": 10})
    assert doc["last"]["commit"] == "deadbee"
    assert doc["last"]["clean"] is True
    on_disk = json.loads((tmp_path / "rec.json").read_text(encoding="utf-8"))
    assert st.check(on_disk, current="deadbee") == []
    assert st.check(on_disk, current="other12") != []


def test_the_record_file_is_NOT_dirt_to_clean_tree():
    """Or the suite makes every tree dirty and nothing certifies again."""
    import clean_tree
    assert "tools/suite_tree_record.json" in clean_tree.IGNORED_EXACT
    # EXACT, not a prefix -- a prefix would hide whatever grew beneath it.
    assert not any(p.startswith("tools/") for p in clean_tree.IGNORED_PREFIXES)


def test_the_records_own_dirt_is_not_counted_as_the_rounds():
    assert "tools/suite_tree_record.json" in st._NOT_DIRT
    assert ".claude/" in st._NOT_DIRT


# -- the step set carries it -------------------------------------------------

def test_the_CHECK_is_an_enumerated_ALWAYS_step():
    """A mechanism nobody is required to run is a mechanism nobody runs."""
    import certify_preconditions as cp
    always = [c for c, when, _ in cp.STEPS if when == "always"]
    assert any("suite_tree.py" in c for c in always), (
        "the suite-tree check must be an enumerated step, or it is optional")
    # and it sits AFTER the suite, since it reads what the suite writes
    cmds = [c for c, _, _ in cp.STEPS]
    assert cmds.index("py -3.12 -m pytest tests") < next(
        i for i, c in enumerate(cmds) if "suite_tree.py" in c)
