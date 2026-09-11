"""No comparison expresses a closed bound as `< instant + one tick`. R267 §4.

**THE CLASS, and why a search proves its absence.** `27582d9` repaired a window
written as `d < f_sec + Timedelta(1, "ns")` where `d <= f_sec` was meant. On
frames at microsecond resolution `np.datetime64(f_sec + 1ns)` truncates back to
`f_sec`, so the strict comparison dropped the row stamped exactly at `f_sec` —
the tie row — on every cohort. **The rule was right and the unit defeated it.**

R241 §3's asymmetry is what makes this checkable: absence of the substring
proves absence of the use, while presence proves nothing. So the sweep is for
the construction, and each hit is classified by hand rather than by the pattern.

Enumerated at R267 across every `.py` in the tree: **two hits, neither a member.**
`availability.py`'s `(1, "ns")` is an entry in a unit-formatting table and
compares nothing. `test_slicing.py`'s `floor - Timedelta(nanoseconds=1)`
subtracts a tick from a **duration** to pin a refusal boundary from both sides —
exact arithmetic with no frame resolution in it, and the intended use of a tick.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

#: Where a member could do harm: anything the probe executes.
SCANNED = ("src", "protocol", "tools")

#: The construction, not the unit. `Timedelta(1, "ns")`, `Timedelta("1ns")`,
#: `Timedelta(nanoseconds=1)` — any spelling of one tick added to something.
TICK = re.compile(r"Timedelta\(\s*(?:1\s*,\s*[\"']ns[\"']"
                  r"|[\"']1\s*ns[\"']|nanoseconds\s*=\s*1)\s*\)")

#: Hits ruled NOT members, with the reason. A hit not listed here fails the
#: test — the point is that a new one gets read, not pattern-matched.
RULED_NOT_MEMBERS = {
    # (relative path, the reason it is not a member)
}


def _hits():
    out = []
    for top in SCANNED:
        for path in (ROOT / top).rglob("*.py"):
            rel = path.relative_to(ROOT).as_posix()
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if TICK.search(line):
                    out.append((rel, i, line.strip()))
    return out


def test_the_scan_REACHES_the_files_it_claims_to():
    """An absence claim over an empty population is not an absence claim."""
    scanned = [p for top in SCANNED for p in (ROOT / top).rglob("*.py")]
    assert len(scanned) > 20, (
        "the sweep walked %d files; if the layout moved this proves nothing"
        % len(scanned))
    # and the pattern is capable of matching, or the zero below is meaningless
    assert TICK.search('x + pd.Timedelta(1, "ns")')
    assert TICK.search("x + pd.Timedelta(nanoseconds=1)")
    assert not TICK.search("pd.Timedelta(seconds=1)")


def test_NO_one_tick_construction_survives_in_an_executed_file():
    unruled = [(f, i, t) for f, i, t in _hits()
               if f not in RULED_NOT_MEMBERS]
    assert not unruled, (
        "a one-tick construction appeared in an executed file. If it expresses "
        "a closed bound as a strict comparison it is the tie-row defect of "
        "27582d9 and the frame's resolution will defeat it; if it is something "
        "else, rule it into RULED_NOT_MEMBERS with the reason: %s" % unruled)


def test_the_REPAIRED_window_is_a_closed_comparison():
    """The fix itself, pinned — so a revert is a test failure, not a silence."""
    src = (ROOT / "src" / "leakaudit" / "availability.py").read_text(
        encoding="utf-8")
    assert "(d_np <= np.datetime64(w_end))" in src, (
        "L2a's closed window must be expressed as closed; `< end + one tick` "
        "is what 27582d9 removed")
    assert 'np.datetime64(w_end + pd.Timedelta(1, "ns"))' not in src
