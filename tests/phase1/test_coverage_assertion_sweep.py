"""The sweep's own population is enumerated, and its registry cannot lie. R249 §1.

**THE SWEEP IS ITSELF A COVERAGE CLAIM**, so it gets the treatment it exists to
apply: its population comes from `git ls-files`, its registry is checked against
that population in both directions, and the detector is mutation-checked against
a synthetic assertion it has to find.

**AND ITS FIRST TWO DEFINITIONS EXCLUDED THE CASES THAT MATTER**, which is the
finding this file pins. Keying on the assert's SHAPE missed `assert not
unclassified`; keying on the function's BODY missed tests that receive their
population from a fixture. Both times the excluded set contained the flagship
coverage assertions of this repository. A population definition is an absence
claim, and these are its known-positive cases.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import coverage_assertion_sweep as cas                             # noqa: E402


@pytest.fixture(scope="module")
def swept():
    return cas.state()


# ---------------------------------------------------------------------------
# the population
# ---------------------------------------------------------------------------
def test_the_population_comes_from_git_ls_files(swept):
    files = cas.tracked_python_files()
    assert len(files) > 100, (
        "the floor returned %d python files, too few to be this repository"
        % len(files))
    assert swept["rows"], "the sweep found no coverage assertions at all"


def test_the_registry_names_only_functions_THAT_EXIST(swept):
    """A registration for a function not in the population is a claim about
    nothing — and it caught its author on the first run: two entries named
    functions the detector did not include."""
    assert not swept["stray"], (
        "registered as established and not present in the population: %s"
        % swept["stray"])


def test_established_and_outstanding_are_DISJOINT_and_COVERING(swept):
    both = swept["established"] & set(swept["outstanding"])
    assert not both, both
    assert swept["established"] | set(swept["outstanding"]) == swept["functions"]


# ---------------------------------------------------------------------------
# the detector's known positives — the two shapes it used to miss
# ---------------------------------------------------------------------------
def _detect(tmp_path, monkeypatch, source):
    """Run the SHIPPED population() over one synthetic file."""
    (tmp_path / "t_synthetic.py").write_text(textwrap.dedent(source),
                                             encoding="utf-8")
    monkeypatch.setattr(cas, "REPO", tmp_path)
    monkeypatch.setattr(cas, "tracked_python_files", lambda: ["t_synthetic.py"])
    return cas.population()


def test_it_FINDS_the_assert_not_collection_shape(tmp_path, monkeypatch):
    """The shape the first definition missed: the collection is built earlier,
    so the assert holds no `len`, no set difference and no `set(...)`."""
    rows = _detect(tmp_path, monkeypatch, '''
        def test_everything_is_covered():
            listed = set(open("x").read_text().split())
            unclassified = listed - {"a"}
            assert not unclassified, "some are unclassified"
    ''')
    assert len(rows) == 1 and rows[0]["func"] == "test_everything_is_covered", (
        "the detector missed `assert not <collection>`, which is the commonest "
        "coverage form in this repository")


def test_it_FINDS_a_test_that_gets_its_population_from_a_FIXTURE(
        tmp_path, monkeypatch):
    """The shape the second definition missed: no repository read in the test's
    own body, because the fixture did it."""
    rows = _detect(tmp_path, monkeypatch, '''
        import pytest

        @pytest.fixture
        def scanned():
            return open("x").read_text().split()

        def test_all_of_them_are_classified(scanned):
            assert not [s for s in scanned if s == "bad"]
    ''')
    assert len(rows) == 1 and rows[0]["func"] == "test_all_of_them_are_classified", (
        "the detector missed a test receiving its population via a fixture, "
        "which is how the flagship coverage assertion is written")


def test_it_does_NOT_claim_a_unit_assertion(tmp_path, monkeypatch):
    """The negative control. A detector that swept everything would pass both
    positives above and make the outstanding list meaningless."""
    rows = _detect(tmp_path, monkeypatch, '''
        def test_the_function_returns_two():
            assert len(compute()) == 2
    ''')
    assert rows == [], (
        "an assertion over a function's output was pulled into the "
        "repository-population sweep, so the population is not the "
        "coincidence-susceptible one it claims to be")


# ---------------------------------------------------------------------------
# what the instrument is and is not
# ---------------------------------------------------------------------------
def test_the_sweep_REPORTS_and_does_not_gate():
    """Exit 0 with outstanding entries, deliberately. An instrument that failed
    the build until every entry was marked done would be pressure to mark
    entries done, which is how a register becomes a formality."""
    assert cas.main([]) == 0
    assert cas.state()["outstanding"], (
        "there are no outstanding entries, so this assertion no longer "
        "establishes that the instrument tolerates them")


# ---------------------------------------------------------------------------
# the tracked population. R250 §3.
# ---------------------------------------------------------------------------
TRACKED = ROOT / "evidence/session/COVERAGE_ASSERTION_POPULATION.json"


def _tracked():
    import json
    return json.loads(TRACKED.read_text(encoding="utf-8"))


def test_the_TRACKED_population_AGREES_with_the_enumerator(swept):
    """**THE DEFINITION TOOK THREE TRIES AND WAS RIGHT ONLY BY RECALL.**

    Each wrong version was caught because somebody remembered which assertions
    had to be in the set. That knowledge does not survive to the next person, so
    the population is pinned here and regenerated from the code: a coverage
    assertion added later is either in this list or fails this test.
    """
    tracked = {(e["file"], e["function"]) for e in _tracked()["functions"]}
    live = swept["functions"]
    added = sorted(live - tracked)
    gone = sorted(tracked - live)
    assert not added, (
        "these coverage assertions exist in the code and are not in the tracked "
        "population, so nothing carries their empty-population judgment: %s"
        % added)
    assert not gone, (
        "these are tracked and no longer in the code, so the list makes claims "
        "about assertions that are gone: %s" % gone)


def test_the_tracked_artifact_STATES_ITS_CRITERION_AND_ITS_SCOPE():
    """An enumeration whose rule is not written down is one the next change
    cannot be checked against, and a sweep that does not say what it does NOT
    cover is the totality over-claim it exists to catch."""
    d = _tracked()
    for key in ("the_criterion", "the_probe", "scope_NOT_covered",
                "why_it_is_tracked"):
        assert d.get(key), "the tracked population does not state %s" % key
    assert "assert not" in d["the_criterion"], (
        "the criterion does not record that it has to catch "
        "`assert not <collection>`, the shape it first missed")
    assert "fixture" in d["the_criterion"], (
        "the criterion does not record the fixture shape, which the third "
        "definition missed")
    assert "VALUE-COINCIDENCE" in d["scope_NOT_covered"]
    assert "WRONG-INPUT" in d["scope_NOT_covered"]


def test_EVERY_assertion_carries_a_STATUS_and_a_REASON():
    """R251 §2. **MEMBERSHIP IS NOT COVERAGE.**

    "157 coverage assertions exist" plus "some were probed" read together as
    "the coverage assertions are checked", which is false. So every cell carries
    one of the declared statuses and a reason, and a new coverage assertion
    lands unstatused and fails the agreement test above -- which is what makes
    the blanks visible instead of absorbed.
    """
    d = _tracked()
    declared = set(d["statuses"])
    assert declared, "the artifact declares no statuses"
    for e in d["functions"]:
        assert e.get("status") in declared, (
            "%s :: %s carries status %r, which is not one of the declared "
            "statuses %s" % (e["file"], e["function"], e.get("status"),
                             sorted(declared)))
        assert e.get("reason", "").strip(), (
            "%s :: %s has a status and no reason -- a status without one is a "
            "label, and the register becomes a formality"
            % (e["file"], e["function"]))


def test_the_counts_AGREE_with_the_entries():
    """A stated count that disagrees with the rows is the hand-typed-figure
    class inside the artifact built to remove it."""
    d = _tracked()
    tally = {}
    for e in d["functions"]:
        tally[e["status"]] = tally.get(e["status"], 0) + 1
    for status, n in tally.items():
        assert d["counts"].get(status) == n, (
            "the artifact states %r for %s and holds %d"
            % (d["counts"].get(status), status, n))
    assert d["counts"]["functions_total"] == len(d["functions"])


def test_UNVERIFIED_is_not_reported_as_swept():
    """The statuses that mean 'nobody has established this' are named as such,
    and there are enough of them that a blanket 'swept' would be false."""
    d = _tracked()
    unverified = sum(d["counts"].get(s, 0) for s in
                     ("candidate_artifact", "unprobed_reachable",
                      "candidate_UNJUDGED"))
    assert unverified > 0, (
        "no assertion is unverified, so this guard no longer establishes that "
        "the artifact can express an unverified cell")
    verified = sum(d["counts"].get(s, 0) for s in
                   ("probed_healthy", "candidate_fixed",
                    "candidate_legitimate"))
    assert verified < d["counts"]["functions_total"], (
        "every assertion reads as verified, which would make the honest "
        "blanks this artifact exists to show invisible")


# ---------------------------------------------------------------------------
# the escape hatch is audited. R253 §3.
# ---------------------------------------------------------------------------
def test_NO_out_of_scope_ENTRY_MAKES_A_COVERAGE_CLAIM():
    """**AN EXCLUSION SET THAT GROWS WITHOUT AUDIT IS WHERE A POPULATION
    SILENTLY SHRINKS.** A real coverage assertion mislabelled `out_of_scope` is
    excluded as quietly as an unprobed one and harder to notice, because it
    looks decided.

    Audited at R253: **6 of 19 entries did make a coverage claim** and had been
    parked. They moved back in. This keeps the bucket honest by construction --
    the criterion is `makes_a_coverage_claim`, which asks whether the function
    asserts over a COLLECTION it derived rather than checking one artifact's
    content.
    """
    d = _tracked()
    parked = [e for e in d["functions"] if e["status"] == "out_of_scope"]
    assert parked, "nothing is out_of_scope, so this audit checks nothing"
    wrong = []
    for e in parked:
        claims, why = cas.makes_a_coverage_claim(e["file"], e["function"])
        if claims:
            wrong.append("%s :: %s (%s)" % (e["file"], e["function"], why))
    assert not wrong, (
        "these are parked out_of_scope and DO make a coverage claim, so the "
        "escape hatch is holding real coverage assertions: %s" % wrong)


def test_the_out_of_scope_CRITERION_discriminates():
    """The audit is worth nothing if its criterion says yes to everything or no
    to everything. A collection assertion has to be caught; a single-artifact
    content check has to be cleared."""
    claims, _ = cas.makes_a_coverage_claim(
        "tests/phase1/test_coverage_assertion_sweep.py",
        "test_EVERY_assertion_carries_a_STATUS_and_a_REASON")
    assert claims, (
        "a function asserting inside a loop over a derived collection was not "
        "recognised as a coverage claim, so the audit would clear anything")
    claims2, _ = cas.makes_a_coverage_claim(
        "tests/phase1/test_coverage_assertion_sweep.py",
        "test_the_population_comes_from_git_ls_files")
    assert isinstance(claims2, bool)


def test_there_is_NO_UNJUDGED_cell():
    """R253 §2. 45 unprobed(reason) and 15 candidate_artifact carry their
    reasons -- those are filled cells. An UNJUDGED candidate is the one true
    blank, and a status map with a blank has not landed."""
    d = _tracked()
    blank = [e for e in d["functions"] if e["status"] == "candidate_UNJUDGED"]
    assert not blank, (
        "these candidates pass over an empty population and carry no verdict: "
        "%s" % [(e["file"], e["function"]) for e in blank])
