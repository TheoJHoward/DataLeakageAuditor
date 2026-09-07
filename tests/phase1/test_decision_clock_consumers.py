"""Every consumer of the decision clock is classified. R239 §1, R240 §1.

**WHY THIS IS A TEST AND NOT A CAREFUL LOOK.** R238 found a third consumer —
`cli.py` read `built[model.decision_column]` directly, never calling the shared
refusal. **Nothing forced that enumeration.** No test failed on it for two rounds
while R236 §3's design was described as covering every entry point, because that
design rested on a two-consumer count nobody had established. The catch was
diligence, and TB-11's family of one is exactly the observation that diligence
does not survive the round where somebody is busy.

**THE SCAN SCOPE IS THE ABSENCE CLAIM'S POPULATION, so it is declared and its
floor is definite.** R240 §1: this test asserts *these are all the consumers*,
which is an absence claim, and a consumer in a directory the test does not search
is invisible while the test stays green — the same failure one level up.

    THE POPULATION IS `git ls-files -- "*.py"`: every tracked Python file in the
    repository.

Not "the package". Not "the directories I found consumers in". **The fourth
consumer is why**: it was `tools/wholeframe_guard.py`, outside `src/`, and a scan
scoped to the package would have passed while missing the instrument that gates
every round. `git ls-files` terminates the regress — there is no "outside the
repository" that can consume this clock.

**CLASSIFICATION IS STRUCTURAL WHEREVER IT CAN BE**, so it does not rest on my
judgment about each site:

    THROUGH_REFUSAL   the read IS the argument to `require_decision_column` /
                      `require_column_name` — refused before use
    COMPARED_ONLY     the read's parent node is a `Compare`. The value becomes a
                      bool and cannot escape as a clock; this is a property of
                      the syntax, not an opinion about the caller
    OWN_MEANS         an independent means, REGISTERED below with the test that
                      fails when that means is removed (R239 §1(b))

A read in none of them **fails, naming the site** — including `dcol =
model.decision_column` followed by a use, which is deliberately not classifiable
and is exactly how a fifth consumer would arrive.

**`protocol/` IS COVERED BY THE SCOPE, and was checked rather than assumed.**
`protocol/runtime_reference.py` is frozen, so a consumer there could not be
routed through the refusal without editing a frozen file. Measured: the string
`decision_column` does not appear in it at all. It is in the scan population
regardless, so if that ever changes this test says so instead of a later round
discovering it.
"""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

REFUSALS = ("require_decision_column", "require_column_name")

#: A LINE-INDEPENDENT KEY, so a classification survives an edit above it —
#: `tools/default_sites.py`'s idiom, for the same reason.
#: (repo-relative path, enclosing function, expression source)
OWN_MEANS = {
    ("tools/wholeframe_guard.py", "main", "MODEL.decision_column"): (
        "`MODEL` is a literal built in the same function, declaring "
        "`decision_column=\"timestamp\"`, so it cannot carry the unset "
        "sentinel. Pinned by the two tests below: one parses that construction "
        "and fails if the keyword is removed, the other checks the declared "
        "clock is the fixture's TRUE clock rather than merely a declared one. "
        "NOTE the weaker second fact, recorded rather than relied on: "
        "`run_probe_a` runs three lines earlier and would refuse first. That "
        "is ordering, and it is not what this registration rests on."),
}


def tracked_python_files():
    """THE DECLARED SCAN SCOPE. R240 §1(a)."""
    r = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--", "*.py"],
                       capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, (
        "`git ls-files` failed, so the scan population cannot be established "
        "and this test would silently search nothing: %s" % r.stderr[:200])
    files = [f.strip() for f in r.stdout.splitlines() if f.strip()]
    assert len(files) > 100, (
        "git ls-files returned %d python files, which is too few to be this "
        "repository -- the scope is wrong and the absence claim would be made "
        "over almost nothing" % len(files))
    return files


def _parents(tree):
    out = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            out[id(child)] = parent
    return out


def _enclosing(tree, node):
    best = None
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if n.lineno <= node.lineno <= (n.end_lineno or n.lineno):
                if best is None or n.lineno > best.lineno:
                    best = n
    return best.name if best else "<module>"


def scan():
    """Every `<expr>.decision_column` read across the declared scope.

    Returns (sites, unparseable). BY PARSE, NOT SUBSTRING (R218): a comment, a
    docstring or a test name containing "decision_column" is not a read, and the
    round that matched its own banned-token list and then the prose explaining
    it settled that the fix is the parser rather than the prose.
    """
    sites, unparseable = [], []
    for rel in tracked_python_files():
        p = ROOT / rel
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="strict"))
        except (SyntaxError, UnicodeDecodeError, OSError) as e:
            unparseable.append((rel, type(e).__name__))
            continue
        parents = _parents(tree)
        guarded = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                    and n.func.id in REFUSALS and n.args:
                guarded.add(id(n.args[0]))
        for n in ast.walk(tree):
            if isinstance(n, ast.Attribute) and n.attr == "decision_column" \
                    and isinstance(n.ctx, ast.Load):
                sites.append({
                    "file": rel.replace("\\", "/"),
                    "line": n.lineno,
                    "func": _enclosing(tree, n),
                    "expr": ast.unparse(n),
                    "through": id(n) in guarded,
                    "compared": isinstance(parents.get(id(n)), ast.Compare),
                })
    return sites, unparseable


def _key(s):
    return (s["file"], s["func"], s["expr"])


def _unclassified(sites):
    """Sites in no class, or in two. The one piece of logic the real test and
    its wrong cases below all run, so a wrong case cannot pass against a
    different implementation than the one that ships."""
    out = []
    for s in sites:
        classes = [s["through"], s["compared"], _key(s) in OWN_MEANS]
        if sum(bool(c) for c in classes) != 1:
            out.append((s, classes))
    return out


@pytest.fixture(scope="module")
def scanned():
    """ONE scan, shared. Each call parses every tracked file, so calling it per
    test parsed the repository four times and repeated any warning a tracked
    file emits four times over. The wrong cases below deliberately do NOT use
    this: they call `scan()` directly so their monkeypatched scope takes
    effect, and so they exercise the shipped function rather than a cache."""
    return scan()


# ---------------------------------------------------------------------------
# the totality
# ---------------------------------------------------------------------------
def test_EVERY_read_of_the_clock_IN_EVERY_TRACKED_FILE_is_in_one_class(scanned):
    sites, unparseable = scanned
    assert sites, "the scan found no reads at all, so it is not scanning"

    bad = _unclassified(sites)
    assert not bad, (
        "these reads of `decision_column` are in no class, or in two:\n%s\n"
        "Each one either passes through the shared refusal, or is only "
        "compared (so the value cannot escape as a clock), or is registered in "
        "OWN_MEANS with the test that fails when its means is removed. A read "
        "in none of these is the exact shape `cli.py` had for two rounds while "
        "the design was described as covering every entry point."
        % "\n".join("  %s:%d  %s (in %s) -> through=%s compared=%s "
                    "own_means=%s" % (s["file"], s["line"], s["expr"],
                                      s["func"], *c) for s, c in bad))


def test_NO_TRACKED_FILE_IS_INVISIBLE_TO_THE_SCAN(scanned):
    """A file the parser cannot read is a file this test cannot clear, and
    skipping it silently would put a hole inside the mechanism built to remove
    holes."""
    _, unparseable = scanned
    assert not unparseable, (
        "these tracked files could not be parsed, so the absence claim does "
        "not cover them: %s" % unparseable)


def test_the_registrations_NAME_SITES_THAT_EXIST(scanned):
    """A registration for a site that is gone is a claim about nothing, and it
    would silently absorb a future site that matched its key."""
    sites, _ = scanned
    stray = set(OWN_MEANS) - {_key(s) for s in sites}
    assert not stray, "registered and not present in the scan: %s" % sorted(stray)


def test_the_PACKAGE_consumers_are_all_routed_through_the_refusal(scanned):
    sites, _ = scanned
    pkg = [s for s in sites
           if s["file"].startswith("src/leakaudit/") and not s["compared"]]
    assert {s["file"] for s in pkg} == {
        "src/leakaudit/availability.py", "src/leakaudit/cli.py",
        "src/leakaudit/identity_control.py"}, sorted({s["file"] for s in pkg})
    assert all(s["through"] for s in pkg), (
        "a package consumer bypasses the shared refusal: %s"
        % [(s["file"], s["line"]) for s in pkg if not s["through"]])


def test_the_FROZEN_protocol_file_was_CHECKED_not_assumed_clock_free():
    """R240 §1(c). A consumer here could not be routed without editing a frozen
    file, so its absence is worth asserting rather than assuming."""
    rel = "protocol/runtime_reference.py"
    assert rel in tracked_python_files(), (
        "%s is not in the scan population, so 'protocol/ is clock-free' would "
        "be an assumption rather than a measurement" % rel)
    body = (ROOT / rel).read_text(encoding="utf-8")
    assert "decision_column" not in body, (
        "the frozen runtime reference now mentions the decision clock. If it "
        "READS it, it is an independent-means consumer that cannot be routed "
        "through the refusal without editing a frozen file, and it needs an "
        "OWN_MEANS registration with a pinning test rather than an edit.")


# ---------------------------------------------------------------------------
# OWN_MEANS carries its pinning tests, per R239 §1(b) and R240 §2
# ---------------------------------------------------------------------------
def _guard_model_keywords():
    tree = ast.parse((ROOT / "tools" / "wholeframe_guard.py")
                     .read_text(encoding="utf-8"))
    built = [n for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "AvailabilityModel"]
    assert len(built) == 1, (
        "the guard builds %d availability models; OWN_MEANS speaks about one"
        % len(built))
    return {k.arg: k.value for k in built[0].keywords if k.arg}


def test_the_guards_own_means_is_that_its_model_DECLARES_the_clock():
    """R239 §1(b): an independent means counts only if a test fails when it is
    removed. Delete `decision_column=` from that literal and this fails."""
    kw = _guard_model_keywords()
    assert "decision_column" in kw, (
        "the guard's MODEL no longer declares `decision_column`, so its "
        "registered means is gone and its read is covered only by "
        "`run_probe_a` running first -- ordering, which OWN_MEANS explicitly "
        "does not rest on")
    assert isinstance(kw["decision_column"], ast.Constant), (
        "the guard's clock is no longer a literal, so 'it cannot carry the "
        "sentinel' is no longer readable from the source")


def test_the_guards_DECLARED_clock_is_its_fixtures_TRUE_clock():
    """R240 §2. **DECLARED IS NOT CORRECT.**

    The guard runs the same model on both sides and compares them, so a clock
    that is wrong would be wrong identically in baseline and current, come back
    SAME, and hide itself in the one instrument nothing else checks. Being
    declared rather than defaulted makes it legitimate under R239 §1(b); it does
    not make it right.

    Confirmed from the FIXTURE'S OWN CONSTRUCTION rather than from the
    declaration: the fixture derives `ts_floor` FROM `timestamp`, so
    `timestamp` is the primary per-row instant and `ts_floor` is its
    second-boundary alignment for the aggregate join — not a rival clock.
    """
    declared = _guard_model_keywords()["decision_column"].value
    fixture = (ROOT / "evidence" / "fixture_spike" / "f2"
               / "phase5_ml_fixture.py").read_text(encoding="utf-8")
    derivation = 'snap["ts_floor"] = snap["timestamp"].dt.floor("1s")'
    assert derivation in fixture, (
        "the fixture no longer derives ts_floor from timestamp, so the reason "
        "`timestamp` is the true decision instant no longer holds and the "
        "guard's clock needs re-establishing from the new construction")
    assert declared == "timestamp", (
        "the guard declares %r as its clock while the fixture's primary "
        "per-row instant is `timestamp`" % declared)


# ---------------------------------------------------------------------------
# the wrong cases -- does the totality actually catch a fifth consumer?
# ---------------------------------------------------------------------------
def _scan_text(src, monkeypatch, tmp_path):
    """Run the SHIPPED scan over one synthetic file."""
    mod = tmp_path / "a_consumer.py"
    mod.write_text(src, encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "tracked_python_files",
                        lambda: ["a_consumer.py"])
    return scan()[0]


def test_A_NEW_UNCLASSIFIED_CONSUMER_FAILS_THE_TOTALITY(tmp_path, monkeypatch):
    """**THE POINT OF THE FILE, and it is worth nothing unless this fails.**
    A totality test that passes over a population it cannot see, or classifies
    everything by accident, reads exactly like a working one."""
    sites = _scan_text("def audit(model, built):\n"
                       "    return built[model.decision_column]\n",
                       monkeypatch, tmp_path)
    assert len(sites) == 1
    assert len(_unclassified(sites)) == 1, (
        "a consumer that reads the clock and does none of the three was NOT "
        "reported, so the totality cannot catch what it exists to catch")


def test_THE_INDIRECT_SHAPE_ALSO_FAILS(tmp_path, monkeypatch):
    """`dcol = model.decision_column` then a use. Deliberately unclassifiable:
    binding to a local is how a consumer avoids looking like one."""
    sites = _scan_text("def audit(model, built):\n"
                       "    dcol = model.decision_column\n"
                       "    return built[dcol]\n", monkeypatch, tmp_path)
    assert len(_unclassified(sites)) == 1


def test_a_ROUTED_consumer_is_accepted(tmp_path, monkeypatch):
    """Negative control. A totality that failed on everything would pass the
    wrong cases above and be useless."""
    sites = _scan_text(
        "def audit(model, built):\n"
        "    dcol = require_decision_column(model.decision_column, 'here')\n"
        "    return built[dcol]\n", monkeypatch, tmp_path)
    assert len(sites) == 1 and sites[0]["through"] is True
    assert _unclassified(sites) == []


def test_a_COMPARED_read_is_accepted(tmp_path, monkeypatch):
    """The other negative control: the structural class has to actually fire."""
    sites = _scan_text("def check(model):\n"
                       "    return model.decision_column == 'timestamp'\n",
                       monkeypatch, tmp_path)
    assert len(sites) == 1 and sites[0]["compared"] is True
    assert _unclassified(sites) == []


def test_the_scan_scope_is_the_TRACKED_SET_not_a_directory_list():
    """R240 §1(a)'s floor, asserted. A scope narrowed back to `src/` would pass
    every other test in this file and miss the guard."""
    files = tracked_python_files()
    tops = {f.split("/")[0] for f in files}
    for expected in ("src", "tools", "tests", "protocol", "evidence"):
        assert expected in tops, (
            "%s/ is absent from the scan population, so a clock consumer there "
            "would be invisible while this file reported full coverage"
            % expected)
