"""The round-reconciliation check resolves its population AT RUN TIME. R219 §1.

WHAT WAS WRONG. `_WORK_ROOT` was a hardcoded absolute path to one session's
scratchpad. That session ended on 26 August 2026 — 679 files, nothing written
since — while the session doing the work carried 12,002 files in a different
directory, one of 149 beside it. So D10's coverage of the current round's working
files was ZERO, and every finding the check could emit came from a directory
nobody was working in (D-V30A-48). It reported green over an empty population for
weeks, which is TB-20's shape: a defect that makes a thing do nothing is
invisible to tests of that thing.

THE PLAUSIBLE WRONG REPAIR is resolving at IMPORT time. This module is imported
by the registration suite in processes unrelated to any session, so an
import-time binding fixes whatever the environment looked like when the module
first loaded — the same defect wearing a different hat. A caller that sets the
variable and then runs the check in the same process would see it work, and it
would be wrong everywhere else. **That is why the discriminating case sets the
variable AFTER import and expects it to be honoured.**

AND UNSET IS NOT A PASS. The defect being replaced was silent zero coverage. A
loud zero is a different thing, and the difference is the whole repair.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import check_registration as cr                                   # noqa: E402


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    monkeypatch.delenv(cr._WORK_ROOT_ENV, raising=False)


# ---------------------------------------------------------------------------
# DIRECTION 1 -- a file that exists only in the live directory is FOUND.
# ---------------------------------------------------------------------------

def test_a_file_only_in_the_work_root_is_reported(tmp_path, monkeypatch):
    (tmp_path / "unlanded.txt").write_text("not in the repo", encoding="utf-8")
    monkeypatch.setenv(cr._WORK_ROOT_ENV, str(tmp_path))
    f = cr.check_round_reconciliation(ROOT)
    real = [x for x in f if not x.is_note]
    assert real, "a working file in neither the repo nor the ephemeral list was "\
                 "not reported; the check is scanning nothing again"
    assert any("unlanded" in x.message or "1 working file" in x.message
               for x in real), [x.message for x in real]


def test_a_file_that_IS_in_the_repo_is_reconciled(tmp_path, monkeypatch):
    """The other half of direction 1: it must not report everything."""
    twin = (ROOT / "README.md").read_bytes()
    (tmp_path / "copy_of_readme.md").write_bytes(twin)
    monkeypatch.setenv(cr._WORK_ROOT_ENV, str(tmp_path))
    real = [x for x in cr.check_round_reconciliation(ROOT) if not x.is_note]
    assert not real, (
        "a byte-identical copy of a committed file was reported as unlanded, so "
        "the check reports on everything and its findings mean nothing: %s"
        % [x.message for x in real])


def test_an_ephemeral_file_is_not_reported(tmp_path, monkeypatch):
    d = tmp_path / "__pycache__"
    d.mkdir()
    (d / "x.cpython-312.pyc").write_bytes(b"\x00compiled")
    monkeypatch.setenv(cr._WORK_ROOT_ENV, str(tmp_path))
    real = [x for x in cr.check_round_reconciliation(ROOT) if not x.is_note]
    assert not real, [x.message for x in real]


# ---------------------------------------------------------------------------
# DIRECTION 2 -- the import-time repair is ruled out.
# ---------------------------------------------------------------------------

def test_the_variable_is_read_AFTER_import_not_at_it(tmp_path, monkeypatch):
    """The discriminating case for the wrong repair.

    `check_registration` was imported at the top of this file, long before this
    line runs and with the variable unset. If resolution happened at import, the
    value set here would be ignored and the check would report zero coverage.
    """
    (tmp_path / "late.txt").write_text("set after import", encoding="utf-8")
    monkeypatch.setenv(cr._WORK_ROOT_ENV, str(tmp_path))
    f = cr.check_round_reconciliation(ROOT)
    assert not any("COVERAGE IS ZERO" in x.message for x in f), (
        "the work root was bound at import time, so a variable set afterwards "
        "is ignored -- which is the original defect in a new form")
    assert [x for x in f if not x.is_note], "nothing was scanned"


def test_two_different_roots_in_ONE_process_give_different_answers(tmp_path,
                                                                   monkeypatch):
    """A second resolution in the same process must not reuse the first."""
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    (a / "only_in_a.txt").write_text("a", encoding="utf-8")

    monkeypatch.setenv(cr._WORK_ROOT_ENV, str(a))
    ra = [x for x in cr.check_round_reconciliation(ROOT) if not x.is_note]
    monkeypatch.setenv(cr._WORK_ROOT_ENV, str(b))
    rb = [x for x in cr.check_round_reconciliation(ROOT) if not x.is_note]

    assert ra and not rb, (
        "the two roots gave the same answer, so the value is cached across "
        "calls: a=%s b=%s" % ([x.message for x in ra], [x.message for x in rb]))


# ---------------------------------------------------------------------------
# UNSET IS NOT A PASS, and a missing directory is not an empty one.
# ---------------------------------------------------------------------------

def test_unset_reports_ZERO_COVERAGE_and_names_the_variable():
    f = cr.check_round_reconciliation(ROOT)
    assert len(f) == 1 and f[0].is_note
    assert "COVERAGE IS ZERO" in f[0].message
    assert "not a pass" in f[0].message.lower()
    assert cr._WORK_ROOT_ENV in f[0].message, (
        "the note does not name the variable to set, so a reader learns that "
        "nothing was checked and not how to check it")


def test_a_root_that_does_not_exist_is_a_FINDING_not_a_note(tmp_path,
                                                            monkeypatch):
    monkeypatch.setenv(cr._WORK_ROOT_ENV, str(tmp_path / "gone"))
    f = cr.check_round_reconciliation(ROOT)
    assert f and not f[0].is_note, (
        "a work root that does not exist is a configuration error and was "
        "reported as a note, which reads as 'nothing to do'")


def test_an_EMPTY_root_is_clean_and_is_not_confused_with_a_missing_one(
        tmp_path, monkeypatch):
    monkeypatch.setenv(cr._WORK_ROOT_ENV, str(tmp_path))
    f = cr.check_round_reconciliation(ROOT)
    assert not [x for x in f if not x.is_note], (
        "an empty working directory is a clean round, not a finding")


def test_the_superseded_hardcoded_path_is_KEPT_as_a_record():
    """Deleted, it would look as though the check had always resolved properly."""
    assert cr._WORK_ROOT_SUPERSEDED.name == "scratchpad"
    assert "8b1d67a4" in str(cr._WORK_ROOT_SUPERSEDED)
