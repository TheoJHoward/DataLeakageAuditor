"""The drift guard's known positive. R252 §3(c).

**B IS SLOT-FREE AND DISCIPLINE-DEPENDENT, and this is the check that turns the
dependency into a finding rather than a silence.** With the work root a
dedicated scratch subdirectory, `tasks/` falls outside it and no frozen
`_EPHEMERAL` change is needed. The price is that round scratch written anywhere
else leaves the reconciliation's population without saying so — which is not a
worry, it is a record: 49 files sat one level above the declared root and were
invisible for many rounds.

So the guard gets what every check here gets: **a work file placed outside the
subdir has to make it red**, and a clean layout has to leave it green. A guard
that reddened on everything, or on nothing, would look identical in a summary.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import scratch_drift as sd                                         # noqa: E402


def _layout(tmp_path):
    """A session directory in the shape B prescribes."""
    root = tmp_path / "scratchpad"
    (root / "sub").mkdir(parents=True)
    (root / "a_note.md").write_text("round work", encoding="utf-8")
    (root / "sub" / "deep.py").write_text("x = 1", encoding="utf-8")
    (tmp_path / "tasks").mkdir()
    (tmp_path / "tasks" / "abc.output").write_text("log", encoding="utf-8")
    return root


# ---------------------------------------------------------------------------
# the known positive
# ---------------------------------------------------------------------------
def test_a_WORK_FILE_OUTSIDE_THE_SUBDIR_MAKES_IT_RED(tmp_path):
    """**THE POSITIVE THIS EXISTS FOR.** It is the 49-files failure in
    miniature: a disclosure body written one level up."""
    root = _layout(tmp_path)
    (tmp_path / "d99.md").write_text("a disclosure body", encoding="utf-8")
    stray = sd.drifted(root)
    assert stray == ["d99.md"], (
        "a round-work file outside the work root was not reported, so B's "
        "discipline dependency is still a silence: %s" % stray)


def test_a_WORK_DIRECTORY_outside_the_subdir_is_reported(tmp_path):
    root = _layout(tmp_path)
    (tmp_path / "cli_fixtures").mkdir()
    (tmp_path / "cli_fixtures" / "agg.csv").write_text("a,b", encoding="utf-8")
    assert sd.drifted(root) == ["cli_fixtures/agg.csv"]


# ---------------------------------------------------------------------------
# the negative controls
# ---------------------------------------------------------------------------
def test_a_CLEAN_layout_is_GREEN(tmp_path):
    """A guard that reddened on everything would pass the positive above."""
    root = _layout(tmp_path)
    assert sd.drifted(root) == [], (
        "a layout with all work under the subdir was reported as drift")


def test_HARNESS_DIRECTORIES_are_not_round_work(tmp_path):
    """`tasks/` is the harness's, and B's whole point is that it falls outside
    the root without needing a frozen exclusion."""
    root = _layout(tmp_path)
    for i in range(5):
        (tmp_path / "tasks" / ("t%d.output" % i)).write_text("x",
                                                            encoding="utf-8")
    assert sd.drifted(root) == []
    assert "tasks" in sd.HARNESS_DIRS


def test_files_DEEP_under_the_subdir_are_fine(tmp_path):
    root = _layout(tmp_path)
    deep = root / "a" / "b" / "c"
    deep.mkdir(parents=True)
    (deep / "x.py").write_text("y = 2", encoding="utf-8")
    assert sd.drifted(root) == []


# ---------------------------------------------------------------------------
# it refuses rather than reporting nothing
# ---------------------------------------------------------------------------
def test_an_UNSET_work_root_is_UNREADABLE_not_clean(monkeypatch):
    """Zero coverage is not a pass — the shape `round_reconciliation` was
    reporting for a whole session."""
    monkeypatch.delenv(sd.WORK_ROOT_ENV, raising=False)
    with pytest.raises(sd.DriftUnreadable) as e:
        sd.resolve_root()
    assert "reports nothing rather than reporting no drift" in str(e.value)


def test_a_work_root_that_is_not_a_directory_is_UNREADABLE(tmp_path):
    f = tmp_path / "a_file"
    f.write_text("x", encoding="utf-8")
    with pytest.raises(sd.DriftUnreadable):
        sd.resolve_root(str(f))


def test_main_exits_NONZERO_on_drift(tmp_path, monkeypatch):
    root = _layout(tmp_path)
    (tmp_path / "stray.txt").write_text("work", encoding="utf-8")
    monkeypatch.setenv(sd.WORK_ROOT_ENV, str(root))
    assert sd.main([]) == 1


def test_main_exits_ZERO_when_clean(tmp_path, monkeypatch):
    root = _layout(tmp_path)
    monkeypatch.setenv(sd.WORK_ROOT_ENV, str(root))
    assert sd.main([]) == 0
