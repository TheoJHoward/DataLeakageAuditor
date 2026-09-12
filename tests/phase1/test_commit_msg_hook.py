"""The commit-msg hook's rule, tested without a repository. R268 §1.

The live positive -- `git commit -m "x"` refused -- is shown in the round's
report against the real repository. These pin the rule itself, each refusal with
the acceptance beside it, so a hook that refused everything would be
distinguishable from one that discriminates.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import commit_msg_hook as h                                   # noqa: E402
from safe_edit import COMMIT_TRAILER                          # noqa: E402

BODY = "A subject line\n\nA paragraph of body text.\n"


def test_a_message_WITHOUT_the_trailer_is_REFUSED():
    """What `git commit -m "x"` produces."""
    ok, reason = h.check("x\n")
    assert not ok
    assert "safe_edit.commit" in reason, "the refusal names the route out"


def test_the_NEGATIVE_a_message_WITH_the_trailer_is_ACCEPTED():
    ok, _ = h.check(BODY + "\n" + COMMIT_TRAILER + "\n")
    assert ok


def test_the_trailer_is_accepted_among_OTHER_trailers():
    """Co-Authored-By and the route trailer share the final block."""
    msg = (BODY + "\nCo-Authored-By: Claude Opus 5 <noreply@anthropic.com>\n"
           + COMMIT_TRAILER + "\n")
    assert h.check(msg)[0]


def test_the_trailer_QUOTED_IN_THE_BODY_does_not_pass():
    """A message ABOUT the hook, quoting the trailer on its own line, is not a
    message that came through the route. Only the final block counts."""
    msg = ("Subject\n\nThe hook keys on this line:\n" + COMMIT_TRAILER
           + "\n\nMore body after it.\n")
    assert not h.check(msg)[0]


def test_comment_lines_are_ignored():
    msg = BODY + "\n" + COMMIT_TRAILER + "\n# Please enter the commit message\n"
    assert h.check(msg)[0]


def test_an_UNREADABLE_message_is_REFUSED_not_passed(tmp_path):
    """Fail closed. A hook that cannot see is not a hook that passes."""
    assert h.main([str(tmp_path / "does-not-exist")]) == 1


def test_main_returns_zero_only_for_an_accepted_message(tmp_path):
    good = tmp_path / "good.txt"
    bad = tmp_path / "bad.txt"
    good.write_text(BODY + "\n" + COMMIT_TRAILER + "\n", encoding="utf-8")
    bad.write_text("x\n", encoding="utf-8")
    assert h.main([str(good)]) == 0
    assert h.main([str(bad)]) == 1


def test_the_trailer_has_ONE_definition():
    """The hook imports the constant; it does not restate it."""
    src = (ROOT / "tools" / "commit_msg_hook.py").read_text(encoding="utf-8")
    assert "from safe_edit import COMMIT_TRAILER" in src
    assert COMMIT_TRAILER not in src, (
        "the trailer string is written into the hook as well as safe_edit, so "
        "the two can drift and the hook would refuse the route's own commits")


def test_safe_edit_commit_ASKS_git_for_the_trailer():
    src = (ROOT / "tools" / "safe_edit.py").read_text(encoding="utf-8")
    assert '"--trailer", COMMIT_TRAILER' in src


def test_the_shell_hook_FAILS_CLOSED_and_finds_the_tool_by_its_own_path():
    sh = (ROOT / ".githooks" / "commit-msg").read_text(encoding="utf-8")
    assert sh.startswith("#!/bin/sh\n"), "a CRLF or missing shebang breaks sh"
    assert "\r" not in sh
    assert 'dirname "$0"' in sh, "located from the hook's own path"
    assert "exec " in sh, "exec, so a failure to launch is a non-zero exit"
    assert "`" not in sh, "no backticks in the file that closes the backtick rule"
