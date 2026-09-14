"""The commit route refuses a tree no suite measured. R272 §2(g).

D-V30A-117 shipped a commit whose tree no full suite had run on. The suite record
now carries a fingerprint of the WORKING tree, and `safe_edit.commit` refuses when
none matches -- and, for a change touching the probe path, when no guard run
recorded the path set's current content.

Every case runs in a throwaway git repository with files STAGED and no commit
made: the gate is what is under test, and it refuses before git is asked to
commit anything.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import probe_path_guard as ppg                                   # noqa: E402
import safe_edit as se                                           # noqa: E402
import tree_fingerprint as tf                                    # noqa: E402

PROBE_FILE = "src/leakaudit/reach.py"


def _git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "r"
    r.mkdir()
    _git(r, "init", "-q")
    (r / "a.txt").write_text("one\n", encoding="utf-8")
    (r / "tools").mkdir()
    return r


def _suite_record(root, digest, full=True):
    (root / "tools" / "suite_tree_record.json").write_text(json.dumps({
        "last": {"tree_fingerprint": digest, "full_suite": full,
                 "args": ["tests"] if full else ["tests/phase1/x.py"]}}),
        encoding="utf-8")


def _message(tmp_path):
    m = tmp_path / "m.txt"
    m.write_text("A subject\n\nA body.\n", encoding="utf-8")
    return m


# --------------------------------------------------------------------------
# the suite half
# --------------------------------------------------------------------------

def test_KNOWN_POSITIVE_a_commit_with_NO_MATCHING_SUITE_RUN_is_REFUSED(repo, tmp_path):
    _git(repo, "add", "a.txt")
    _suite_record(repo, "0" * 64)
    with pytest.raises(se.EditRuleError) as e:
        se.commit(_message(tmp_path), repo=repo)
    msg = str(e.value)
    assert "COMMIT REFUSED" in msg and "NO SUITE RUN MATCHES" in msg, msg


def test_a_commit_with_NO_SUITE_RECORD_at_all_is_REFUSED(repo):
    _git(repo, "add", "a.txt")
    problems = se.commit_gate(repo)
    assert problems and "NO SUITE RECORD" in problems[0], problems


def test_the_NEGATIVE_a_matching_whole_suite_record_PASSES(repo):
    _git(repo, "add", "a.txt")
    _suite_record(repo, tf.fingerprint(repo)["digest"])
    assert se.commit_gate(repo) == []


def test_an_EDIT_AFTER_THE_SUITE_is_REFUSED(repo):
    _git(repo, "add", "a.txt")
    _suite_record(repo, tf.fingerprint(repo)["digest"])
    (repo / "a.txt").write_text("two\n", encoding="utf-8")
    problems = se.commit_gate(repo)
    assert problems and "NO SUITE RUN MATCHES" in problems[0], problems


def test_an_UNTRACKED_file_added_after_the_suite_is_REFUSED(repo):
    _git(repo, "add", "a.txt")
    _suite_record(repo, tf.fingerprint(repo)["digest"])
    (repo / "b.txt").write_text("new\n", encoding="utf-8")
    assert se.commit_gate(repo)


def test_git_ADD_after_the_suite_does_NOT_change_the_tree(repo):
    """Content, not porcelain status: staging what the suite read is the same tree."""
    _suite_record(repo, tf.fingerprint(repo)["digest"])
    _git(repo, "add", "a.txt")
    assert se.commit_gate(repo) == []


def test_a_SUBSET_run_matching_the_tree_is_REFUSED(repo):
    _git(repo, "add", "a.txt")
    _suite_record(repo, tf.fingerprint(repo)["digest"], full=False)
    problems = se.commit_gate(repo)
    assert problems and "not the whole suite" in problems[0], problems


def test_the_RUN_RECORDS_are_not_part_of_the_tree(repo):
    before = tf.fingerprint(repo)["digest"]
    _suite_record(repo, "x")
    (repo / "tools" / "wholeframe_guard_times.json").write_text("{}", encoding="utf-8")
    assert tf.fingerprint(repo)["digest"] == before


# --------------------------------------------------------------------------
# the guard half
# --------------------------------------------------------------------------

def _stage_probe_file(repo):
    p = repo / PROBE_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# probe path\n", encoding="utf-8")
    _git(repo, "add", PROBE_FILE)
    assert PROBE_FILE in ppg.path_set()


def test_KNOWN_POSITIVE_a_PROBE_PATH_commit_with_NO_MATCHING_GUARD_RUN_is_REFUSED(
        repo, tmp_path):
    _stage_probe_file(repo)
    _suite_record(repo, tf.fingerprint(repo)["digest"])
    with pytest.raises(se.EditRuleError) as e:
        se.commit(_message(tmp_path), repo=repo)
    msg = str(e.value)
    assert "PROBE-PATH COMMIT WITHOUT A MATCHING GUARD RUN" in msg, msg
    assert PROBE_FILE in msg


def test_the_NEGATIVE_a_guard_run_on_this_content_PASSES(repo):
    _stage_probe_file(repo)
    _suite_record(repo, tf.fingerprint(repo)["digest"])
    (repo / "tools" / "wholeframe_guard_times.json").write_text(json.dumps({
        "runs": [{"path_set_fingerprint":
                  tf.path_set_fingerprint(ppg.path_set(), repo)}]}),
        encoding="utf-8")
    assert se.commit_gate(repo) == []


def test_a_guard_run_on_OTHER_content_does_not_count(repo):
    _stage_probe_file(repo)
    stale = tf.path_set_fingerprint(ppg.path_set(), repo)
    (repo / PROBE_FILE).write_text("# edited after the guard\n", encoding="utf-8")
    _git(repo, "add", PROBE_FILE)
    _suite_record(repo, tf.fingerprint(repo)["digest"])
    (repo / "tools" / "wholeframe_guard_times.json").write_text(json.dumps({
        "runs": [{"path_set_fingerprint": stale}]}), encoding="utf-8")
    problems = se.commit_gate(repo)
    assert problems and "WITHOUT A MATCHING GUARD RUN" in problems[0], problems


def test_a_change_OFF_the_probe_path_needs_no_guard(repo):
    _git(repo, "add", "a.txt")
    _suite_record(repo, tf.fingerprint(repo)["digest"])
    assert se.commit_gate(repo) == []
