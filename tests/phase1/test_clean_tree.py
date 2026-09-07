"""Certification refuses a tree that is not the one shipping. R247 §1.

**THE RULE.** A verification is a claim about a specific tree state. Any edit
after it, in the same round, voids it. Half this session's defects are that one
shape — evidence measured at state A, artifact shipped at state B.

Every case below is a wrong case: content-in, mutated in memory, nothing written
to any real path. R247 §3 — a mutation test that writes the file it is testing
is an irreversible-act hazard dressed as a tradeoff.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import clean_tree as ct                                            # noqa: E402


def _entries_from(porcelain: str) -> list:
    """The shipped filter, applied to supplied porcelain text.

    CONTENT-IN. `ct.entries()` shells out to git; this exercises the same
    filtering rule against text, so the wrong cases need no repository in a
    particular state.
    """
    out = []
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip().strip('"')
        if any(path.startswith(p) for p in ct.IGNORED_PREFIXES):
            continue
        out.append(line.rstrip())
    return out


def test_the_filter_matches_the_shipped_one():
    """The helper above restates `ct.entries`'s rule, so it is pinned against
    the real thing rather than being a second implementation free to drift."""
    real = ct.entries()
    porcelain = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain"],
        capture_output=True, text=True, encoding="utf-8").stdout
    assert _entries_from(porcelain) == real


# ---------------------------------------------------------------------------
# the wrong cases
# ---------------------------------------------------------------------------
def test_a_MODIFIED_file_makes_the_tree_dirty():
    assert _entries_from(" M src/leakaudit/availability.py\n"), (
        "an uncommitted modification did not register, so certification would "
        "run against a tree that is not the one shipping")


def test_an_UNTRACKED_file_makes_the_tree_dirty():
    assert _entries_from("?? tools/a_new_instrument.py\n"), (
        "a new file nobody has committed did not register -- which is exactly "
        "the shape that let a suite count predate three files in its commit")


def test_a_STAGED_file_makes_the_tree_dirty():
    assert _entries_from("M  DEVIATIONS.md\n")


def test_dot_claude_is_IGNORED_and_that_is_a_rule_not_a_convenience():
    """`.claude/` is never committed and never read, so its presence is not
    uncommitted work -- it is not work."""
    assert _entries_from("?? .claude/\n") == []
    assert _entries_from("?? .claude/settings.json\n") == []


def test_a_CLEAN_tree_is_clean():
    """The negative control. A checker that called everything dirty would pass
    every case above and refuse every certification."""
    assert _entries_from("") == []
    assert _entries_from("?? .claude/\n\n") == []


def test_a_MIXTURE_reports_only_the_real_work():
    got = _entries_from("?? .claude/\n M DEVIATIONS.md\n?? tools/x.py\n")
    assert len(got) == 2 and all(".claude" not in g for g in got)


# ---------------------------------------------------------------------------
# the instrument reports rather than assumes
# ---------------------------------------------------------------------------
def test_an_UNREADABLE_tree_is_not_reported_clean(tmp_path):
    """A directory that is not a repository cannot answer, and the answer is
    'unknown', not 'clean'. Silence from a broken instrument reading as a pass
    is D-V30A-48's shape."""
    with pytest.raises(ct.TreeUnreadable):
        ct.entries(tmp_path)


def test_main_returns_nonzero_when_dirty_and_zero_when_clean(monkeypatch):
    monkeypatch.setattr(ct, "entries", lambda repo=None: [" M x.py"])
    assert ct.main([]) == 1
    monkeypatch.setattr(ct, "entries", lambda repo=None: [])
    assert ct.main([]) == 0


def test_main_returns_nonzero_when_the_tree_cannot_be_read(monkeypatch):
    def boom(repo=None):
        raise ct.TreeUnreadable("git is not available")
    monkeypatch.setattr(ct, "entries", boom)
    assert ct.main([]) == 1, (
        "an unreadable tree exited zero, so a broken git would certify every "
        "round silently")
