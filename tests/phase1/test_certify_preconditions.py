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
    # The hook precondition is its own test below; here it is held satisfied so
    # this stays the work root's negative control and not a test of the clone.
    monkeypatch.setattr(cp, "check_commit_hook", lambda: (True, "held"))
    assert cp.main([]) == 0


# ---------------------------------------------------------------------------
# the commit-msg hook precondition. R268 §1(b).
# ---------------------------------------------------------------------------
def _hook_git(config_rc, config_out, ls_out):
    import commit_msg_hook as h

    def fake(root, *args):
        if args[0] == "config":
            return config_rc, config_out
        return 0, ls_out
    return h, fake


def test_an_UNSET_hooksPath_REFUSES_certification(monkeypatch, tmp_path):
    h, fake = _hook_git(1, "", "")
    monkeypatch.setattr(h, "_git_read", fake)
    monkeypatch.setenv(cp.WORK_ROOT_ENV, str(tmp_path))
    ok, msg = cp.check_commit_hook()
    assert not ok and "not set in this clone" in msg
    assert cp.main([]) == 1, "a clone without the hook must not certify"


def test_a_hooksPath_pointing_ELSEWHERE_is_REFUSED(monkeypatch):
    h, fake = _hook_git(0, "some/other/dir", "100755 x 0\t.githooks/commit-msg")
    monkeypatch.setattr(h, "_git_read", fake)
    ok, msg = cp.check_commit_hook()
    assert not ok and "not the tracked" in msg


def test_a_hook_tracked_NON_EXECUTABLE_is_REFUSED(monkeypatch):
    h, fake = _hook_git(0, ".githooks", "100644 x 0\t.githooks/commit-msg")
    monkeypatch.setattr(h, "_git_read", fake)
    ok, msg = cp.check_commit_hook()
    assert not ok and "100644" in msg


def test_the_NEGATIVE_a_live_hook_is_ACCEPTED(monkeypatch):
    """Without this, a precondition refusing everything looks identical."""
    h, fake = _hook_git(0, ".githooks", "100755 x 0\t.githooks/commit-msg")
    monkeypatch.setattr(h, "_git_read", fake)
    ok, msg = cp.check_commit_hook()
    assert ok, msg


def test_the_hook_helper_may_run_ONLY_read_only_git():
    """The no-subprocess pin above is textual. The hook's read lives in another
    module, so this pins what that module may run: two read-only subcommands,
    through one call site, and nothing that could execute a step."""
    import commit_msg_hook as h
    assert h.READ_ONLY_GIT == ("config", "ls-files")
    for forbidden in (("commit", "-m", "x"), ("push",), ("add", ".")):
        try:
            h._git_read(ROOT, *forbidden)
        except ValueError:
            continue
        raise AssertionError("_git_read ran %r" % (forbidden,))
    src = (ROOT / "tools" / "commit_msg_hook.py").read_text(encoding="utf-8")
    assert src.count("subprocess.run(") == 1, "one call site, behind the allow-list"


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


# ---------------------------------------------------------------------------
# the step set and the documented block are ONE sequence. R253 §1.
# ---------------------------------------------------------------------------
ROUND_STATE = ROOT / "evidence/session/ROUND_STATE.md"


def _documented_commands():
    """The commands in ROUND_STATE.md's certification block."""
    text = ROUND_STATE.read_text(encoding="utf-8")
    marker = "py -3.12 tools/certify_preconditions.py"
    start = text.index(marker)
    end = text.index("```", start)
    return [ln.strip() for ln in text[start:end].splitlines() if ln.strip()]


def test_EVERY_STEP_SET_TOOL_APPEARS_IN_THE_DOCUMENTED_BLOCK():
    """**TWO PLACES HELD THE SEQUENCE AND THEY DIVERGED.** R253 §1: the drift
    guard was added to `ROUND_STATE.md`'s block and NOT to `STEPS`, so the
    enumerated step set said certification had five always-steps while the
    block a runner copies had six. The two-lists hazard, in the pair of lists
    that define what certification IS.

    The existing check only looked for four named tools, so it could not see
    the divergence. This compares the sets.
    """
    documented = " ".join(_documented_commands())
    for cmd, when, _why in cp.STEPS:
        if when != "always":
            continue
        tool = [w for w in cmd.split() if w.endswith(".py") or w == "tests"]
        assert tool, cmd
        assert tool[0].split("/")[-1] in documented, (
            "%s is an ALWAYS step and does not appear in ROUND_STATE.md's "
            "certification block, so a runner copying the block would skip it"
            % tool[0])


def test_the_DRIFT_GUARD_is_an_ALWAYS_step():
    """Its unit tests are all synthetic (`tmp_path`), so the enumerated step is
    what exercises it against the real layout. A guard verified only against
    constructed layouts and hand-run against the real one is one skipped
    hand-run from unverified."""
    drift = [(c, w) for c, w, _ in cp.STEPS if "scratch_drift" in c]
    assert drift, "scratch_drift is not in the certification step set"
    assert drift[0][1] == "always", drift
    assert cp.WORK_ROOT_ENV in drift[0][0], (
        "the drift step does not carry the work-root variable, without which "
        "it cannot resolve the subdirectory it checks")
