"""Two working rules, made mechanical rather than written down. R220 §1.

BOTH RULES WERE SATISFIED AS WRITTEN AND DEFEATED IN SUBSTANCE, which is a
specification problem rather than a care problem — and this project already knows
that resolving to be more careful does not scale, because that is why
`contract._UNWIRED` refuses rather than documents. So both tightenings are code
that declines, not sentences that ask.

RULE 1 — `-F` TAKES A PATH.
    The standing rule is that every commit message goes through `-F` from a file.
    `git commit -F -` reads STDIN, which is the exact shell-quoting path the rule
    exists to eliminate: the letter satisfied, the purpose defeated, wearing the
    flag's own name. It happened, and the message that landed was the shell
    command text. That is the discarded-parameter shape a fourth time — a
    mechanism that appears to be applied and is not.

RULE 2 — A PROGRAMMATIC EDIT PRESERVES LINE ENDINGS.
    `Path.read_text()` performs universal-newline translation, turning CRLF into
    LF in memory. `Path.write_text(..., newline="")` writes exactly what it is
    given. The pair silently converts a whole file. It converted
    `tools/check_registration.py` — a registered path — from 3,189 CRLF endings
    to LF, turning a 58-line change into a 6,429-line diff.

    THE DAMAGE IS NOT THE ENDINGS. It is that a 6,429-line diff hides a 58-line
    one, and every review of that instrument, including the delta-of-findings
    comparison, depends on the diff being readable.

    `.gitattributes` ALREADY CARRIES `* -text`, so git stores and checks out
    byte-exact and never converts. The protection was in place; the defect was a
    Python edit operating above it. A per-path `eol=` pin would ENABLE text
    conversion for those paths, which is the opposite of what is wanted, and
    would rewrite the four registered files that are LF today. So the pin is not
    tightened and the byte-preserving edit rule stands alone.
"""
from __future__ import annotations

import pathlib
import subprocess


class EditRuleError(RuntimeError):
    """A working rule declined the operation."""


# ---------------------------------------------------------------------------
# Rule 2 — byte-preserving edits
# ---------------------------------------------------------------------------

def dominant_newline(data: bytes) -> bytes:
    """`b"\\r\\n"` or `b"\\n"`, whichever the file actually uses."""
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    if crlf and lf:
        raise EditRuleError(
            "mixed line endings (%d CRLF, %d bare LF): an edit cannot preserve "
            "what the file does not consistently have, and guessing would "
            "normalise it silently, which is the defect this module exists for"
            % (crlf, lf))
    return b"\r\n" if crlf else b"\n"


def read_text(path) -> tuple[str, bytes]:
    """Text with `\\n` separators, plus the file's ACTUAL newline, to write back.

    Returns the pair deliberately. A function returning only the text invites
    the caller to write it with whatever default is at hand, which is exactly
    how the conversion happened.
    """
    p = pathlib.Path(path)
    raw = p.read_bytes()
    nl = dominant_newline(raw)
    return raw.decode("utf-8").replace("\r\n", "\n"), nl


def write_text(path, text: str, newline: bytes) -> None:
    """Write `text`, restoring `newline`. Refuses to guess."""
    if newline not in (b"\r\n", b"\n"):
        raise EditRuleError("newline must be b'\\r\\n' or b'\\n', got %r" % (newline,))
    data = text.replace("\r\n", "\n").encode("utf-8")
    if newline == b"\r\n":
        data = data.replace(b"\n", b"\r\n")
    pathlib.Path(path).write_bytes(data)


def edit(path, transform) -> bool:
    """Apply `transform(text) -> text`, preserving the file's line endings.

    Returns whether anything changed. The whole point is that a caller cannot
    accidentally normalise: the newline never passes through the caller's hands.
    """
    text, nl = read_text(path)
    new = transform(text)
    if new == text:
        return False
    write_text(path, new, nl)
    return True


# ---------------------------------------------------------------------------
# Rule 1 — `-F` takes a path
# ---------------------------------------------------------------------------

#: The trailer this route asks git to append. R268 §1. `.githooks/commit-msg`
#: refuses any message whose final trailer block lacks it, so a message typed
#: with `git commit -m` -- which passed through the shell -- is refused before it
#: lands. ONE definition: the hook imports it from here rather than restating it.
#: A TRIPWIRE, NOT A PROOF -- see tools/commit_msg_hook.py for what it does not do.
COMMIT_TRAILER = "Committed-Via: tools/safe_edit.commit"


def commit_gate(repo=None) -> list:
    """Reasons a commit of this working tree is refused. Empty: it may land.

    R272 §2(g), the mechanism for D-V30A-117.

    A SUITE RUN MATCHING THIS TREE. `tools/suite_tree_record.json` carries the
    fingerprint of the working tree the last `pytest tests` run measured, and it
    has to equal the tree's fingerprint now and be a whole-suite run. A suite,
    then an edit, then a commit is refused; so is a commit with no suite at all.
    Records-only commits get the same rule, because the suite reads the records.

    A GUARD RUN MATCHING THE PROBE PATH. When the staged change touches a file in
    `PROBE_PATH_SET.json`'s path set, a completed run in
    `tools/wholeframe_guard_times.json` has to have recorded the path set's
    current content. The guard writes that file only after its eight terms held.
    """
    import json

    import probe_path_guard as ppg
    import tree_fingerprint as tf

    root = pathlib.Path(repo) if repo else pathlib.Path(__file__).resolve().parents[1]
    problems = []
    fp = tf.fingerprint(root)
    try:
        last = json.loads((root / "tools" / "suite_tree_record.json")
                          .read_text(encoding="utf-8")).get("last") or {}
    except Exception as e:                                   # noqa: BLE001
        last = None
        problems.append("NO SUITE RECORD could be read at "
                        "tools/suite_tree_record.json (%s). Run `py -3.12 -m "
                        "pytest tests` as the last step before committing." % e)
    if last is not None:
        if last.get("tree_fingerprint") != fp["digest"]:
            problems.append(
                "NO SUITE RUN MATCHES THIS WORKING TREE: the suite record's "
                "fingerprint is %s and this tree's is %s (HEAD %s, %d changed "
                "file(s)). Something changed after the suite ran, or it never "
                "ran on this tree. Run `py -3.12 -m pytest tests` as the last "
                "step before committing."
                % (str(last.get("tree_fingerprint"))[:12], fp["digest"][:12],
                   fp["head"][:7], len(fp["files"])))
        elif not last.get("full_suite"):
            problems.append(
                "the suite run matching this tree was not the whole suite; its "
                "arguments were %r." % (last.get("args"),))
    staged = subprocess.run(["git", "-C", str(root), "diff", "--cached",
                             "--name-only"], capture_output=True, text=True,
                            encoding="utf-8").stdout.splitlines()
    pset = ppg.path_set()
    touched = sorted({s.strip() for s in staged if s.strip()} & pset)
    if touched:
        want = tf.path_set_fingerprint(pset, root)
        try:
            runs = json.loads((root / "tools" / "wholeframe_guard_times.json")
                              .read_text(encoding="utf-8")).get("runs", [])
        except Exception:                                    # noqa: BLE001
            runs = []
        if not any(r.get("path_set_fingerprint") == want for r in runs):
            problems.append(
                "PROBE-PATH COMMIT WITHOUT A MATCHING GUARD RUN: this commit "
                "touches %s, and no completed run in "
                "tools/wholeframe_guard_times.json recorded the path set's "
                "current content (%s). Run the whole-frame guard on this content "
                "first." % (", ".join(touched), want[:12]))
    return problems


def commit(message_file, repo=None, extra=(), gate=True) -> int:
    """`git commit -F <path>`, refusing every way of not doing that.

    Refuses `-`, refuses a path that does not exist, refuses an empty file, and
    refuses a message that looks like a shell command — the specific thing that
    landed when a heredoc leaked into `-F -`.

    Appends `COMMIT_TRAILER` with `--trailer`, so git adds it and the message
    file on disk is never modified. Since R268 the commit-msg hook refuses any
    message without it.

    Since R272 it also refuses a tree no suite run matches, and a probe-path
    change no guard run matches -- see `commit_gate`.
    """
    if str(message_file).strip() == "-":
        raise EditRuleError(
            "`-F -` reads STDIN. The rule is a PATH TO A FILE ON DISK, because "
            "the shell-quoting path is what the rule exists to eliminate. "
            "Write the message to a file first.")
    p = pathlib.Path(message_file)
    if not p.is_file():
        raise EditRuleError(
            "%s is not a file that exists. `-F` takes a path, and the file is "
            "written before the command runs." % p)
    body = p.read_text(encoding="utf-8", errors="replace")
    if not body.strip():
        raise EditRuleError("%s is empty; a commit message is not nothing" % p)
    first = body.strip().split("\n", 1)[0]
    if first.startswith(("git ", "python ", "cd ", "$ ")) or "; echo " in first:
        raise EditRuleError(
            "the first line of %s reads like a shell command (%r). That is what "
            "landed when a heredoc leaked into `-F -`, and it is refused rather "
            "than committed." % (p, first[:70]))
    # THE TRAILER, ADDED BY GIT RATHER THAN WRITTEN INTO THE FILE. R268 §1. The
    # first edit for this round changed the docstring above and left this line
    # as it was, so the route would have been refused by its own hook; the test
    # asking for `--trailer` here is what caught it.
    # THE TREE HAS TO BE ONE A SUITE MEASURED. R272 §2(g). Refused before git
    # is asked to commit anything, with every reason at once.
    if gate:
        problems = commit_gate(repo)
        if problems:
            raise EditRuleError(
                "COMMIT REFUSED (R272 section 2(g)):\n  - "
                + "\n  - ".join(problems))
    cmd = ["git", "commit", "-F", str(p), "--trailer", COMMIT_TRAILER, *extra]
    return subprocess.run(cmd, cwd=str(repo) if repo else None).returncode
