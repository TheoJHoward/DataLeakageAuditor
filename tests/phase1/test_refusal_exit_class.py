"""Every refusal the CLI can reach exits 2. R276 §1(1).

THE DEFECT. `SystemExit(message)` prints the message and exits **1**, and 1 is
this tool's FINDINGS class. So a misspelt key in a model file, and a model file
with no decision column, were reported to any reader of the exit status as
"leaks found". R275's walk measured both: named errors, correct prose, wrong
class. A configuration error read as a result is the worst misread this tool can
produce, because it is the one a machine acts on without a person seeing it.

THE MECHANISM. `cli.Refusal` is raised everywhere a usage refusal is decided,
`main` catches it beside the library's own deliberate errors, prints it on
stderr and returns `EXIT_USAGE`. One mapping, one place.

THE TOTALITY, in two halves:
  * STATIC -- no module under `src/leakaudit`, tracked or untracked, raises
    `SystemExit` at all, except the console entry point `raise SystemExit(main())`.
  * LIVE -- every refusal below is RUN, and each has to come back 2 with its
    message on stderr. The two the walk found are marked RED.
"""
from __future__ import annotations

import ast
import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                         # noqa: E402

SRC = ROOT / "src" / "leakaudit"


# --------------------------------------------------------------------------
# the static half
# --------------------------------------------------------------------------

def _population() -> list:
    """Tracked AND untracked modules under src/leakaudit: the floor, both ways."""
    out = set()
    for args in (["ls-files"], ["ls-files", "--others", "--exclude-standard"]):
        r = subprocess.run(["git", "-C", str(ROOT), *args, "src/leakaudit"],
                           capture_output=True, text=True, encoding="utf-8")
        assert r.returncode == 0, r.stderr
        out |= {l.strip() for l in r.stdout.splitlines()
                if l.strip().endswith(".py")}
    return sorted(out)


def _system_exits(source: str, module: str) -> set:
    tree = ast.parse(source)
    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Raise) or node.exc is None:
            continue
        exc = node.exc
        name = None
        if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name):
            name = exc.func.id
        elif isinstance(exc, ast.Name):
            name = exc.id
        if name != "SystemExit":
            continue
        arg = ""
        if isinstance(exc, ast.Call) and exc.args:
            arg = ast.dump(exc.args[0])
        found.add((module, "main()" if "'main'" in arg else ast.unparse(node)))
    return found


def test_the_population_is_READ_from_git_and_is_not_empty():
    pop = _population()
    assert "src/leakaudit/cli.py" in pop and len(pop) > 5, pop


def test_NO_module_raises_SystemExit_except_the_console_ENTRY_POINT():
    pop = _population()
    assert len(pop) > 5, (
        "the population is empty, so this absence claim is about nothing: %s"
        % pop)
    stray = set()
    for rel in pop:
        p = ROOT / rel
        if p.is_file():
            stray |= {s for s in _system_exits(p.read_text(encoding="utf-8"),
                                               p.stem)
                      if s[1] != "main()"}
    assert not stray, (
        "`SystemExit(message)` exits 1, the FINDINGS class, so a refusal raised "
        "this way is reported to a script as a leak. Raise `cli.Refusal` "
        "instead, which `main` maps to EXIT_USAGE: %s" % sorted(stray))


def test_the_ENTRY_POINT_is_still_there():
    text = (SRC / "cli.py").read_text(encoding="utf-8")
    assert "raise SystemExit(main())" in text
    assert "class Refusal(Exception):" in text


def test_REFUSAL_is_caught_beside_the_librarys_own_errors():
    assert cli.Refusal in cli._expected_errors()


# --------------------------------------------------------------------------
# the live half
# --------------------------------------------------------------------------

@pytest.fixture
def work(tmp_path):
    secs = pd.date_range("2026-04-01 09:00:00", periods=60, freq="1s")
    rng = np.random.default_rng(5)
    pd.DataFrame({"timestamp": [s + pd.Timedelta(milliseconds=200) for s in secs],
                  "p": rng.standard_normal(60)}).to_csv(tmp_path / "snap.csv",
                                                        index=False)
    pd.DataFrame({"k": secs, "v": rng.standard_normal(60)}).to_csv(
        tmp_path / "agg.csv", index=False)
    (tmp_path / "aware.csv").write_text(
        (tmp_path / "agg.csv").read_text(encoding="utf-8").replace(
            "2026-04-01 09", "2026-04-01T09").replace(",", "+00:00,", 0),
        encoding="utf-8")
    pd.DataFrame({"k": secs.tz_localize("UTC"),
                  "v": rng.standard_normal(60)}).to_csv(tmp_path / "aware.csv",
                                                        index=False)
    # A NAME OF ITS OWN. Two test modules writing `p.py` into their own tmp
    # directories share one `sys.modules` entry, and the first import wins.
    (tmp_path / "rfp.py").write_text(
        "import pandas as pd\n"
        "def build(f):\n"
        "    o = f['snap'].copy()\n"
        "    o['timestamp'] = pd.to_datetime(o['timestamp'])\n"
        "    a = f.get('agg', f.get('aware'))\n"
        "    if a is not None:\n"
        "        a = a.copy(); a['k'] = pd.to_datetime(a['k'])\n"
        "        try:\n"
        "            a['k'] = a['k'].dt.tz_convert(None)\n"
        "        except (TypeError, AttributeError):\n"
        "            pass\n"
        "        o['x'] = o['timestamp'].dt.floor('1s').map(\n"
        "            a.set_index('k')['v']).to_numpy()\n"
        "    return o[['timestamp', 'x']]\n", encoding="utf-8")
    (tmp_path / "rfboom.py").write_text("raise RuntimeError('inside')\n",
                                        encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    yield tmp_path
    sys.path.remove(str(tmp_path))


def _model(tmp, name, doc):
    p = tmp / name
    p.write_text(json.dumps(doc), encoding="utf-8")
    return str(p)


def _cases(tmp) -> list:
    """(label, argv). Every one is a refusal, and every one is RUN below."""
    snap = "snap=%s" % (tmp / "snap.csv")
    agg = "agg=%s" % (tmp / "agg.csv")
    good = _model(tmp, "m.json", {"version": 5, "aggregate_frames": {"agg": "k"},
                                  "decision_column": "timestamp"})
    typo = _model(tmp, "m_typo.json", {"version": 5,
                                       "aggregate_frame": {"agg": "k"},
                                       "decision_column": "timestamp"})
    nodec = _model(tmp, "m_nodec.json", {"version": 5,
                                         "aggregate_frames": {"agg": "k"}})
    aware = _model(tmp, "m_aware.json", {"version": 5,
                                         "aggregate_frames": {"aware": "k"},
                                         "decision_column": "timestamp"})
    (tmp / "bad.json").write_text("{not json", encoding="utf-8")
    (tmp / "prof_bad.json").write_text(
        json.dumps({"version": 5, "decision_column": "t"}), encoding="utf-8")
    (tmp / "prof_ok.json").write_text(
        json.dumps({"version": 5, "window_seconds": 1.0}), encoding="utf-8")
    (tmp / "data.xlsx").write_text("no", encoding="utf-8")
    base = ["run", "--pipeline", "rfp:build", "--frame", snap, "--frame", agg]
    return [
        ("pipeline spec with no function", ["run", "--pipeline", "p",
                                            "--frame", snap]),
        ("module not on the path", ["run", "--pipeline", "nosuch:build",
                                    "--frame", snap]),
        ("module raises on import", ["run", "--pipeline", "rfboom:build",
                                     "--frame", snap]),
        ("no such attribute", ["run", "--pipeline", "rfp:nope", "--frame", snap]),
        ("frame pair with no `=`", ["run", "--pipeline", "rfp:build",
                                    "--frame", "justapath.csv"]),
        ("frame file absent", ["run", "--pipeline", "rfp:build",
                               "--frame", "snap=%s" % (tmp / "gone.csv")]),
        ("unreadable extension", ["run", "--pipeline", "rfp:build",
                                  "--frame", "snap=%s" % (tmp / "data.xlsx")]),
        ("no --frame at all", ["run", "--pipeline", "rfp:build"]),
        ("--slice-from without --model", base + ["--slice-from", "2026-04-01"]),
        ("--padding without --model", base + ["--padding", "1h"]),
        ("--complete without --model", base + ["--complete"]),
        ("--confirm without --model", base + ["--confirm"]),
        ("--confirm-cap without --confirm", base + ["--confirm-cap", "2"]),
        ("--confirm-cap below one", base + ["--model", good, "--confirm",
                                            "--confirm-cap", "0"]),
        ("--profile without --model", base + ["--profile",
                                              str(tmp / "prof_ok.json")]),
        ("model file absent", base + ["--model", str(tmp / "gone.json")]),
        ("model file not JSON", base + ["--model", str(tmp / "bad.json")]),
        ("RED: misspelt model key", base + ["--model", typo]),
        ("RED: no decision column", base + ["--model", nodec]),
        ("profile path absent", base + ["--model", good, "--profile",
                                        str(tmp / "gone.json")]),
        ("profile carrying a structural key",
         base + ["--model", good, "--profile", str(tmp / "prof_bad.json")]),
        ("aware key with no zone declared",
         ["run", "--pipeline", "rfp:build", "--frame", snap,
          "--frame", "aware=%s" % (tmp / "aware.csv"), "--model", aware]),
        ("check with a model file that is not JSON",
         ["check", "--pipeline", "rfp:build", "--frame", snap,
          "--model", str(tmp / "bad.json")]),
        ("draft onto a target that exists",
         ["draft", "--frame", agg, "--out", good]),
        ("draft with a profile that does not resolve",
         ["draft", "--frame", agg, "--profile", str(tmp / "gone.json"),
          "--out", str(tmp / "fresh.json")]),
    ]


def _run(argv) -> tuple:
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        rc = cli.main(argv)
    return rc, err.getvalue()


def test_EVERY_refusal_the_CLI_reaches_EXITS_TWO(work):
    wrong = []
    for label, argv in _cases(work):
        rc, err = _run(argv)
        if rc != cli.EXIT_USAGE or not err.strip():
            wrong.append((label, rc, err.strip()[:80]))
    assert not wrong, (
        "a refusal that exits anything but 2 is read by a script as a result: %s"
        % wrong)


@pytest.mark.parametrize("label", ["RED: misspelt model key",
                                   "RED: no decision column"])
def test_THE_TWO_THE_WALK_FOUND_exit_two_and_say_why(work, label):
    """R275's walk: both were named errors and both exited 1."""
    argv = dict((l, a) for l, a in _cases(work))[label]
    rc, err = _run(argv)
    assert rc == cli.EXIT_USAGE == 2, err
    assert rc != cli.EXIT_FINDINGS
    if "misspelt" in label:
        assert "unknown key(s) ['aggregate_frame']" in err, err
    else:
        assert "no decision column is declared" in err, err
        # R276 §1(2): the asker is named inside the sentence, not after it.
        assert "(asked by the model file" in err, err
        assert "for it. the model file" not in err, "the dangling fragment"


def test_the_case_list_is_not_SILENTLY_SHORT(work):
    """A totality whose population shrank would pass while covering less."""
    assert len(_cases(work)) >= 25


def test_a_CLEAN_run_is_not_a_refusal(work):
    """The negative control: the same machinery on a working configuration
    returns a result class, not 2."""
    good = _model(work, "m.json", {"version": 5,
                                   "aggregate_frames": {"agg": "k"},
                                   "decision_column": "timestamp"})
    rc, _err = _run(["run", "--pipeline", "rfp:build",
                     "--frame", "snap=%s" % (work / "snap.csv"),
                     "--frame", "agg=%s" % (work / "agg.csv"),
                     "--model", good])
    assert rc != cli.EXIT_USAGE, "a working run reported as a usage error"
