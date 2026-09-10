"""Every consumer of the decision clock is classified. R239 §1, R240 §1, R241.

**THE CLAIM HAS TWO AXES AND BOTH ARE ABSENCE CLAIMS.** R239 made the consumers a
population; R240 made the scanned files a population; R241 closes both, which is
what ends the recursion rather than spawning another level.

    FILE AXIS   which files are searched.  Floor: `git ls-files` — every tracked
                file. There is no "outside the repository" that can consume this
                clock.
    READ AXIS   which of the reads found are consumers. Floor: every read is
                classified, with its reason. Not "four consumers and six I looked
                at", because six eyeballed dismissals are six chances to wave a
                clock use past.

After both, there is no third axis: a clock use has to be a read of
`decision_column`, in a tracked file, in runnable code.

**THE SUBSTRING RULE, AND ITS ASYMMETRY.** R218 settled *parse, not substring* —
a docstring mentioning a name is not a use. R241 refines it, and the refinement
is what makes the file axis cheap:

    A clock use REQUIRES the substring `decision_column`. So its ABSENCE proves
    no use exists — no parse can find a use of a string that does not occur.
    Its PRESENCE proves nothing.

The two directions are not symmetric. This file uses substring-absence to
exclude a file soundly, and parses every file where the string does occur. That
is a proof, not a shortcut — and it is why a tracked file with a stray backslash
in a docstring is soundly excluded without being parsed at all.

**WHY A TEST AND NOT A CAREFUL LOOK.** R238 found the third consumer, `cli.py`,
reading `built[model.decision_column]` and never calling the shared refusal.
Nothing forced that enumeration; no test failed on it for two rounds while
R236 §3's design was described as covering every entry point. R240's scan then
found a fourth in `tools/`, outside the package. Each catch was diligence, and
TB-11's family of one is precisely the observation that diligence does not
survive the round where somebody is busy.
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

NEEDLE = b"decision_column"
REFUSALS = ("require_decision_column", "require_column_name")

#: Extensions that carry runnable Python. The file axis rests on this list being
#: complete, so a test below proves the tracked tail contains nothing else that
#: runs: no notebook, no shebang, no executable mode bit.
PYTHON_SUFFIXES = (".py", ".pyw", ".pyx", ".pyi", ".ipynb")

#: Line-independent keys — `tools/default_sites.py`'s idiom, so a classification
#: survives an edit above it.  (repo-relative path, enclosing function, source)
OWN_MEANS = {
    ("tools/wholeframe_guard.py", "main", "MODEL.decision_column"): (
        "`MODEL` is a literal built in the same function declaring "
        "`decision_column=\"timestamp\"`, so it cannot carry the unset "
        "sentinel. Pinned by two tests below: one parses that construction and "
        "fails if the keyword is removed, the other checks the declared clock "
        "is the fixture's TRUE clock. NOTE the weaker fact recorded rather than "
        "relied on: `run_probe_a` runs three lines earlier and would refuse "
        "first. That is ordering, and it is not what this rests on."),
}

#: R241 §2. Every read that is NOT routed through the shared refusal carries its
#: own reason here, so the reduction from all reads to the consumers is a
#: classification with a reason at each step rather than a count someone trimmed.
NOT_A_CLOCK_USE = {
    ("src/leakaudit/inference.py", "as_model_dict", "d.decision_column"):
        "`d` is a `Draft`, not an `AvailabilityModel`. The value is compared "
        "against `UNFILLED` to decide whether to scaffold the field in the "
        "drafted file; it is never used to index a frame and never reaches a "
        "probe.",
    ("tests/phase1/test_model_file.py",
     "test_a_well_formed_model_loads", "m.decision_column"):
        "A test asserting the loader kept the declared value. The read is a "
        "`Compare` operand, so it yields a bool.",
    ("tests/phase1/test_model_file.py",
     "test_declaring_it_EXPLICITLY_as_timestamp_is_accepted",
     "m.decision_column"):
        "The paired positive for D-V30A-74: declaring `timestamp` on purpose "
        "is accepted, because what R236 removed is the silent pick and not the "
        "user's freedom to be mistaken. Also a `Compare` operand.",
    ("tests/phase1/test_decision_clock_consumers.py",
     "test_NOT_A_CLOCK_registrations_are_true_of_the_draft_field",
     "Draft().decision_column"):
        "This file's own check that the draft's blank is a different object "
        "from the model's sentinel, which is the reason the `inference.py` "
        "registration above holds.",
}


# ---------------------------------------------------------------------------
# the file axis
# ---------------------------------------------------------------------------
#: THE POPULATION FLAGS, one string so the three floors that use them cannot
#: drift apart. R263 §3(b). `--cached` is the tracked set; `--others
#: --exclude-standard` adds untracked files that are not ignored -- which is
#: what makes a module the current round just wrote part of the population
#: BEFORE it is committed.
LS_FILES = ("ls-files", "--cached", "--others", "--exclude-standard")


def tracked_files():
    """THE OUTER POPULATION: every tracked file PLUS every untracked
    non-ignored one, unfiltered. R241 §1, corrected at R263 §3.

    IT READ `git ls-files` ALONE UNTIL R263, AND THAT MISSED THE ROUND'S OWN
    WORK. R261 wrote `src/leakaudit/label_probe.py`, ran this suite green, and
    committed; R262's first run of the same tests on the same code failed here,
    because the module had become tracked in between. **A green suite over a
    population that excludes the file the round just wrote is a green suite
    about the previous round.** Disclosed at D-V30A-102.
    """
    r = subprocess.run(["git", "-C", str(ROOT)] + list(LS_FILES),
                       capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, (
        "`git ls-files` failed, so the population cannot be established and "
        "this test would silently search nothing: %s" % r.stderr[:200])
    files = [f.strip() for f in r.stdout.splitlines() if f.strip()]
    assert len(files) > 500, (
        "git ls-files returned %d files, too few to be this repository -- the "
        "scope is wrong and every absence claim below would be made over "
        "almost nothing" % len(files))
    return files


def _read_bytes(rel):
    try:
        return (ROOT / rel).read_bytes()
    except OSError:
        return None


def files_containing_the_needle():
    """The sound narrowing. Every other tracked file is excluded by ABSENCE of
    the substring a clock use requires, which is a proof rather than a filter."""
    out, unreadable = [], []
    for rel in tracked_files():
        data = _read_bytes(rel)
        if data is None:
            unreadable.append(rel)
        elif NEEDLE in data:
            out.append(rel)
    return out, unreadable


# ---------------------------------------------------------------------------
# the read axis
# ---------------------------------------------------------------------------
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
    """Reads of `<expr>.decision_column`, parsed, over the narrowed set.

    Returns (sites, unparseable, candidates). `candidates` is every tracked file
    containing the substring — the set that has to be either parsed or shown to
    be non-runnable, so nothing in it is dismissed silently.
    """
    candidates, unreadable = files_containing_the_needle()
    sites, unparseable = [], list(unreadable)
    for rel in candidates:
        if not rel.endswith(".py"):
            continue                     # handled by the non-runnable test
        try:
            tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"))
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
    return sites, unparseable, candidates


def _key(s):
    return (s["file"], s["func"], s["expr"])


def _unclassified(sites):
    """Reads in no class, or in two."""
    out = []
    for s in sites:
        classes = [s["through"], s["compared"], _key(s) in OWN_MEANS]
        if sum(bool(c) for c in classes) != 1:
            out.append((s, classes))
    return out


@pytest.fixture(scope="module")
def scanned():
    """ONE scan, shared. The wrong cases below deliberately do NOT use it: they
    call `scan()` so their monkeypatched scope takes effect and they exercise
    the shipped function rather than a cache."""
    return scan()


# ---------------------------------------------------------------------------
# FILE AXIS -- the floor is proved, not assumed
# ---------------------------------------------------------------------------
def test_NO_TRACKED_FILE_OUTSIDE_py_CARRIES_RUNNABLE_PYTHON():
    """R241 §1. `.py` is a filter, and a filter chosen by habit is an assumption.

    The claim underneath it: no tracked file outside `.py` carries runnable
    Python that could read the clock. A notebook that read it would be a
    consumer a `.py` scan never sees.
    """
    files = tracked_files()
    # THE POPULATION IS ASSERTED NON-EMPTY BEFORE ANYTHING IS CONCLUDED FROM IT.
    # R250 §1(b): the empty-population probe found this assertion passing with
    # `tracked_files()` emptied -- no tail, so no notebook, no shebang and no
    # executable bit, all three vacuously true. The population cannot legitimately
    # be empty (the repository tracks ~956 files), so a silent pass over zero is
    # the round_reconciliation defect in miniature.
    assert len(files) > 500, (
        "the tracked set came back with %d files, so every conclusion below "
        "would be drawn from nothing" % len(files))
    tail = [f for f in files if not f.endswith(".py")]
    assert tail, (
        "no non-.py tracked files at all, which is not this repository -- the "
        "tail is what these three checks range over")

    notebooks = [f for f in tail
                 if f.lower().endswith(PYTHON_SUFFIXES[1:])]
    assert not notebooks, (
        "tracked files carry runnable Python outside .py and are outside the "
        "scan: %s" % notebooks)

    shebangs = []
    for rel in tail:
        data = _read_bytes(rel)
        if data is None:
            continue
        first = data.split(b"\n", 1)[0].decode("utf-8", "replace")
        if first.startswith("#!") and "python" in first.lower():
            shebangs.append(rel)
    assert not shebangs, (
        "tracked non-.py files declare a python interpreter, so they run as "
        "Python and belong in the scan: %s" % shebangs)

    r = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-s"],
                       capture_output=True, text=True, encoding="utf-8")
    execs = [ln.split("\t", 1)[1] for ln in r.stdout.splitlines()
             if ln.startswith("100755") and "\t" in ln
             and not ln.split("\t", 1)[1].endswith(".py")]
    assert not execs, (
        "tracked non-.py files are marked executable, so they may run: %s"
        % execs)


def test_every_file_CONTAINING_the_string_is_parsed_or_proved_non_runnable(
        scanned):
    """The narrowing is sound only if nothing in the candidate set is dropped
    quietly. Every tracked file containing `decision_column` is either parsed as
    Python, or is a non-.py file that the test above proves cannot run."""
    _, _, candidates = scanned
    non_py = [f for f in candidates if not f.endswith(".py")]
    assert all(not f.lower().endswith(PYTHON_SUFFIXES) or f.endswith(".py")
               for f in non_py), non_py
    # they are in the candidate set and are prose; the file-axis test above is
    # what makes "prose" a proof rather than a look.
    assert candidates, "the narrowing excluded everything, so it is not working"


def test_NO_CANDIDATE_FILE_IS_INVISIBLE_TO_THE_SCAN(scanned):
    """A candidate the parser cannot read is one the absence claim cannot cover.

    Scoped to CANDIDATES, and that is the substring refinement paying off: a
    tracked file that does not contain the string is excluded by a proof, so an
    unparseable one out there is irrelevant to this claim rather than a hole.
    """
    _, unparseable, _ = scanned
    assert not unparseable, (
        "these files contain the string and could not be read or parsed, so "
        "the absence claim does not cover them: %s" % unparseable)


# ---------------------------------------------------------------------------
# READ AXIS -- every read, with its reason
# ---------------------------------------------------------------------------
def test_EVERY_read_is_in_exactly_one_class(scanned):
    sites, _, _ = scanned
    assert sites, "the scan found no reads at all, so it is not scanning"
    bad = _unclassified(sites)
    assert not bad, (
        "these reads of `decision_column` are in no class, or in two:\n%s\n"
        "Each either passes through the shared refusal, or is only compared "
        "(so the value becomes a bool and cannot escape as a clock), or is "
        "registered in OWN_MEANS with the test that fails when its means is "
        "removed. A read in none of these is the shape `cli.py` had for two "
        "rounds while the design was described as complete."
        % "\n".join("  %s:%d  %s (in %s) -> through=%s compared=%s "
                    "own_means=%s" % (s["file"], s["line"], s["expr"],
                                      s["func"], *c) for s, c in bad))


def test_EVERY_NON_ROUTED_read_carries_ITS_OWN_REASON(scanned):
    """R241 §2. The reduction from all reads to the consumers is a
    classification with a reason at each step, not a count someone trimmed.

    A structural class says the value cannot escape; it does not say WHAT the
    read is. Both are recorded so the next reader meets the reasons rather than
    re-deriving them — and so an eleventh read cannot be absorbed by a class
    that happens to fit.
    """
    sites, _, _ = scanned
    missing = [(_key(s), s["line"]) for s in sites
               if not s["through"]
               and _key(s) not in OWN_MEANS
               and _key(s) not in NOT_A_CLOCK_USE]
    assert not missing, (
        "these reads are not routed through the refusal and have no recorded "
        "reason. Say what each one IS -- the refusal reading the field, a test "
        "asserting on it, a different class's attribute -- or route it: %s"
        % missing)


def test_the_registrations_NAME_READS_THAT_EXIST(scanned):
    """A registration for a read that is gone is a claim about nothing, and it
    would silently absorb a future read matching its key."""
    sites, _, _ = scanned
    keys = {_key(s) for s in sites}
    stray = (set(OWN_MEANS) | set(NOT_A_CLOCK_USE)) - keys
    assert not stray, "registered and not present: %s" % sorted(stray)


def test_the_PACKAGE_consumers_are_all_routed_through_the_refusal(scanned):
    sites, _, _ = scanned
    pkg = [s for s in sites
           if s["file"].startswith("src/leakaudit/") and not s["compared"]]
    # FOUR SINCE R261, and the fourth was invisible to this scan for a round.
    #
    # `label_probe.py` reads the clock for the same reason the others do: every
    # availability instant it computes is compared against an output row's
    # decision instant. It is routed through the shared refusal, which the
    # second assertion below checks.
    #
    # WHY IT APPEARED A ROUND LATE, and it is not a fix that was forgotten. This
    # scan reads TRACKED files. R261 ran its final suite before `git add`, so
    # the module it had just written was untracked and outside the population --
    # the suite was green over a set that excluded the round's own new file.
    # Committing made it visible and this assertion failed on the next run.
    # Recorded as D-V30A-102: it is R247's shape (evidence at one state, artifact
    # at another) in a scan's population rather than in a figure.
    assert {s["file"] for s in pkg} == {
        "src/leakaudit/availability.py", "src/leakaudit/cli.py",
        "src/leakaudit/identity_control.py",
        "src/leakaudit/label_probe.py"}, sorted({s["file"] for s in pkg})
    assert all(s["through"] for s in pkg), (
        "a package consumer bypasses the shared refusal: %s"
        % [(s["file"], s["line"]) for s in pkg if not s["through"]])


#: Every `git ls-files` floor in this repository, and what each one is. R263
#: §3(b). ENUMERATED, because "every floor was corrected" is an absence claim
#: and an absence claim needs its population written down. Found with
#: `grep -rn "ls-files" --include=*.py tests/ tools/`.
LS_FILES_FLOORS = {
    "tests/phase1/test_decision_clock_consumers.py":
        "this file's own `tracked_files()` -- the clock-consumer scan",
    "tools/coverage_assertion_sweep.py":
        "`tracked_python_files()` -- the sweep's `.py` floor",
    "tools/portability_digest.py":
        "the portability inputs' presence check",
}

#: The one floor NOT corrected, named with its reason rather than left out of
#: the population. `tools/check_registration.py` is the frozen checker: its
#: verdicts are pinned against the tagged instrument and differences are ruled
#: against a ceiling of four, currently at two. Correcting its D16 floor is a
#: change to a frozen file and costs a ruled-difference slot, which R263 did not
#: authorise. Recorded so the exemption is a decision somebody can see.
LS_FILES_FROZEN = {
    "tools/check_registration.py":
        "D16's tracked set; frozen instrument, correcting it spends a ruled "
        "difference and was not authorised",
}


def test_EVERY_ls_files_FLOOR_sees_untracked_non_ignored_files():
    """R263 §3(b). A floor that reads only the index cannot see the module the
    round just wrote, so a run before the commit measures the previous round.

    THE POPULATION IS ENUMERATED ABOVE AND CHECKED AGAINST THE TREE HERE, so a
    new floor added later fails this rather than joining silently.
    """
    import re

    found = {}
    for rel in tracked_files():
        if not rel.endswith(".py") or not (rel.startswith("tests/")
                                           or rel.startswith("tools/")):
            continue
        text = _read_bytes(rel).decode("utf-8", "replace")
        # A CALL, not a mention: `empty_population_probe` names the string to
        # DETECT this pattern in other files and has no floor of its own.
        if re.search(r'"ls-files"', text) or re.search(r"'ls-files'", text):
            found[rel] = text

    known = set(LS_FILES_FLOORS) | set(LS_FILES_FROZEN)
    unknown = sorted(set(found) - known - {"tools/empty_population_probe.py"})
    assert not unknown, (
        "a `git ls-files` floor exists that this population does not name, so "
        "'every floor was corrected' would be an absence claim over a set "
        "somebody chose: %s" % unknown)

    for rel in LS_FILES_FLOORS:
        assert rel in found, (
            "%s no longer calls `git ls-files`; the enumeration above is stale "
            "and this test is asserting over a file that moved on" % rel)
        text = found[rel]
        assert "--others" in text and "--exclude-standard" in text, (
            "%s reads the index alone, so a module written this round is "
            "outside its population until it is committed. That is D-V30A-102: "
            "R261's suite was green over a set excluding its own new file." % rel)

    for rel in LS_FILES_FROZEN:
        assert rel in found, "%s no longer calls `git ls-files`" % rel


def test_the_FROZEN_protocol_file_is_clock_free_BY_SUBSTRING_ABSENCE():
    """R241 §3's sound direction, on the sharp case.

    `protocol/runtime_reference.py` is frozen: a consumer there could not be
    routed through the shared refusal without editing a frozen file. The string
    a clock use requires does not occur in it, so no use can exist — and that
    proof is complete on its own. Freezing is irrelevant to a file that never
    read the clock.
    """
    rel = "protocol/runtime_reference.py"
    assert rel in tracked_files(), (
        "%s is not tracked, so its clock-freedom would be an assumption" % rel)
    assert NEEDLE not in _read_bytes(rel), (
        "the frozen runtime reference now contains `decision_column`. If it "
        "READS the clock it cannot be routed without editing a frozen file, so "
        "it needs an OWN_MEANS registration with a pinning test, not an edit.")


def test_NOT_A_CLOCK_registrations_are_true_of_the_draft_field():
    from leakaudit.availability import NOT_SET
    from leakaudit.inference import UNFILLED, Draft
    assert Draft().decision_column is UNFILLED
    assert UNFILLED is not NOT_SET, (
        "the draft's blank and the model's sentinel became the same object, so "
        "the inference.py registration's reason no longer holds")


# ---------------------------------------------------------------------------
# OWN_MEANS carries its pinning tests. R239 §1(b), R240 §2
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
    """R240 §2. **DECLARED IS NOT CORRECT.** The guard runs the same model on
    both sides and compares them, so a wrong clock is wrong identically,
    returns SAME, and hides in the one instrument nothing else checks."""
    declared = _guard_model_keywords()["decision_column"].value
    fixture = (ROOT / "evidence" / "fixture_spike" / "f2"
               / "phase5_ml_fixture.py").read_text(encoding="utf-8")
    derivation = 'snap["ts_floor"] = snap["timestamp"].dt.floor("1s")'
    assert derivation in fixture, (
        "the fixture no longer derives ts_floor from timestamp, so the reason "
        "`timestamp` is the true decision instant no longer holds")
    assert declared == "timestamp", (
        "the guard declares %r while the fixture's primary per-row instant is "
        "`timestamp`" % declared)


# ---------------------------------------------------------------------------
# the wrong cases
# ---------------------------------------------------------------------------
def _scan_text(src, monkeypatch, tmp_path, name="a_consumer.py"):
    (tmp_path / name).write_text(src, encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "tracked_files",
                        lambda: [name])
    return scan()[0]


def test_A_NEW_UNCLASSIFIED_CONSUMER_FAILS_THE_TOTALITY(tmp_path, monkeypatch):
    """**The point of the file, and it is worth nothing unless this fails.**"""
    sites = _scan_text("def audit(model, built):\n"
                       "    return built[model.decision_column]\n",
                       monkeypatch, tmp_path)
    assert len(sites) == 1
    assert len(_unclassified(sites)) == 1, (
        "a consumer that reads the clock and does none of the three was NOT "
        "reported, so the totality cannot catch what it exists to catch")


def test_THE_INDIRECT_SHAPE_ALSO_FAILS(tmp_path, monkeypatch):
    """`dcol = model.decision_column` then a use. Binding to a local is how a
    consumer stops looking like one, so it is deliberately unclassifiable."""
    sites = _scan_text("def audit(model, built):\n"
                       "    dcol = model.decision_column\n"
                       "    return built[dcol]\n", monkeypatch, tmp_path)
    assert len(_unclassified(sites)) == 1


def test_a_ROUTED_consumer_is_accepted(tmp_path, monkeypatch):
    """Negative control: a totality failing on everything would pass the wrong
    cases above and be useless."""
    sites = _scan_text(
        "def audit(model, built):\n"
        "    dcol = require_decision_column(model.decision_column, 'here')\n"
        "    return built[dcol]\n", monkeypatch, tmp_path)
    assert len(sites) == 1 and sites[0]["through"] is True
    assert _unclassified(sites) == []


def test_a_COMPARED_read_is_accepted(tmp_path, monkeypatch):
    sites = _scan_text("def check(model):\n"
                       "    return model.decision_column == 'timestamp'\n",
                       monkeypatch, tmp_path)
    assert len(sites) == 1 and sites[0]["compared"] is True
    assert _unclassified(sites) == []


def test_a_file_WITHOUT_the_string_is_excluded_and_never_parsed(
        tmp_path, monkeypatch):
    """R241 §3's refinement, as a behaviour. A file with no occurrence of the
    substring is excluded by proof — so a syntax error in it is irrelevant to
    this claim rather than a hole in it."""
    (tmp_path / "broken.py").write_text(
        "this is not python at all (((\n", encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "tracked_files",
                        lambda: ["broken.py"])
    sites, unparseable, candidates = scan()
    assert sites == [] and unparseable == [] and candidates == [], (
        "a file with no occurrence of the substring was parsed anyway, so the "
        "sound narrowing is not being used and an unrelated syntax error "
        "would read as a coverage hole")


def test_the_scan_scope_is_the_TRACKED_SET_not_a_directory_list():
    files = tracked_files()
    tops = {f.split("/")[0] for f in files}
    for expected in ("src", "tools", "tests", "protocol", "evidence"):
        assert expected in tops, (
            "%s/ is absent from the population, so a clock consumer there "
            "would be invisible while this file reported full coverage"
            % expected)
