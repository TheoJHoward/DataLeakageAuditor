#!/usr/bin/env python3
"""The certification step set, and the preconditions without which it is partial.

    $ py -3.12 tools/certify_preconditions.py

Exit 0 when every precondition is met, 1 otherwise. Run BEFORE certifying.

**WHY THIS EXISTS.** *"Certified"* is an absence claim over the certification
STEPS — no required step was skipped — and for a whole session it meant "the
commands I happened to run passed." Certification is several commands, and
nothing ensured all of them ran or that their preconditions were met.

**THE SPECIFIC SKIP IT CLOSES.** `round_reconciliation` reads its population from
`LEAKAUDIT_WORK_ROOT`. Run without it, the check returns **PASS** while printing
*"COVERAGE IS ZERO … This is not a pass."* — the message and the verdict
disagree, because the zero-coverage branch emits its finding as a NOTE. Every
gate result reported across that session ran that way, so a working instrument
was silently zeroed by the command that ran it. **R227's rule, turned on the
operator: an invocation is not the invocation.**

**WHAT THIS IS NOT.** It does not RUN the steps. A single entrypoint that runs
every step and fails if any is skipped is the structural close, and it is a
decision about how certification is invoked rather than something to add in a
round's tail. This enumerates and gates the preconditions; the sequence is still
typed.

**AND IT IS A SIBLING.** `tools/check_registration.py` is verdict-frozen against
the tagged instrument with a ceiling of four ruled differences. R243: new
verification stands beside it, not inside it. The verdict-message contradiction
above lives in that frozen file and is recorded for the next registration rather
than patched here — with this precondition in place, the contradicting branch is
never reached.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

import os
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]

WORK_ROOT_ENV = "LEAKAUDIT_WORK_ROOT"
FIXTURE_ENV = "LEAKAUDIT_FIXTURE"

#: THE STEP SET. R248 §1(a). "All steps ran" is an absence claim and this is its
#: population, stated in one place so a runner is not reconstructing it.
STEPS = (
    ("py -3.12 tools/clean_tree.py",
     "always",
     "the working tree is the one shipping; every instrument after this "
     "measures a tree and which tree is the whole question (R247 §1)"),
    ("LEAKAUDIT_WORK_ROOT=<this round's work root> "
     "py -3.12 tools/scratch_drift.py",
     "always",
     "no round work sits outside the work root. Option B keeps the root a "
     "dedicated scratch subdirectory so `tasks/` falls outside it and no "
     "frozen exclusion is needed -- and the price is that scratch written "
     "elsewhere leaves the reconciliation's population silently, which is how "
     "49 files stayed invisible for many rounds. Its unit tests are all "
     "synthetic, so THIS step is what exercises it against the real layout "
     "(R253 §1)"),
    ("LEAKAUDIT_WORK_ROOT=<this round's work root> "
     "py -3.12 tools/check_registration.py --stage prereg",
     "always",
     "the frozen checker. The variable is NOT optional: without it "
     "round_reconciliation reconciles nothing and says so in a note while "
     "returning PASS (R248 §0)"),
    ("py -3.12 tools/manifest_verify.py",
     "always",
     "every attested hash matches its file. The gate checks manifest COVERAGE "
     "and never content (R242, R243)"),
    ("py -3.12 -m pytest tests",
     "always",
     "the suite, on the committed tree"),
    ("py -3.12 tools/suite_tree.py",
     "always",
     "the suite ran on THIS tree. It records HEAD and the clean status as it "
     "runs; this refuses when that is not HEAD now, or the tree was dirty, or "
     "the run was narrower than `tests`. Without it, `on the committed tree` "
     "above was an ordering somebody remembered (R267 §1.1, D-V30A-102)"),
    ("LEAKAUDIT_FIXTURE=1 py -3.12 tools/wholeframe_guard.py",
     "when a probe-path file moved",
     "the whole-frame path is byte-for-byte the committed population run. "
     "Required whenever any file in PROBE_PATH_SET.json's path_set changed "
     "since the last SAME run"),
)


class PreconditionUnmet(Exception):
    """A precondition could not be satisfied, so certification would be partial."""


def check_work_root() -> tuple:
    """(ok, message). The one that was actually skipped."""
    raw = os.environ.get(WORK_ROOT_ENV)
    if not raw:
        return False, (
            "%s is unset. `round_reconciliation` would reconcile NOTHING and "
            "return PASS while printing 'COVERAGE IS ZERO ... This is not a "
            "pass'. That is how a working instrument was zeroed for a whole "
            "session. Set it to the directory this round's scratch work lives "
            "in -- the directory itself, not a subdirectory of it: 49 files sat "
            "one level above a too-narrow root and never entered the "
            "population (R248 §4)." % WORK_ROOT_ENV)
    p = pathlib.Path(raw)
    if not p.exists():
        return False, (
            "%s names %s, which does not exist. A path that is not there is a "
            "configuration error, not an empty round." % (WORK_ROOT_ENV, p))
    if not p.is_dir():
        return False, "%s names %s, which is not a directory." % (WORK_ROOT_ENV, p)
    return True, "%s -> %s" % (WORK_ROOT_ENV, p)


def check_commit_hook() -> tuple:
    """The commit-msg hook is live for this clone. R268 §1(b).

    A per-clone git setting does not travel with the repository, so without a
    precondition a fresh clone would carry the hook file and never run it. This
    is what makes the setting stick: a clone without it cannot certify.

    The read happens in `commit_msg_hook.installed`, not here, and this file
    still runs nothing -- see that module's `READ_ONLY_GIT` for why the query
    lives there and what bounds it.
    """
    try:
        tools = str(REPO / "tools")
        if tools not in sys.path:
            sys.path.insert(0, tools)
        import commit_msg_hook
    except Exception as e:                                   # noqa: BLE001
        return False, ("the commit-msg hook's tool cannot be imported (%s), so "
                       "whether the hook is live cannot be known" % e)
    return commit_msg_hook.installed(REPO)


def preconditions() -> list:
    """[(name, ok, message)] for every precondition certification depends on."""
    ok, msg = check_work_root()
    hook_ok, hook_msg = check_commit_hook()
    return [("work root", ok, msg), ("commit hook", hook_ok, hook_msg)]


def main(argv=None) -> int:
    print("CERTIFICATION STEP SET -- %d steps" % len(STEPS))
    for cmd, when, why in STEPS:
        print("  [%s] %s" % (when, cmd))
        print("      %s" % why)
    print()
    print("PRECONDITIONS")
    failed = 0
    for name, ok, msg in preconditions():
        print("  %-12s %s  %s" % (name, "OK  " if ok else "UNMET", msg))
        if not ok:
            failed += 1
    print()
    if failed:
        print("REFUSED. %d precondition(s) unmet, so certification would run a "
              "step over an empty population and report a pass. Nothing here "
              "ran the steps -- it refused to let them be run incompletely."
              % failed)
        return 1
    print("Preconditions met. The step set above is what certification requires; "
          "this does not run it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
