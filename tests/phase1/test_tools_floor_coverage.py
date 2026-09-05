"""Which repository tools are exercised on the declared floor. R229 §3.

THE ABSENCE CLAIM THIS REPLACES. R228 reported "other tools are unexamined, not
confirmed clean" — correct phrasing, and an absence claim with no population.
The corner suite run sweeps everything the SUITE exercises; what it cannot reach
is a `tools/` entry no test imports. So the entries are partitioned.

TOTALITY, the same shape the config-key complement and the Track B families use:
every file in `tools/` is in EXACTLY ONE of two classes, and the two cover the
directory. A new tool fails this file until somebody places it, which is the
point — placing it is the work.

    COVERED     a test imports it, so the corner suite run executed it on
                CPython 3.11.9. The naming test below requires the test file
                to exist.
    UNEXAMINED  no test imports it. The corner run says nothing about it, and
                this file says so rather than letting the suite's green stand
                in for coverage.

WHAT "COVERED" DOES AND DOES NOT MEAN. It means the module was imported and its
tested paths ran on the floor interpreter. It does NOT mean every function did:
`probe_path_guard` is covered, and covered is exactly how its 3.12-only
`sys.monitoring` path was found — three tests failing on 3.11 (D-V30A-58). A tool
with thin tests can be covered and still hide a floor break in an untested branch.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
TESTS = ROOT / "tests"

for p in (str(ROOT), str(ROOT / "src"), str(TOOLS)):
    if p not in sys.path:
        sys.path.insert(0, p)

# module -> the test file whose import puts it on the floor run's path.
COVERED = {
    "check_registration": "tests/phase1/test_work_root_resolution.py",
    "default_sites": "tests/phase1/test_default_sites.py",
    "floor_check": "tests/phase1/test_floor_check.py",
    "opt_in_currency": "tests/phase1/test_opt_in_currency.py",
    "portability_digest": "tests/phase1/test_portability_digest.py",
    "probe_path_guard": "tests/phase1/test_probe_path_guard.py",
    "safe_edit": "tests/phase1/test_safe_edit.py",
}

# module -> why nothing reaches it. Not an excuse; a statement of the gap.
UNEXAMINED = {
    "work_root_baseline": (
        "no test imports it. `tests/phase1/test_work_root_baseline.py` tests the "
        "CHECK that reads the baseline -- `check_registration."
        "check_round_reconciliation` -- and not the writer that produces it. The "
        "writer is run by hand once a round and its behaviour on the floor "
        "interpreter is unmeasured. Found by this enumeration, which is what the "
        "enumeration is for."),
}


def _modules() -> set[str]:
    return {p.stem for p in TOOLS.glob("*.py") if not p.stem.startswith("_")}


def test_every_tool_is_in_exactly_one_class():
    mods = _modules()
    both = set(COVERED) & set(UNEXAMINED)
    assert not both, "in two classes at once, so unclassified: %s" % sorted(both)
    missing = mods - set(COVERED) - set(UNEXAMINED)
    assert not missing, (
        "these tools are in tools/ and in neither class, so nothing here says "
        "whether the floor run reaches them. Place each one: %s" % sorted(missing))
    stray = (set(COVERED) | set(UNEXAMINED)) - mods
    assert not stray, (
        "named here and not present in tools/, so this is a claim about files "
        "that are gone: %s" % sorted(stray))


def test_every_COVERED_tool_really_is_imported_by_the_test_named():
    """A hand-written map drifts from the code, which is the failure this
    project keeps recording. So the map is checked against the tests."""
    for mod, testfile in COVERED.items():
        p = ROOT / testfile
        assert p.is_file(), "%s names %s, which does not exist" % (mod, testfile)
        text = p.read_text(encoding="utf-8")
        assert re.search(r"^\s*(import %s\b|from %s import)" % (mod, mod),
                         text, re.M), (
            "%s is classified COVERED by %s, and that file does not import it"
            % (mod, testfile))


def test_no_UNEXAMINED_tool_is_actually_imported_by_a_test():
    """The other direction. A stale 'unexamined' entry understates coverage and
    would send someone to write a test that already exists."""
    for mod in UNEXAMINED:
        hits = [p for p in TESTS.rglob("test_*.py")
                if re.search(r"^\s*(import %s\b|from %s import)" % (mod, mod),
                             p.read_text(encoding="utf-8"), re.M)]
        assert not hits, (
            "%s is declared unexamined and %s imports it"
            % (mod, [str(h.relative_to(ROOT)) for h in hits]))


def test_every_UNEXAMINED_entry_carries_a_REASON():
    for mod, reason in UNEXAMINED.items():
        assert len(reason) > 80, (
            "%r is declared unexamined with no real reason. 'Unexamined' "
            "without one is the same silence as not having looked: %r"
            % (mod, reason))


def test_the_known_floor_break_is_in_a_COVERED_tool():
    """The enumeration's own discriminating case. D-V30A-58 was found because a
    test exercised the tool on 3.11; if `probe_path_guard` were unexamined, the
    break would still be undiscovered — and this assertion would be the thing
    that failed if somebody removed the coverage that found it."""
    assert "probe_path_guard" in COVERED
    src = (TOOLS / "probe_path_guard.py").read_text(encoding="utf-8")
    assert "sys.monitoring" in src
    assert "3.12+" in src, (
        "the 3.12-only requirement is no longer named in the file that has it")
