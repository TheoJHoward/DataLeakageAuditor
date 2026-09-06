"""Every command, invoked as a USER invokes it. R233 §3.

**THE HOLE THIS CLOSES HAS BITTEN THREE TIMES, always the same way: the test took
the library path and the user takes the command line.**

1. **P0** was fixed at `audit()` and not at the CLI.
2. **Three config keys** — `column_modes`, `ties_available`, `timestamp_column` —
   reached the library and not the command.
3. **`draft` worked on frames and not on files.** Every test in
   `test_inference.py` builds its frames with `pd.date_range`, which yields
   `datetime64`. The CLI loads CSVs, where every column arrives as **text** — and
   under pandas 3 a text column's dtype is `str`, not `object`, which the
   type check asked for. On the development environment the draft determined
   **nothing at all** and the suite was green.

**THE DISCRIMINATING INPUT ALREADY EXISTS AND IT IS THE ONE THAT CAUGHT (3): a
CSV with string timestamps.** Every test here reads from disk in a user's format.
A CLI-path test that passed on pre-built frames would be testing the library path
in disguise, so these tests write files and pass paths — never DataFrames.

**TOTALITY.** `COMMANDS` below is checked against the parser's own subparsers:
disjoint, jointly covering, and a new command fails this file until it has a
CLI-path test. That is the point — writing the test is the work, and the failure
is what makes somebody do it.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                        # noqa: E402

DATA = ROOT / "tests" / "phase1" / "portability_data"

# command -> the test here that exercises it through the CLI entry point.
COMMANDS = {
    "run": "test_run_through_the_cli_on_files_from_disk",
    "check": "test_check_through_the_cli_on_files_from_disk",
    "draft": "test_draft_through_the_cli_writes_a_file_from_csvs",
    "schema": "test_schema_through_the_cli_prints_the_format",
}


@pytest.fixture
def work(tmp_path, monkeypatch):
    """A user's directory: CSVs and a pipeline module, on disk.

    THE FRAMES ARE NEVER CONSTRUCTED HERE. They are copied from
    `portability_data/` and read by the CLI itself, so every column arrives as
    the user's loader produces it -- which is what made defect (3) invisible to
    the library-path tests.
    """
    for name in ("stations.csv", "scans.csv"):
        shutil.copy(DATA / name, tmp_path / name)
    shutil.copy(DATA / "pipeline.py", tmp_path / (PIPE + ".py"))
    monkeypatch.chdir(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    # A UNIQUE MODULE NAME, AND IT IS REMOVED AFTERWARDS. `sys.modules` caches by
    # NAME, not by path: the first version called this `mypipe`, which is also
    # what `test_the_walks_wrong_turns.py` writes into its own tmp_path. Whichever
    # file imported first won, and the other three tests got this file's pipeline
    # -- failing with `Label(s) ['weight_kg'] do not exist`, an error about a
    # column in the wrong module. Suite-order dependence introduced by a new test
    # file, and caught only because those tests already existed.
    yield tmp_path
    sys.modules.pop(PIPE, None)


PIPE = "clipath_pipeline"


def _frames(work):
    return ["--frame", "stations=%s" % (work / "stations.csv"),
            "--frame", "scans=%s" % (work / "scans.csv")]


def _run(argv):
    """Invoke the CLI and return (exit code, everything it printed)."""
    try:
        rc = cli.main(argv)
    except SystemExit as e:
        return (e.code if isinstance(e.code, int) else 2), str(e)
    return rc, ""


# ---------------------------------------------------------------------------
# TOTALITY -- the population is the parser's own commands.
# ---------------------------------------------------------------------------

def _parser_commands() -> set:
    import argparse
    ap = cli.build_parser()
    for action in ap._actions:                      # noqa: SLF001
        if isinstance(action, argparse._SubParsersAction):   # noqa: SLF001
            return set(action.choices)
    raise AssertionError("the CLI has no subcommands any more")


def test_every_CLI_command_has_a_cli_path_test():
    missing = _parser_commands() - set(COMMANDS)
    assert not missing, (
        "these commands have no test that invokes them as a user does, so the "
        "hole that bit three times is open for them: %s" % sorted(missing))


def test_no_cli_path_test_names_a_command_that_does_not_exist():
    stray = set(COMMANDS) - _parser_commands()
    assert not stray, "named here and not a command: %s" % sorted(stray)


def test_every_named_cli_path_test_actually_exists_in_this_file():
    """A hand-written map drifts from the code. This one is checked."""
    here = globals()
    for command, testname in COMMANDS.items():
        assert callable(here.get(testname)), (
            "%r is mapped to %r and no such test is defined here"
            % (command, testname))


# ---------------------------------------------------------------------------
# One per command, all reading files the CLI itself loads.
# ---------------------------------------------------------------------------

def test_draft_through_the_cli_writes_a_file_from_csvs(work, capsys):
    """The known positive that discriminates. These CSVs' timestamp columns
    arrive as TEXT, which is the input the library-path tests never saw."""
    out = work / "model.json"
    rc, _ = _run(["draft"] + _frames(work) + ["--out", str(out)])
    assert rc == cli.EXIT_OK_SILENT
    assert out.is_file(), "the draft was not written"

    body = json.loads(out.read_text(encoding="utf-8"))
    assert body["aggregate_frames"] == {"stations": "timestamp",
                                        "scans": "scanned_at"}, (
        "structure was NOT determined from CSV-loaded frames -- which is the "
        "exact defect this file exists for: %s" % body.get("aggregate_frames"))
    prov = body["draft_provenance"]
    assert sorted(prov["unfilled_availability"]) == ["scans.scanned_at",
                                                     "stations.timestamp"]
    assert prov["structure_edited_by_hand"] is False
    assert prov["generated_by"] == "leakaudit draft"
    assert prov["source_frames"]["stations"][0] > 0

    text = capsys.readouterr().out
    assert "WRITTEN:" in text and "It is a DRAFT" in text


def test_draft_through_the_cli_REFUSES_to_overwrite(work):
    out = work / "model.json"
    out.write_text('{"version": 3}', encoding="utf-8")
    before = out.read_text(encoding="utf-8")
    rc, msg = _run(["draft"] + _frames(work) + ["--out", str(out)])
    assert rc == 2, "overwriting was not refused"
    assert "already exists" in msg
    assert out.read_text(encoding="utf-8") == before, "the file was clobbered"


def test_run_through_the_cli_REFUSES_an_unfilled_draft_and_NAMES_the_blanks(work):
    out = work / "model.json"
    _run(["draft"] + _frames(work) + ["--out", str(out)])
    rc, msg = _run(["run", "--pipeline", PIPE + ":build"] + _frames(work)
                   + ["--model", str(out)])
    assert rc == cli.EXIT_USAGE
    assert "THIS IS A DRAFT" in msg
    assert "scans.scanned_at" in msg and "stations.timestamp" in msg, (
        "the refusal does not name which fields are blank, which is the "
        "difference between a message and a route out: %s" % msg)


def test_run_through_the_cli_on_files_from_disk(work, capsys):
    rc, msg = _run(["run", "--pipeline", PIPE + ":build"] + _frames(work))
    assert rc in (cli.EXIT_FINDINGS, cli.EXIT_OK_SILENT), msg
    text = capsys.readouterr().out
    assert "leakaudit:" in text


def test_run_under_DRAFTED_structure_says_so_in_the_output(work, capsys):
    """R233 §1(d). Availability can no longer be accepted unread -- the tool
    never guesses it -- but structure can, and a finding resting on a key column
    a program chose should carry that fact."""
    out = work / "model.json"
    _run(["draft"] + _frames(work) + ["--out", str(out)])
    body = json.loads(out.read_text(encoding="utf-8"))
    body["draft_provenance"]["unfilled_availability"] = []
    body["decision_column"] = "timestamp"
    out.write_text(json.dumps(body, indent=2), encoding="utf-8")
    capsys.readouterr()

    _run(["run", "--pipeline", PIPE + ":build"] + _frames(work)
         + ["--model", str(out)])
    text = capsys.readouterr().out
    assert "STRUCTURE WAS DRAFTED, NOT WRITTEN" in text, text[-1500:]
    assert "structure_edited_by_hand" in text


def test_check_through_the_cli_on_files_from_disk(work, capsys):
    rc, msg = _run(["check", "--pipeline", PIPE + ":build"] + _frames(work))
    assert rc in (cli.EXIT_FINDINGS, cli.EXIT_OK_SILENT,
                  cli.EXIT_NOTHING_PROBED), msg
    text = capsys.readouterr().out
    assert "check(s) ran" in text


def test_schema_through_the_cli_prints_the_format(capsys):
    rc, _ = _run(["schema"])
    assert rc == 0
    text = capsys.readouterr().out
    assert '"version": 3' in text and "aggregate_frames" in text


# ---------------------------------------------------------------------------
# The discriminating property of this whole file.
# ---------------------------------------------------------------------------

def test_this_file_never_constructs_a_dataframe():
    """THE PROPERTY THAT MAKES THESE CLI-PATH TESTS. A test that built its
    frames would be exercising the library path with a CLI wrapper around it,
    and would have passed on the very defect this file was written for.

    IT PARSES RATHER THAN MATCHING TEXT, and it took two failures to get there.
    A substring scan failed on its own banned-token list, then on the module
    docstring that EXPLAINS the defect -- prose about `pd.date_range` is not a
    call to it. **R218 ruled this exact case: fix the parser, do not reword the
    docstring**, after the installability checker read an English sentence as an
    import. A docstring is a string constant and simply is not a call, so with
    `ast` there is nothing to exempt.

    That the check tripped over itself twice is TB-25's shape in miniature --
    the document about a defect class is where the class appears -- on the first
    run of a file written in the round that recorded it.
    """
    import ast
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    banned = {"DataFrame", "date_range", "read_csv", "read_parquet"}
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in banned:
            found.append(node.attr)
        elif isinstance(node, ast.Name) and node.id in banned:
            found.append(node.id)
    assert not found, (
        "this file CALLS %s: its inputs must be FILES the CLI loads, not frames "
        "a test built -- otherwise it exercises the library path with a CLI "
        "wrapper around it, which is the defect it exists for"
        % sorted(set(found)))
