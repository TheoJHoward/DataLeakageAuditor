"""The residue check reports a LEVEL and finds an INCREMENT. R226 §3.

WHAT CHANGED AND WHY IT IS NOT A SILENCING. `round_reconciliation` used to make
the whole unreconciled set a finding. That set grows every round by construction
-- a scratch directory only gets bigger -- and it reached 548, which no reader
can act on. R216 §5: a check earns attention in proportion to the fraction of its
findings that need thought, and a monotonically growing unactionable number earns
none.

THE PLAUSIBLE WRONG REPAIR, ruled out here by test rather than by intention:

  * declaring the large classes ephemeral to shrink the number. Forbidden by
    R226 §3 in terms, and it would be a token justified by its yield -- the
    thing R220 §3 and R224 §4 both refused.
  * a baseline the check updates itself. Then the increment is empty always and
    the check reports green over a population it absorbed on the same run, which
    is D-V30A-48's defect wearing a newer hat.
  * a baseline that reads as permission. An entry means REPORTED AND READ. The
    file that holds claims about files is `_EPHEMERAL`, and it takes reasons.

THE LEVEL DOES NOT DISAPPEAR. It is printed on every run, as a note, so the
number is still in front of whoever reads the gate.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import check_registration as cr                                  # noqa: E402


@pytest.fixture
def work(tmp_path, monkeypatch):
    """A tiny repo and a tiny work root, so the check's population is known."""
    repo = tmp_path / "repo"
    (repo / "evidence" / "session").mkdir(parents=True)
    (repo / "kept.txt").write_text("in the repository\n", encoding="utf-8")
    (repo / "evidence" / "MANIFEST.sha256").write_text("", encoding="utf-8")

    wr = tmp_path / "wr"
    wr.mkdir()
    (wr / "old_a.txt").write_text("a\n", encoding="utf-8")
    (wr / "old_b.txt").write_text("b\n", encoding="utf-8")
    (wr / "matches_repo.txt").write_text("in the repository\n", encoding="utf-8")
    monkeypatch.setenv(cr._WORK_ROOT_ENV, str(wr))
    return repo, wr


def _msgs(repo):
    return [(f.is_note, f.message) for f in cr.check_round_reconciliation(repo)]


def _write_baseline(repo, paths):
    p = repo / cr._WORK_ROOT_BASELINE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# baseline\n" + "\n".join(sorted(paths)) + "\n",
                 encoding="utf-8")


def test_a_missing_baseline_FAILS_LOUDLY_rather_than_passing(work):
    """Zero coverage by default is not a pass -- the rule R220 §4 established
    for the work root itself, applied to the thing that now bounds it. Without a
    baseline the check cannot compute an increment, and the wrong behaviour is
    to treat "no increment computable" as "no increment"."""
    repo, _ = work
    out = _msgs(repo)
    assert any(not note and "NO BASELINE" in m for note, m in out), out
    assert any(not note and "work_root_baseline.py --write" in m
               for note, m in out), (
        "the refusal does not name the route out: %s" % out)


def test_the_LEVEL_is_reported_even_when_the_increment_is_empty(work):
    repo, wr = work
    _write_baseline(repo, ["old_a.txt", "old_b.txt"])
    out = _msgs(repo)
    level = [m for note, m in out if note and m.startswith("LEVEL:")]
    assert level, "the level vanished from the output: %s" % out
    assert "2 working file(s)" in level[0], level[0]
    assert not any(not note for note, _m in out), (
        "nothing appeared since the baseline and the check still reports a "
        "finding: %s" % out)


def test_a_NEW_file_is_the_finding(work):
    repo, wr = work
    _write_baseline(repo, ["old_a.txt", "old_b.txt"])
    (wr / "appeared_this_round.py").write_text("x = 1\n", encoding="utf-8")
    out = _msgs(repo)
    findings = [m for note, m in out if not note]
    assert len(findings) == 1, out
    assert "APPEARED SINCE THE BASELINE" in findings[0]
    assert "appeared_this_round.py" in findings[0]
    assert "1 working file(s)" in findings[0]
    assert "old_a.txt" not in findings[0], (
        "the finding names files that were already in the baseline, so it is "
        "the level again rather than the increment: %s" % findings[0])


def test_the_baseline_does_NOT_shrink_the_level(work):
    """A baseline entry is not an ephemeral declaration. The level counts it."""
    repo, wr = work
    _write_baseline(repo, ["old_a.txt", "old_b.txt"])
    level = [m for note, m in _msgs(repo) if note and m.startswith("LEVEL:")][0]
    assert "2 working file(s)" in level, (
        "the two baselined files left the level, so the baseline is acting as "
        "a permission list: %s" % level)


def test_a_file_that_matches_repository_content_is_never_in_either(work):
    """The pre-existing behaviour, asserted so the new plumbing did not move
    it: content that is in the repository is reconciled, not baselined."""
    repo, _wr = work
    _write_baseline(repo, [])
    out = _msgs(repo)
    text = " ".join(m for _n, m in out)
    assert "matches_repo.txt" not in text, text


def test_the_check_NEVER_writes_the_baseline_itself(work):
    """The whole design: a self-updating baseline reports green over a
    population it absorbed on the same run."""
    repo, _wr = work
    path = repo / cr._WORK_ROOT_BASELINE
    assert not path.exists()
    cr.check_round_reconciliation(repo)
    assert not path.exists(), (
        "the check created the baseline, so the first run after any new file "
        "appears will absorb it and report nothing")

    _write_baseline(repo, ["old_a.txt"])
    before = path.read_bytes()
    cr.check_round_reconciliation(repo)
    assert path.read_bytes() == before, "the check rewrote the baseline"


def test_the_baseline_file_says_what_an_entry_MEANS():
    """A path list with no statement of what membership asserts will be read as
    permission, because that is what path lists usually are."""
    p = ROOT / cr._WORK_ROOT_BASELINE
    if not p.exists():
        pytest.skip("no baseline in this tree yet")
        return
    head = p.read_text(encoding="utf-8")[:1200]
    assert "REPORTED" in head and "READ" in head, head[:300]
    assert "not a claim" in head or "makes none" in head, head[:300]
