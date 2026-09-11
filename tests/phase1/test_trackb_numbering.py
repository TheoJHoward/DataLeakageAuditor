"""The lessons ledger's numbering is unique, checked rather than assumed.

R267 §4 asked whether TB numbering is unique. It was not — two `## TB-25`
headings stood in the file, and one of eight external citations meant the second
one. **A ledger of defect classes exhibiting the count-in-prose defect is TB-25's
own subject**, so the answer is a check and not a correction: a correction fixes
one collision, a check fixes the next one too.

Renumbering is what this must NOT drive anyone to. The rule is the next free
number with a note, so the assertion is uniqueness of the headings, never
contiguity — a gap is fine and closing one by moving an entry would break
citations that already point at it.
"""
from __future__ import annotations

import collections
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "evidence" / "session" / "TRACKB_LESSONS.md"
HEADING = re.compile(r"^##\s+(TB-\d+)\s+—\s*(.*)$")


def _headings():
    out = collections.defaultdict(list)
    for i, line in enumerate(LEDGER.read_text(encoding="utf-8").splitlines(), 1):
        m = HEADING.match(line)
        if m:
            out[m.group(1)].append((i, m.group(2)))
    return out


def test_the_ledger_HAS_entries_so_this_cannot_pass_over_nothing():
    heads = _headings()
    assert len(heads) >= 25, (
        "the heading pattern matched %d entries; if the format changed this "
        "check is measuring nothing" % len(heads))


def test_EVERY_TB_NUMBER_IS_USED_ONCE():
    dupes = {k: v for k, v in _headings().items() if len(v) > 1}
    assert not dupes, (
        "a lessons number used twice makes every citation of it ambiguous, and "
        "the reader cannot tell which entry a past round meant: %s"
        % {k: [ln for ln, _ in v] for k, v in dupes.items()})


def test_CONTIGUITY_IS_NOT_ASSERTED_and_that_is_deliberate():
    """A gap is legal; closing one by renumbering breaks live citations.

    This is asserted rather than left implicit so that a future reader who sees
    a gap does not treat it as a defect to tidy away.
    """
    nums = sorted(int(k.split("-")[1]) for k in _headings())
    assert nums, "no entries parsed"
    # The ledger may or may not be contiguous. Either is fine; what is checked
    # is only that the numbers are distinct, which the sorted set proves.
    assert len(set(nums)) == len(nums)


def test_the_RESOLVED_collision_is_recorded_where_both_readers_arrive():
    text = LEDGER.read_text(encoding="utf-8")
    assert "## TB-28 —" in text, "the collision's second entry took a new number"
    # Both headings carry a note, because a reader lands on one or the other.
    tb25 = text.index("## TB-25 —")
    tb28 = text.index("## TB-28 —")
    for name, start in (("TB-25", tb25), ("TB-28", tb28)):
        window = text[start:start + 1800]
        assert "NUMBERING NOTE" in window, (
            "%s carries no numbering note, so a reader arriving there cannot "
            "learn a collision existed" % name)
