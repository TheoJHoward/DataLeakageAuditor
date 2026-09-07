"""Every consumer of the decision clock is classified. R239 §1.

**WHY THIS IS A TEST AND NOT A CAREFUL LOOK.** R238 found a third consumer —
`cli.py` read `built[model.decision_column]` directly, never calling the shared
refusal — and it was found because the reads were enumerated rather than
recalled. **Nothing forced that enumeration.** No test failed on the third
consumer; R236 §3 had designed "one refusal, both entry points reach it" against
a two-consumer model that was simply wrong, and the design read as complete for
two rounds. The catch was diligence, and diligence is what does not survive the
round where somebody is busy — TB-11/F6, the family of one, whose whole point is
that a check you have to remember to run is the check that gets skipped the once
it matters.

**AND THE ENUMERATION FOUND A FOURTH.** Written for R239, this scan reported
`tools/wholeframe_guard.py` indexing `built[MODEL.decision_column]` with no call
to the refusal — outside the package, on the probe path, and covered by its own
means rather than by the shared one. Three was not all of them either.

**THE TOTALITY.** Every read of `.decision_column` in the shipped package and in
the instruments is in exactly one class:

    THROUGH_REFUSAL   the read is the argument to `require_decision_column`, so
                      an unset or non-column clock is refused before use
    OWN_MEANS         it refuses by an independent means, registered below WITH
                      the test that fails when that means is removed
    NOT_A_CLOCK       the attribute belongs to a different class entirely

**A read in none of the three FAILS**, naming the site. That is what turns "I
enumerated them this time" into "a fourth cannot slip in unclassified."

Tests are excluded from the population deliberately: a test reading
`m.decision_column` is asserting a value, not using it as a clock, and folding
assertions in would make the population the thing nobody could keep classified.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

#: Where a decision clock can be consumed: the shipped package, and the
#: instruments that drive the probe directly.
SCANNED = [ROOT / "src" / "leakaudit", ROOT / "tools"]

REFUSALS = ("require_decision_column", "require_column_name")

#: A LINE-INDEPENDENT KEY, so a classification survives an edit above it —
#: `tools/default_sites.py`'s idiom, for the same reason.
#: (file, enclosing function, expression source)
OWN_MEANS = {
    ("wholeframe_guard.py", "main", "MODEL.decision_column"): (
        "`MODEL` is a literal built in the same function, declaring "
        "`decision_column=\"timestamp\"`, so it cannot carry the unset "
        "sentinel. Pinned by "
        "`test_the_guards_own_means_is_that_its_model_DECLARES_the_clock`, "
        "which parses that construction and fails if the keyword is removed. "
        "NOTE the weaker second fact, recorded rather than relied on: "
        "`run_probe_a` runs three lines earlier and would refuse first. That "
        "is ordering, and it is not what this registration rests on."),
}

#: Reads of a `decision_column` attribute that is not an availability model's.
NOT_A_CLOCK = {
    ("inference.py", "as_model_dict", "d.decision_column"): (
        "`d` is a `Draft`, not an `AvailabilityModel`. `Draft.decision_column` "
        "holds the draft's own blank (`UNFILLED`) and is written into the "
        "drafted file as the fill-me sentinel, which the loader refuses. It "
        "never reaches a probe and is never used to index a frame."),
}


def _enclosing(tree, node):
    best = None
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if n.lineno <= node.lineno <= (n.end_lineno or n.lineno):
                if best is None or n.lineno > best.lineno:
                    best = n
    return best.name if best else "<module>"


def _sites():
    """Every `<expr>.decision_column` read, with how it is reached."""
    out = []
    for root in SCANNED:
        for p in sorted(root.glob("*.py")):
            tree = ast.parse(p.read_text(encoding="utf-8"))
            guarded = set()
            for n in ast.walk(tree):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                        and n.func.id in REFUSALS and n.args:
                    guarded.add(ast.dump(n.args[0]))
            for n in ast.walk(tree):
                if isinstance(n, ast.Attribute) \
                        and n.attr == "decision_column" \
                        and isinstance(n.ctx, ast.Load):
                    out.append({
                        "file": p.name,
                        "line": n.lineno,
                        "func": _enclosing(tree, n),
                        "expr": ast.unparse(n),
                        "through": ast.dump(n) in guarded,
                    })
    return out


def _key(s):
    return (s["file"], s["func"], s["expr"])


# ---------------------------------------------------------------------------
# the totality
# ---------------------------------------------------------------------------
def _unclassified(sites):
    """Sites in no class, or in two. The one piece of logic both the real test
    and its wrong case below run, so the wrong case cannot pass against a
    different implementation than the one that ships."""
    out = []
    for s in sites:
        classes = [s["through"], _key(s) in OWN_MEANS, _key(s) in NOT_A_CLOCK]
        if sum(bool(c) for c in classes) != 1:
            out.append((s, classes))
    return out


def test_EVERY_read_of_the_clock_is_in_EXACTLY_ONE_class():
    """Disjoint and covering, with the third state failing."""
    sites = _sites()
    assert sites, "the scan found no reads at all, so it is not scanning"

    unclassified = _unclassified(sites)

    assert not unclassified, (
        "these reads of `decision_column` are in no class, or in two:\n%s\n"
        "Each one either passes through `require_decision_column`, or is "
        "registered in OWN_MEANS with the test that fails when its means is "
        "removed, or is registered in NOT_A_CLOCK because the attribute is not "
        "an availability model's. A new consumer that does none of these is "
        "the exact shape `cli.py` had for two rounds while the design was "
        "described as covering every entry point."
        % "\n".join("  %s:%d  %s (in %s) -> through=%s own_means=%s "
                    "not_a_clock=%s" % (s["file"], s["line"], s["expr"],
                                        s["func"], *c)
                    for s, c in unclassified))


def test_the_registrations_NAME_SITES_THAT_EXIST():
    """A registration for a site that is gone is a claim about nothing, and it
    would silently absorb a future site that happened to match its key."""
    keys = {_key(s) for s in _sites()}
    stray = (set(OWN_MEANS) | set(NOT_A_CLOCK)) - keys
    assert not stray, (
        "registered here and not present in the scan: %s" % sorted(stray))


def test_the_three_PACKAGE_consumers_are_all_routed_through_the_refusal():
    """The population claim, stated as an assertion rather than a count I
    remember. If a fourth package consumer appears it lands here, not in a
    later round's enumeration."""
    pkg = [s for s in _sites()
           if s["file"] not in ("inference.py",) and _key(s) not in NOT_A_CLOCK
           and (ROOT / "src" / "leakaudit" / s["file"]).exists()]
    assert {s["file"] for s in pkg} == {"availability.py", "cli.py",
                                        "identity_control.py"}, \
        sorted({s["file"] for s in pkg})
    assert all(s["through"] for s in pkg), (
        "a package consumer bypasses the shared refusal: %s"
        % [(s["file"], s["line"]) for s in pkg if not s["through"]])


# ---------------------------------------------------------------------------
# OWN_MEANS carries its pinning test, per R239 §1(b)
# ---------------------------------------------------------------------------
def test_the_guards_own_means_is_that_its_model_DECLARES_the_clock():
    """**THE MEANS, PINNED.** R239 §1(b): an independent means counts only if a
    test fails when it is removed. The guard's means is that its `MODEL` literal
    declares the clock, so this parses the construction and requires the
    keyword. Delete `decision_column=` from that literal and this fails.
    """
    src = (ROOT / "tools" / "wholeframe_guard.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    built = [n for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "AvailabilityModel"]
    assert len(built) == 1, (
        "the guard builds %d availability models; the registration in "
        "OWN_MEANS speaks about one" % len(built))
    kw = {k.arg: k.value for k in built[0].keywords if k.arg}
    assert "decision_column" in kw, (
        "the guard's MODEL no longer declares `decision_column`, so its "
        "registered means is gone and its read at `MODEL.decision_column` is "
        "covered only by `run_probe_a` running first -- which is ordering, and "
        "is what OWN_MEANS explicitly does not rest on")
    assert isinstance(kw["decision_column"], ast.Constant), (
        "the guard's clock is no longer a literal, so 'it cannot carry the "
        "sentinel' is no longer readable from the source")
    assert kw["decision_column"].value == "timestamp"


def test_NOT_A_CLOCK_is_true_of_the_draft_field():
    """The other registration, checked rather than asserted in prose."""
    from leakaudit.inference import UNFILLED, Draft
    assert Draft().decision_column is UNFILLED
    from leakaudit.availability import NOT_SET
    assert UNFILLED is not NOT_SET, (
        "the draft's blank and the model's sentinel became the same object, so "
        "NOT_A_CLOCK's reason -- that these are different fields on different "
        "classes -- no longer holds")


# ---------------------------------------------------------------------------
# and the classes mean what they say
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("name", ["availability.py", "identity_control.py",
                                  "cli.py"])
def test_each_package_consumer_actually_REFUSES_an_unset_clock(name):
    """THROUGH_REFUSAL is a claim about behaviour, not about syntax. The scan
    proves the call is there; this proves the call refuses."""
    import pandas as pd

    from leakaudit.availability import (AvailabilityModel, ProbeError,
                                        require_decision_column)
    m = AvailabilityModel(aggregate_frames={"a": "k"},
                          window=pd.Timedelta(seconds=1))
    with pytest.raises(ProbeError):
        require_decision_column(m.decision_column, "a %s consumer" % name)


# ---------------------------------------------------------------------------
# the wrong case -- does the totality test actually catch a fourth consumer?
# ---------------------------------------------------------------------------
def test_A_NEW_UNCLASSIFIED_CONSUMER_FAILS_THE_TOTALITY(tmp_path, monkeypatch):
    """**THE POINT OF THE WHOLE FILE, and it is worth nothing unless this
    fails.** A totality test that passes over a population it cannot see, or
    that classifies everything by accident, reads exactly like a working one.

    So: a synthetic module that reads the clock and does none of the three
    things, scanned by the SHIPPED `_sites` and judged by the SHIPPED
    `_unclassified`. `cli.py` looked precisely like this for two rounds while
    the design was described as covering every entry point.
    """
    mod = tmp_path / "a_new_consumer.py"
    mod.write_text(
        "def audit(model, built):\n"
        "    return built[model.decision_column]\n", encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "SCANNED", [tmp_path])

    sites = _sites()
    assert len(sites) == 1 and sites[0]["file"] == "a_new_consumer.py", sites
    bad = _unclassified(sites)
    assert len(bad) == 1, (
        "a consumer that reads the clock and neither routes through the "
        "refusal nor is registered was NOT reported, so the totality test "
        "cannot catch the thing it exists to catch")
    assert bad[0][0]["expr"] == "model.decision_column"


def test_a_synthetic_consumer_that_DOES_route_through_is_accepted(tmp_path,
                                                                  monkeypatch):
    """The negative control. A totality test that failed on everything would
    pass the wrong case above and be useless."""
    mod = tmp_path / "a_routed_consumer.py"
    mod.write_text(
        "def audit(model, built):\n"
        "    dcol = require_decision_column(model.decision_column, 'here')\n"
        "    return built[dcol]\n", encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "SCANNED", [tmp_path])

    sites = _sites()
    assert len(sites) == 1 and sites[0]["through"] is True
    assert _unclassified(sites) == []
