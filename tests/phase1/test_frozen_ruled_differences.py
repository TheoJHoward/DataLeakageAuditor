"""The ruled-difference table, and the count that stops it becoming a solvent.

R223 §1. D17 compares the TAG's checker against the current one on the same tree.
A difference is either RULED — a person looked and decided — or a failure. The
table is the record of the first kind.

WHY IT COULD BECOME A SOLVENT. "Add a ruled-difference entry" would dispose of
every frozen-instrument finding ever raised. Two things stop it, and both are
asserted here rather than intended:

  THE ENTRY RECORDS A TRUE FACT OR IT SUPPRESSES A TRUE FINDING, and the reason
  must be checkable against the two instruments rather than merely stated. This
  is NOT R163 §1's exemption test: the table exists for exactly this, and using a
  mechanism for its designed purpose is not an exemption.

  THE COUNT IS PRE-COMMITTED. N = 4, chosen before there was any pressure on it,
  with a structural reason: twenty-four checks, so four ruled differences is one
  sixth of the instrument declared to disagree with its own frozen form. It is
  not a budget to spend — reaching it means the comparison is re-examined as a
  whole rather than extended a fifth time.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import check_registration as cr                                   # noqa: E402


def test_the_running_count_is_below_its_PRE_COMMITTED_limit():
    n = len(cr._FROZEN_PERMITTED)
    assert n <= cr._FROZEN_PERMITTED_LIMIT, (
        "%d ruled differences against a pre-committed limit of %d. At the limit "
        "the frozen-instrument comparison is RE-EXAMINED AS A WHOLE -- whether "
        "the baseline should be re-cut, whether the differences share a cause, "
        "whether the check still earns its runtime -- and not extended again."
        % (n, cr._FROZEN_PERMITTED_LIMIT))


def test_the_limit_was_set_before_the_entries_reached_it():
    """Not enforceable from the tree, so the property asserted is the margin.

    A limit equal to the count is a limit chosen to fit, and this asserts there
    is room left — which is the observable trace of having chosen it early.
    """
    assert cr._FROZEN_PERMITTED_LIMIT > len(cr._FROZEN_PERMITTED), (
        "the limit equals the current count, which is what choosing it late "
        "looks like from the outside")


def test_every_ruled_difference_carries_a_REASON_in_the_source():
    """A table of names is a list of things silenced. A table with reasons is a
    record of decisions, and the difference is the whole of what makes it not a
    solvent."""
    src = (ROOT / "tools" / "check_registration.py").read_text(encoding="utf-8")
    head = src.split("_FROZEN_PERMITTED = ")[0]
    block = head[head.rindex("# Verdict differences that are RULED"):]
    for name in cr._FROZEN_PERMITTED:
        assert name in block, (
            "%r is in the permitted table with no reason recorded above it. An "
            "entry without a reason is a silence, not a ruling." % name)
        # the reason has to be more than a mention
        idx = block.index(name)
        assert len(block[idx:idx + 400].split("\n")) > 3, (
            "%r's reason is a line rather than a reason" % name)


def test_round_reconciliations_reason_is_CHECKABLE_not_merely_stated():
    """The reason claims two specific, verifiable things about the instruments."""
    src = (ROOT / "tools" / "check_registration.py").read_text(encoding="utf-8")
    head = src.split("_FROZEN_PERMITTED = ")[0]
    assert "HARDCODED absolute path" in head
    assert "LEAKAUDIT_WORK_ROOT" in head
    assert "PERMANENT AND BY DESIGN" in head

    # And the claims are true of the two instruments, not just written down.
    blob = subprocess.run(
        ["git", "show", "%s:tools/check_registration.py" % cr._FROZEN_TAG],
        cwd=str(ROOT), capture_output=True)
    assert blob.returncode == 0, "the tagged checker could not be read"
    frozen = blob.stdout.decode("utf-8", "replace")
    assert "8b1d67a4" in frozen, (
        "the frozen checker does not carry the hardcoded path the reason names, "
        "so the reason describes something else")
    assert cr._WORK_ROOT_ENV not in frozen, (
        "the frozen checker already resolves at run time, so the difference the "
        "reason describes is not the difference that exists")
    current = (ROOT / "tools" / "check_registration.py").read_text(encoding="utf-8")
    assert cr._WORK_ROOT_ENV in current


def test_the_superseded_hardcoded_path_is_still_recorded_in_the_current_one():
    """Deleted, a reader could not check the reason against anything."""
    assert "8b1d67a4" in str(cr._WORK_ROOT_SUPERSEDED)
