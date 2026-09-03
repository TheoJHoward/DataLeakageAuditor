"""The two working rules decline rather than ask. R220 §1.

Both violations they close were self-caught and disclosed, and neither was
judgment failing: in both cases the rule was satisfied as written and defeated in
substance. A specification problem is fixed by tightening the specification, not
by resolving to be more careful — which does not scale, and which this project
already knows does not scale, because that is why `_UNWIRED` refuses rather than
documents.

THE POSITIVES ARE BUILT FROM THE ACTUAL DEFECTS: the exact `-F -` invocation and
the exact `read_text` + `write_text(newline="")` pair, both reproduced here so a
regression fires on the thing that happened rather than on a synthetic cousin.
"""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import safe_edit as se                                            # noqa: E402


# ---------------------------------------------------------------------------
# Rule 2 -- line endings. The positive is the exact pair that converted a
# registered instrument.
# ---------------------------------------------------------------------------

def test_the_EXACT_pair_that_caused_it_still_converts(tmp_path):
    """Not a fix -- the demonstration that the hazard is real and silent.

    If this ever stops converting, the module's whole reason has changed and
    the rest of this file needs re-reading rather than trusting.
    """
    p = tmp_path / "crlf.py"
    p.write_bytes(b"import os\r\nx = 1\r\n")
    text = p.read_text(encoding="utf-8")          # translates CRLF -> LF
    p.write_text(text, encoding="utf-8", newline="")   # writes LF
    assert p.read_bytes().count(b"\r\n") == 0, (
        "the hazard this module exists for no longer reproduces")


@pytest.mark.parametrize("raw", [b"a\r\nb\r\n", b"a\nb\n", b"only one line\r\n",
                                 b"trailing\r\n\r\n"])
def test_edit_preserves_whatever_the_file_had(tmp_path, raw):
    p = tmp_path / "f.txt"
    p.write_bytes(raw)
    before_crlf = raw.count(b"\r\n")
    se.edit(p, lambda t: t.replace("a", "A"))
    after = p.read_bytes()
    assert after.count(b"\r\n") == before_crlf, (
        "line endings changed: %r -> %r" % (raw, after))


def test_edit_on_a_CRLF_file_keeps_CRLF_even_when_adding_lines(tmp_path):
    p = tmp_path / "f.py"
    p.write_bytes(b"import os\r\nx = 1\r\n")
    se.edit(p, lambda t: t + "y = 2\n")
    after = p.read_bytes()
    assert after == b"import os\r\nx = 1\r\ny = 2\r\n", after
    assert after.count(b"\n") == after.count(b"\r\n"), "a bare LF was introduced"


def test_edit_reports_whether_anything_changed(tmp_path):
    p = tmp_path / "f.txt"
    p.write_bytes(b"same\r\n")
    assert se.edit(p, lambda t: t) is False
    assert p.read_bytes() == b"same\r\n"
    assert se.edit(p, lambda t: t.upper()) is True


def test_MIXED_endings_are_refused_rather_than_normalised(tmp_path):
    """Guessing would normalise silently, which is the defect itself."""
    p = tmp_path / "mixed.txt"
    p.write_bytes(b"a\r\nb\nc\r\n")
    with pytest.raises(se.EditRuleError, match="mixed line endings"):
        se.edit(p, lambda t: t)


def test_write_text_refuses_to_guess_a_newline(tmp_path):
    with pytest.raises(se.EditRuleError):
        se.write_text(tmp_path / "x.txt", "a\n", b"\r")


def test_the_registered_paths_round_trip_unchanged():
    """The real files, not synthetic ones. Four are LF and three are CRLF, and
    an edit that changes nothing must change nothing."""
    for rel in ("PREREG.md", "HISTORY.md", "tools/check_registration.py",
                "AVAILABILITY_DECLARATION.md", "DEVIATIONS.md",
                "protocol/runtime_reference.py", "DESIGN.md"):
        p = ROOT / rel
        before = p.read_bytes()
        text, nl = se.read_text(p)
        rebuilt = text.replace("\n", nl.decode())
        assert rebuilt.encode("utf-8") == before, (
            "%s does not round-trip: the reader and writer disagree" % rel)


# ---------------------------------------------------------------------------
# Rule 1 -- `-F` takes a path. The positive is the exact invocation that landed
# a shell command as a commit message.
# ---------------------------------------------------------------------------

def test_dash_is_refused_and_the_refusal_says_why():
    with pytest.raises(se.EditRuleError) as e:
        se.commit("-")
    msg = str(e.value)
    assert "STDIN" in msg and "PATH TO A FILE" in msg, msg


def test_a_path_that_does_not_exist_is_refused(tmp_path):
    with pytest.raises(se.EditRuleError, match="not a file that exists"):
        se.commit(tmp_path / "never_written.txt")


def test_an_empty_message_file_is_refused(tmp_path):
    p = tmp_path / "m.txt"
    p.write_text("   \n\n", encoding="utf-8")
    with pytest.raises(se.EditRuleError, match="empty"):
        se.commit(p)


def test_a_message_that_is_a_SHELL_COMMAND_is_refused(tmp_path):
    """The exact thing that landed at 03b0c6f."""
    p = tmp_path / "m.txt"
    p.write_text('git commit -F "C:/some/path/msg.txt"; echo "exit=$?"\n',
                 encoding="utf-8")
    with pytest.raises(se.EditRuleError) as e:
        se.commit(p)
    assert "heredoc" in str(e.value) or "shell command" in str(e.value)


def test_an_ORDINARY_message_is_NOT_refused(tmp_path, monkeypatch):
    """The negative control. A guard that refuses everything protects nothing,
    and this one must let a real commit message through."""
    p = tmp_path / "m.txt"
    p.write_text("A real subject line\n\nAnd a body explaining it.\n",
                 encoding="utf-8")
    calls = []
    monkeypatch.setattr(se.subprocess, "run",
                        lambda cmd, **kw: calls.append(cmd) or type(
                            "R", (), {"returncode": 0})())
    assert se.commit(p) == 0
    assert calls and calls[0][:4] == ["git", "commit", "-F", str(p)], calls
