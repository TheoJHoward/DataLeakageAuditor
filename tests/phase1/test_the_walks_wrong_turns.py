"""Every wrong turn the definition-of-done walk took, as a test. R210 §2.

THE TRANSCRIPT IS THE ACCEPTANCE SUITE FOR ITS OWN FIXES. Each test here is one
step a stranger actually took, re-run, asserting that the message now names the
ROUTE OUT and not only the failure. The standard is not invented: it is the one
this package already set in its config refusals -- the v2-model message naming
three routes out, and the malformed-JSON message naming the error, its offset,
and why refusing beats guessing.

WHAT IS NOT ASSERTED IS AS IMPORTANT. A user's own pipeline raising must still
produce a traceback pointing at THEIR file. The boundary catches the errors this
package raises on purpose; catching everything would turn a bug in this tool into
a message blaming the user, which is the mirror image of the defect being fixed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                        # noqa: E402
from leakaudit.contract import ContractError, guarded_build      # noqa: E402


@pytest.fixture
def work(tmp_path, monkeypatch):
    """The walk's own two frames, small, written where the CLI can read them."""
    secs = pd.date_range("2026-04-01 08:00:00", periods=40, freq="1s")
    pd.DataFrame({
        "timestamp": secs + pd.Timedelta(milliseconds=300),
        "queue_depth": range(40),
    }).to_csv(tmp_path / "stations.csv", index=False)
    pd.DataFrame({
        "scanned_at": [s + pd.Timedelta(milliseconds=400) for s in secs],
        "items": range(40),
    }).to_csv(tmp_path / "scans.csv", index=False)
    (tmp_path / "mypipe.py").write_text(
        "import pandas as pd\n"
        "def build(frames):\n"
        "    st = frames['stations'].copy()\n"
        "    st['timestamp'] = pd.to_datetime(st['timestamp'])\n"
        "    sc = frames['scans'].copy()\n"
        "    sc['sec'] = pd.to_datetime(sc['scanned_at']).dt.floor('1s')\n"
        "    st['sec'] = st['timestamp'].dt.floor('1s')\n"
        "    agg = sc.groupby('sec')['items'].sum().rename('items_total')\n"
        "    st['items_total'] = st['sec'].map(agg).fillna(0)\n"
        "    return st[['timestamp', 'queue_depth', 'items_total']]\n",
        encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _args(work, *extra):
    return ["run", "--pipeline", "mypipe:build",
            "--frame", "stations=%s" % (work / "stations.csv"),
            "--frame", "scans=%s" % (work / "scans.csv")] + list(extra)


def _model(work, name, obj):
    p = work / name
    p.write_text(json.dumps(obj), encoding="utf-8")
    return str(p)


# ---------------------------------------------------------------------------
# ITEM 2 -- the first hard stop, at the first command.
# ---------------------------------------------------------------------------

def test_item2_a_module_beside_you_names_the_route_out(work):
    """The wrong turn: run from the module's own directory with no PYTHONPATH.

    `SystemExit(message)` is this module's existing idiom for a usage error and
    Python prints it as one clean line with no traceback, which is the observable
    behaviour under test. What is asserted is the CONTENT.
    """
    for p in (str(work), ""):
        while p in sys.path:
            sys.path.remove(p)
    with pytest.raises(SystemExit) as e:
        cli.main(_args(work))
    text = str(e.value)
    assert "Traceback" not in text
    assert "PYTHONPATH" in text, (
        "the message names the failure and not the route out, which is the "
        "class this whole item is about:\n%s" % text)
    assert "pip install -e" in text
    assert "mypipe.py" in text, (
        "the file is sitting in the working directory and the message does not "
        "mention it:\n%s" % text)


def test_item2_an_import_that_RAISES_is_not_called_a_path_problem(work):
    """A module that IS found and blows up must not be blamed on the path."""
    (work / "boom.py").write_text("raise RuntimeError('inside my module')\n",
                                  encoding="utf-8")
    sys.path.insert(0, str(work))
    try:
        with pytest.raises(SystemExit) as e:
            cli.main(["run", "--pipeline", "boom:build",
                      "--frame", "stations=%s" % (work / "stations.csv")])
    finally:
        sys.path.remove(str(work))
    text = str(e.value)
    assert "inside your own code" in text and "RuntimeError" in text
    assert "PYTHONPATH" not in text, (
        "a module that was found and raised is being offered a path fix:\n%s"
        % text)


# ---------------------------------------------------------------------------
# ITEMS 3 and 4 -- ProbeError as a traceback, and a symptom instead of a cause.
# ---------------------------------------------------------------------------

def test_item3_a_wrong_key_column_is_ONE_LINE_not_a_traceback(work, capsys):
    sys.path.insert(0, str(work))
    try:
        rc = cli.main(_args(work, "--model", _model(work, "bad_key.json", {
            "version": 3, "aggregate_frames": {"scans": "scan_time"},
            "decision_column": "timestamp"})))
    finally:
        sys.path.remove(str(work))
    out = capsys.readouterr()
    text = (out.out + out.err).strip()
    assert rc == cli.EXIT_USAGE
    assert "Traceback" not in text
    assert text.count("\n") == 0, "not one line:\n%s" % text
    assert "has no key column 'scan_time'" in text


def test_item4_a_misspelled_frame_names_DECLARED_and_SUPPLIED(work, capsys):
    sys.path.insert(0, str(work))
    try:
        rc = cli.main(_args(work, "--model", _model(work, "bad_frame.json", {
            "version": 3, "aggregate_frames": {"scan": "scanned_at"},
            "decision_column": "timestamp"})))
    finally:
        sys.path.remove(str(work))
    out = capsys.readouterr()
    text = out.out + out.err
    assert rc == cli.EXIT_USAGE
    assert "Traceback" not in text
    assert "'scan'" in text and "'scans'" in text and "'stations'" in text, (
        "the message must name what was declared against what was supplied -- "
        "without both, the reader is left with a symptom:\n%s" % text)
    assert "Correct the name" in text


# ---------------------------------------------------------------------------
# ITEM 6 -- the contract is annotated AND checked. These are separate items and
# this file tests the CHECK; the annotation is inspected in its own test below.
# ---------------------------------------------------------------------------

def test_item6_a_build_returning_a_dict_is_told_so(work, capsys):
    (work / "badpipe.py").write_text(
        "def returns_a_dict(frames):\n    return {'a': [1, 2]}\n"
        "def returns_nothing(frames):\n    pass\n", encoding="utf-8")
    sys.path.insert(0, str(work))
    try:
        rc = cli.main(["run", "--pipeline", "badpipe:returns_a_dict",
                       "--frame", "stations=%s" % (work / "stations.csv")])
    finally:
        sys.path.remove(str(work))
    out = capsys.readouterr()
    text = out.out + out.err
    assert rc == cli.EXIT_USAGE
    assert "Traceback" not in text
    assert "returned dict" in text and "pd.DataFrame(" in text, (
        "the message must name what arrived and the route out:\n%s" % text)


def test_item6_a_build_returning_None_is_told_so(work, capsys):
    (work / "badpipe.py").write_text(
        "def returns_nothing(frames):\n    pass\n", encoding="utf-8")
    sys.path.insert(0, str(work))
    try:
        rc = cli.main(["run", "--pipeline", "badpipe:returns_nothing",
                       "--frame", "stations=%s" % (work / "stations.csv")])
    finally:
        sys.path.remove(str(work))
    out = capsys.readouterr()
    text = out.out + out.err
    assert rc == cli.EXIT_USAGE
    assert "returned None" in text and "falls off the end" in text


def test_item6_the_guard_is_IDEMPOTENT(work):
    """The CLI wraps and `audit` wraps again; two frames of plumbing in a
    traceback whose value is that it points at the user's file."""
    def build(frames):
        return pd.DataFrame({"a": [1]})

    once = guarded_build(build)
    twice = guarded_build(once)
    assert twice is once, "double-wrapped: the user's traceback gains a frame"


def test_item6_the_guard_lets_the_USERS_OWN_EXCEPTION_THROUGH(work):
    """Not an item, and the thing that must not regress."""
    def build(frames):
        raise ValueError("my own pipeline is broken")

    with pytest.raises(ValueError, match="my own pipeline is broken"):
        guarded_build(build)({})


def test_the_boundary_does_not_swallow_a_bug_in_THIS_tool(work, capsys):
    """A bare except at the boundary would print our bug as the user's mistake."""
    expected = cli._expected_errors()
    assert ContractError in expected
    assert not any(e in (Exception, BaseException) for e in expected), (
        "the boundary catches everything, so a defect in this tool prints as "
        "though the user had made a mistake -- the mirror image of the defect "
        "the boundary was added to fix")


# ---------------------------------------------------------------------------
# ITEMS 1 and 5 -- documentation. Asserted separately from the CHECK above,
# because R210 is explicit that an annotation is not a check.
# ---------------------------------------------------------------------------

def test_item1_the_build_CONTRACT_is_stated_in_the_help():
    text = cli.build_parser().format_help()
    for sub in ("run", "check"):
        p = [a for a in cli.build_parser()._subparsers._group_actions[0]
             .choices.items() if a[0] == sub][0][1]
        h = p.format_help()
        assert "dict" in h and "--frame" in h, (
            "`%s --help` does not say what the build function receives:\n%s"
            % (sub, h))
        assert "DataFrame" in h, (
            "`%s --help` does not say what it must return:\n%s" % (sub, h))
    assert text


def test_item1_the_ANNOTATION_states_the_argument_side_too():
    """It said `Callable[[Any], pd.DataFrame]` -- the half nobody had to guess."""
    from leakaudit.contract import audit
    ann = str(audit.__annotations__.get("build", ""))
    assert "Any]" not in ann, (
        "the argument side is still `Any`, and the annotation is where a reader "
        "looks for the contract: %r" % ann)
    assert "Mapping" in ann and "DataFrame" in ann, ann


def test_item5_the_json_orientation_is_stated():
    p = [a for a in cli.build_parser()._subparsers._group_actions[0]
         .choices.items() if a[0] == "run"][0][1]
    h = p.format_help()
    assert "records" in h, (
        "`--frame x.json` does not say which pandas orient is expected, so a "
        "stranger writing orient='split' finds out by failing:\n%s" % h)
