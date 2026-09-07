"""Certification cannot be run with an unmet precondition. R248 §1.

**THE SKIP THIS CLOSES.** `round_reconciliation` reads its population from
`LEAKAUDIT_WORK_ROOT`. Run without it, the check returns PASS while printing
*"COVERAGE IS ZERO … This is not a pass"* — and every gate result across a whole
session ran that way, so a working instrument was zeroed by the command that ran
it. The instrument is not can't-fail: given its population it fails.

*"Certified"* is an absence claim over the certification STEPS — no required step
was skipped, no precondition unmet — and it had never had its population stated.

Content-in throughout: the environment is monkeypatched, nothing on disk is
touched, and no test writes a file it is testing (R247 §3).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import certify_preconditions as cp                                 # noqa: E402


# ---------------------------------------------------------------------------
# the step set is stated, and states what it is
# ---------------------------------------------------------------------------
def test_the_step_set_is_ENUMERATED_not_remembered():
    assert len(cp.STEPS) >= 5, (
        "the certification step set has %d entries, which is fewer than the "
        "commands certification actually requires" % len(cp.STEPS))
    for cmd, when, why in cp.STEPS:
        assert cmd.strip() and why.strip(), cmd
        assert when in ("always", "when a probe-path file moved"), when


def test_every_certification_INSTRUMENT_is_named_in_the_step_set():
    """The named instruments exist and are all present. A step set that omits a
    tool is the absence claim failing in the file written to state it."""
    joined = " ".join(c for c, _, _ in cp.STEPS)
    for tool in ("clean_tree.py", "check_registration.py", "manifest_verify.py",
                 "wholeframe_guard.py"):
        assert tool in joined, "%s is not in the step set" % tool
        assert (ROOT / "tools" / tool).is_file(), "%s does not exist" % tool
    assert "pytest tests" in joined


def test_the_step_set_carries_the_WORK_ROOT_variable():
    """The variable is the thing that was omitted, so its presence in the
    recorded command is the point of recording the command."""
    gate = [c for c, _, _ in cp.STEPS if "check_registration.py" in c][0]
    assert cp.WORK_ROOT_ENV in gate


def test_the_step_set_uses_py_3_12_not_bare_python():
    """R227: `python` is a NAME, not an invocation."""
    for cmd, _, _ in cp.STEPS:
        assert "py -3.12" in cmd, cmd
        assert not cmd.split("=")[-1].strip().startswith("python "), cmd


# ---------------------------------------------------------------------------
# the precondition, in every state
# ---------------------------------------------------------------------------
def test_an_UNSET_work_root_is_REFUSED(monkeypatch):
    monkeypatch.delenv(cp.WORK_ROOT_ENV, raising=False)
    ok, msg = cp.check_work_root()
    assert not ok, (
        "an unset work root passed the precondition, so the exact skip that "
        "zeroed a check for a session is still possible by hand")
    assert "COVERAGE IS ZERO" in msg, (
        "the refusal does not say what the omission DOES, so a reader meets a "
        "rule rather than a reason")


def test_an_EMPTY_work_root_is_REFUSED(monkeypatch):
    monkeypatch.setenv(cp.WORK_ROOT_ENV, "")
    assert not cp.check_work_root()[0]


def test_a_work_root_that_DOES_NOT_EXIST_is_REFUSED(monkeypatch, tmp_path):
    monkeypatch.setenv(cp.WORK_ROOT_ENV, str(tmp_path / "nope"))
    ok, msg = cp.check_work_root()
    assert not ok and "does not exist" in msg, (
        "a path that is not there is a configuration error, not an empty round")


def test_a_work_root_that_is_a_FILE_is_REFUSED(monkeypatch, tmp_path):
    f = tmp_path / "a_file"
    f.write_text("x", encoding="utf-8")
    monkeypatch.setenv(cp.WORK_ROOT_ENV, str(f))
    assert not cp.check_work_root()[0]


def test_a_REAL_directory_is_ACCEPTED(monkeypatch, tmp_path):
    """The negative control. A precondition that refused everything would pass
    every case above and block every round."""
    monkeypatch.setenv(cp.WORK_ROOT_ENV, str(tmp_path))
    ok, msg = cp.check_work_root()
    assert ok and str(tmp_path) in msg


# ---------------------------------------------------------------------------
# the exit status is what a runner reads
# ---------------------------------------------------------------------------
def test_main_REFUSES_with_a_nonzero_exit(monkeypatch):
    monkeypatch.delenv(cp.WORK_ROOT_ENV, raising=False)
    assert cp.main([]) == 1, (
        "the preconditions printed a refusal and exited zero, so a runner "
        "chaining commands would carry on into a partial certification")


def test_main_PERMITS_with_a_zero_exit(monkeypatch, tmp_path):
    monkeypatch.setenv(cp.WORK_ROOT_ENV, str(tmp_path))
    assert cp.main([]) == 0


def test_it_does_NOT_run_the_steps():
    """R248 §1(c) is flagged, not built. This enumerates and gates; it does not
    execute, and a version that quietly ran the suite would be the single
    entrypoint arriving without the decision that authorises it."""
    src = (ROOT / "tools" / "certify_preconditions.py").read_text(
        encoding="utf-8")
    for runner in ("subprocess.run", "subprocess.call", "os.system",
                   "subprocess.Popen"):
        assert runner not in src, (
            "%s appears in the preconditions tool, which is supposed to gate "
            "rather than execute" % runner)
