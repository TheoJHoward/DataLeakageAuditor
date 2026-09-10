#!/usr/bin/env python3
"""The population of coverage assertions, and which have been shown able to fail.

    $ py -3.12 tools/coverage_assertion_sweep.py

Exit 0 always: this REPORTS a population and its completion state. It is not a
gate, and saying so matters -- a sweep instrument that failed the build would be
pressure to mark entries done.

**WHY THIS EXISTS.** Four can't-fail checks were found in one session, each by a
different accident: a `bare=True` negative control, two caught by a mutation
check, a count assertion satisfied by an entry's own label, and an instrument
zeroed by its invocation. The practice that followed -- *every count, coverage or
totality assertion is shown to go RED on a violation before its green is
believed* -- was recorded and applied to one file. **The population of enforcing
tests was itself unswept**, which is an absence claim about the tests that make
absence claims.

**THE POPULATION, AND WHY IT IS DEFINED BY WHAT IT READS.** A first attempt keyed
on the SHAPE of the assert -- `len(...)`, a set difference, a `set(...)` compare.
That excluded the commonest form in this repository:

    assert not unclassified, "..."

whose collection is built on an earlier line. Keying on shape dropped
`test_decision_clock_consumers`, `test_lessons_classification`,
`test_manifest_hashes` and `test_config_key_complement` -- the four files whose
coverage claims matter most, and three of the four defects. **The enumerator
excluded the cases that matter, which is the session's own recurring failure
appearing inside the sweep for it.**

Inverted: an assertion is coincidence-susceptible when **its population is read
from the repository** -- a file list, a registry, a tracked set. Change the code
under test and a unit assertion's output changes with it; a repository assertion
can be satisfied by something unrelated that happens to sit in the tree. Every
one of the four defects had that property, so it is the axis.

**WHAT "ESTABLISHED" MEANS HERE.** An entry is established when a test in the
repository mutates the artifact and requires the assertion to go red. Not "it
looks fine", not "it passed" -- a green assertion is not evidence until it has
been shown able to go red.

**WHAT THIS DOES NOT DO.** It does not mutate anything itself. A generic mutation
over the whole population would have to know what each one's artifact is, and guessing
that is how a sweep reports coverage it does not have. The instrument enumerates
and tracks; the mutations are written by hand, per assertion, and registered
below.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

import ast
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]

#: A function whose body contains one of these reads its population from the
#: repository rather than from code under test.
REPO_READ = ("ls-files", "ls_files", "rglob", ".glob(", "iterdir", "listdir",
             "read_text", "read_bytes", "os.walk", "subprocess.run")

#: Module-level helpers in this repository that perform such a read.
REPO_HELPERS = ("_text()", "scan()", "entries()", "tracked_files()", "verify(",
                "_entries(", "_families(", "tracked_python_files()")

#: ESTABLISHED: (file, enclosing function) -> the test that mutates the artifact
#: and requires the assertion to go red. Keyed line-independently, so a
#: registration survives an edit above it -- `tools/default_sites.py`'s idiom.
ESTABLISHED = {
    ("tests/phase1/test_lessons_classification.py",
     "check_the_section_states_the_TOTAL"):
        "test_the_total_assertion_REDDENS_on_a_wrong_total_that_matches_an_ID "
        "and three siblings: a wrong total coinciding with an entry label, a "
        "wrong total with the true total in prose, a missing declaration, and a "
        "duplicated one. Plus a negative control on the real file.",
    ("tests/phase1/test_lessons_classification.py",
     "check_every_lesson_is_classified"):
        "test_the_SIBLING_assertions_redden_too -- an entry in no family.",
    ("tests/phase1/test_lessons_classification.py",
     "check_no_family_names_a_lesson_that_does_not_exist"):
        "test_the_SIBLING_assertions_redden_too -- a family naming a non-entry.",
    ("tests/phase1/test_lessons_classification.py",
     "check_the_families_are_DISJOINT"):
        "test_the_SIBLING_assertions_redden_too -- an entry in two families.",
    ("tests/phase1/test_decision_clock_consumers.py",
     "test_EVERY_read_is_in_exactly_one_class"):
        "test_A_NEW_UNCLASSIFIED_CONSUMER_FAILS_THE_TOTALITY and "
        "test_THE_INDIRECT_SHAPE_ALSO_FAILS, with two negative controls "
        "(a routed consumer, a compared read) and a file-without-the-string "
        "case.",
    ("tests/phase1/test_decision_clock_consumers.py",
     "test_the_PACKAGE_consumers_are_all_routed_through_the_refusal"):
        "same harness: a synthetic consumer that routes around the refusal is "
        "required to be reported.",
    ("tests/phase1/test_decision_clock_consumers.py",
     "test_NO_CANDIDATE_FILE_IS_INVISIBLE_TO_THE_SCAN"):
        "test_a_file_WITHOUT_the_string_is_excluded_and_never_parsed -- an "
        "unparseable file with no occurrence of the needle is excluded by "
        "proof rather than counted as a hole.",
    ("tests/phase1/test_manifest_hashes.py",
     "test_EVERY_manifest_hash_MATCHES_the_file_it_attests"):
        "test_a_TAMPERED_file_is_CAUGHT, plus an attested file that vanishes "
        "and a zero-coverage manifest.",
    ("tests/phase1/test_manifest_hashes.py", "test_a_TAMPERED_file_is_CAUGHT"):
        "it IS the mutation: a clean tree passes, the byte changes, the "
        "verifier names the file.",
    ("tests/phase1/test_certify_preconditions.py",
     "test_it_does_NOT_run_the_steps"):
        "the precondition is exercised unset / set / nonexistent / a file, and "
        "main()'s exit status is asserted in both directions; this one asserts "
        "the tool holds no subprocess call.",
}


def tracked_python_files() -> list:
    """Tracked AND untracked-non-ignored `.py`. R263 §3(b).

    `--others --exclude-standard` was added because a floor that reads only the
    index cannot see the module the current round wrote, so a sweep run before
    the commit sweeps the previous round's tree. D-V30A-102 records the
    instance; this is one of its siblings, corrected at the same time so the
    two do not answer the same question differently.
    """
    r = subprocess.run(["git", "-C", str(REPO), "ls-files", "--cached",
                        "--others", "--exclude-standard", "--", "*.py"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError("git ls-files failed: %s" % r.stderr[:200])
    return [f.strip() for f in r.stdout.splitlines() if f.strip()]


def _enclosing(tree, node):
    best = None
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if n.lineno <= node.lineno <= (n.end_lineno or n.lineno):
                if best is None or n.lineno > best.lineno:
                    best = n
    return best


def _reads_repo(node) -> bool:
    body = ast.unparse(node)
    return (any(s in body for s in REPO_READ)
            or any(h in body for h in REPO_HELPERS))


def _repo_fixtures(tree) -> set:
    """Fixtures whose own body reads the repository.

    THE DETECTOR MISSED THESE AND IT IS THE THIRD TIME. A test that receives its
    population as a fixture argument has no repository read in its own body --
    `test_EVERY_read_is_in_exactly_one_class(scanned)` is the flagship coverage
    assertion in this repository and was invisible to the first two versions of
    this enumeration. A population definition that excludes the cases that
    matter is the failure this sweep exists to find, occurring inside the sweep.
    """
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            decorated = any("fixture" in ast.unparse(d) for d in n.decorator_list)
            if decorated and _reads_repo(n):
                out.add(n.name)
    return out


def population() -> list:
    """Every assert in a test/check function whose population is the repository.

    Reached three ways: the function reads the repository itself, it calls a
    module helper that does, or it takes a FIXTURE that does.
    """
    rows = []
    for rel in tracked_python_files():
        try:
            tree = ast.parse((REPO / rel).read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError, OSError):
            continue
        fixtures = _repo_fixtures(tree)
        for a in ast.walk(tree):
            if not isinstance(a, ast.Assert):
                continue
            fn = _enclosing(tree, a)
            if fn is None or not (fn.name.startswith("test_")
                                  or fn.name.startswith("check_")):
                continue
            params = {p.arg for p in fn.args.args}
            if not (_reads_repo(fn) or (params & fixtures)):
                continue
            rows.append({"file": rel.replace("\\", "/"), "line": a.lineno,
                         "func": fn.name})
    return rows


def makes_a_coverage_claim(rel: str, func: str) -> tuple:
    """(bool, why) -- does this function assert over a COLLECTION it derived?

    **THE CRITERION THAT AUDITS THE ESCAPE HATCH.** R253 §3. Every entry in the
    population reads the repository -- that is how it got in -- so re-checking
    `out_of_scope` against THAT criterion clears all of them and establishes
    nothing. The sharper question is what the bucket actually asserts:

        a COVERAGE CLAIM asserts something about every member of a set, and can
        be vacuous over an empty one. A CONTENT CHECK asserts a fact about one
        artifact's text, and cannot.

    Audited when this was written: **6 of 19 `out_of_scope` entries did make a
    coverage claim** and had been parked. An exclusion set that grows without
    audit is where a population silently shrinks, and a misclassified entry is
    harder to notice than an unprobed one because it looks decided.
    """
    try:
        tree = ast.parse((REPO / rel).read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False, "unparseable"
    node = next((x for x in ast.walk(tree)
                 if isinstance(x, ast.FunctionDef) and x.name == func), None)
    if node is None:
        return False, "function not found"
    why = set()
    for a in ast.walk(node):
        if not isinstance(a, ast.Assert):
            continue
        t = a.test
        if isinstance(t, ast.UnaryOp) and isinstance(t.op, ast.Not):
            inner = t.operand
            if isinstance(inner, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
                why.add("assert not <comprehension>")
            elif isinstance(inner, ast.BinOp) and isinstance(inner.op, ast.Sub):
                why.add("assert not <set difference>")
            elif isinstance(inner, ast.Name):
                why.add("assert not <name>")
        for n in ast.walk(t):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                if n.func.id == "len":
                    why.add("len() comparison")
                elif n.func.id in ("set", "frozenset", "sorted"):
                    why.add("%s() comparison" % n.func.id)
            if isinstance(n, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
                why.add("comprehension in the assertion")
    for loop in ast.walk(node):
        if isinstance(loop, ast.For) and any(isinstance(x, ast.Assert)
                                             for x in ast.walk(loop)):
            why.add("assert inside a for-loop over a collection")
    return bool(why), "; ".join(sorted(why))


def state() -> dict:
    rows = population()
    keys = {(r["file"], r["func"]) for r in rows}
    done = {k for k in keys if k in ESTABLISHED}
    return {"rows": rows, "functions": keys, "established": done,
            "outstanding": sorted(keys - done),
            "stray": sorted(set(ESTABLISHED) - keys)}


def main(argv=None) -> int:
    s = state()
    print("COVERAGE-ASSERTION SWEEP -- population and completion state")
    print("  population: asserts in test/check functions that read the "
          "repository")
    print("  floor     : git ls-files -- *.py  (%d files)"
          % len(tracked_python_files()))
    print()
    print("  assertions in the population : %d" % len(s["rows"]))
    print("  functions holding them       : %d" % len(s["functions"]))
    print("  ESTABLISHED (mutation shown) : %d" % len(s["established"]))
    print("  OUTSTANDING                  : %d" % len(s["outstanding"]))
    if s["stray"]:
        print()
        print("  REGISTERED BUT NOT PRESENT (a claim about nothing):")
        for f, fn in s["stray"]:
            print("    %s :: %s" % (f, fn))
    print()
    print("OUTSTANDING -- each needs a mutation shown to make it red:")
    byf = {}
    for f, fn in s["outstanding"]:
        byf.setdefault(f, []).append(fn)
    for f in sorted(byf):
        print("  %s" % f)
        for fn in sorted(byf[f]):
            print("      %s" % fn)
    print()
    print("NOT A GATE. This reports; it does not fail the build, because an "
          "instrument that failed until every entry was marked done would be "
          "pressure to mark entries done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
