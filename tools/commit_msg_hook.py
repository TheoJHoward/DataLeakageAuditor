#!/usr/bin/env python3
"""commit-msg hook: refuse a message that did not come through `safe_edit.commit`.

    installed as  .githooks/commit-msg   with  core.hooksPath = .githooks

Exit 0 when the message's final trailer block carries `safe_edit.COMMIT_TRAILER`,
1 otherwise -- and 1 on ANY failure to read or parse, because a hook that cannot
see is not a hook that passes.

**R268 §1, AND THE RULES IT MECHANISES.** Two durable rules broke in one command
at R267: a message passed with `-m` instead of `-F` from a file, and backticks
in that shell argument. It landed intact by luck. Both rules were enforced by
discipline alone in the round whose subject was mechanisms over discipline.

`safe_edit.commit` is the only route that takes a message from a file on disk,
and it now asks git to append `COMMIT_TRAILER`. A message carrying the trailer
came through that route; a message typed with `-m` does not carry it and is
refused **before it lands**. Because the file never passes through a shell,
backticks in COMMIT MESSAGES close with it.

**WHAT THIS DOES NOT DO, stated so the hook does not imply more than it covers.**

  * It is a TRIPWIRE, NOT A PROOF. Git does not tell a hook whether `-m` or `-F`
    was used, so a person who types the trailer by hand after `-m` passes. What
    it closes is the ACCIDENTAL route -- which is the one that happened.
  * It sees commit messages and nothing else. Backticks in every OTHER shell
    argument remain a rule enforced by discipline; no hook sees a shell.
  * It lives in a per-clone setting. `certify_preconditions` refuses to certify a
    clone where `core.hooksPath` does not resolve to the tracked directory, which
    is what makes the setting stick.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

REFUSAL = (
    "commit refused by .githooks/commit-msg (R268 section 1).\n"
    "The message does not carry the trailer `tools/safe_edit.commit` appends, so "
    "it did not come through the one route that takes a message from a FILE ON "
    "DISK. `git commit -m` passes the message through the shell -- the path the "
    "`-F` rule and the backtick rule exist to close.\n"
    "Write the message to a file with the Write tool, then commit with "
    "`tools/safe_edit.commit(<path>)`.")


def final_trailer_block(text: str) -> list:
    """Lines of the last paragraph, which is where git puts trailers.

    Matching the trailer ANYWHERE would let a message body that quotes it on its
    own line pass -- a disclosure about this hook, for instance. Git's trailers
    are the final paragraph, so that is the only place looked.
    """
    lines = [ln.rstrip() for ln in text.splitlines()
             if not ln.lstrip().startswith("#")]
    while lines and not lines[-1].strip():
        lines.pop()
    block = []
    for ln in reversed(lines):
        if not ln.strip():
            break
        block.append(ln.strip())
    return list(reversed(block))


def check(text: str) -> tuple:
    """(ok, reason). Pure, so the rule is testable without a repository."""
    from safe_edit import COMMIT_TRAILER
    if COMMIT_TRAILER in final_trailer_block(text):
        return True, "carries %r" % COMMIT_TRAILER
    return False, REFUSAL


HOOKS_DIR = ".githooks"
HOOK_FILE = "commit-msg"

#: The ONLY git subcommands this module may run, and both only read. R268 §1(b).
#: `certify_preconditions` is pinned to contain no subprocess call, because it
#: exists to GATE certification and never to execute a step. Whether the hook
#: is installed is a read of git's own state, not a step -- so the read lives
#: here, behind this allow-list, and a test pins the allow-list. Stated rather
#: than slipped past: the pin is textual, and routing around a textual pin
#: silently would be the loophole it exists to deny.
READ_ONLY_GIT = ("config", "ls-files")


def _git_read(root, *args) -> tuple:
    if not args or args[0] not in READ_ONLY_GIT:
        raise ValueError("commit_msg_hook may run only %s, not %r"
                         % (READ_ONLY_GIT, args[:1]))
    import subprocess
    r = subprocess.run(["git", "-C", str(root), *args],
                       capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def installed(repo=None) -> tuple:
    """(ok, message): is the hook live for THIS clone? R268 §1(b).

    Two facts, because either one missing leaves `-m` open:

      * `core.hooksPath`, set LOCALLY, resolves to the tracked `.githooks`. It is
        a per-clone setting and git never copies it; a global value would pass
        for this machine and fail for the next, so only `--local` counts.
      * the hook is TRACKED at mode 100755. On a checkout that honours the bit,
        a 100644 hook is present and silently skipped.
    """
    root = pathlib.Path(repo) if repo else HERE.parent
    rc, configured = _git_read(root, "config", "--local", "--get",
                               "core.hooksPath")
    if rc != 0 or not configured:
        return False, ("core.hooksPath is not set in this clone, so "
                       ".githooks/commit-msg never runs and a message typed with "
                       "`git commit -m` lands. Set it: "
                       "git config core.hooksPath .githooks")
    p = pathlib.Path(configured)
    resolved = (p if p.is_absolute() else root / p).resolve()
    want = (root / HOOKS_DIR).resolve()
    if resolved != want:
        return False, ("core.hooksPath resolves to %s, not the tracked %s, so "
                       "the hook this repository ships is not the one git runs"
                       % (resolved, want))
    if not (want / HOOK_FILE).is_file():
        return False, "%s/%s is missing" % (HOOKS_DIR, HOOK_FILE)
    _, ls = _git_read(root, "ls-files", "-s", "--",
                      "%s/%s" % (HOOKS_DIR, HOOK_FILE))
    mode = ls.split()[0] if ls else ""
    if mode != "100755":
        return False, ("%s/%s is tracked as %s, not 100755, so a checkout that "
                       "honours the bit gets a hook git will not execute"
                       % (HOOKS_DIR, HOOK_FILE, mode or "UNTRACKED"))
    return True, ("core.hooksPath -> %s (local); %s/%s tracked 100755"
                  % (configured, HOOKS_DIR, HOOK_FILE))


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        text = pathlib.Path(argv[0]).read_text(encoding="utf-8",
                                               errors="replace")
        ok, reason = check(text)
    except Exception as e:                                   # noqa: BLE001
        print("commit-msg hook could not read or check the message (%s: %s), "
              "so it REFUSES: a hook that cannot see is not a hook that passes."
              % (type(e).__name__, e), file=sys.stderr)
        return 1
    if ok:
        return 0
    print(reason, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
