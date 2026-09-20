"""What a reader gets: one stream, a table that reconciles, a priced remedy.

R276 §1(10)(7)(6)(8), the gaps R275's walk measured at the terminal:

  (10) the report, the coverage table and the line saying what to do next are
       all on STDOUT. `> report.txt` used to keep the coverage numbers and lose
       the remedy, which printed on stderr.
  (7)  the remedy prices `--complete` FOR THIS DATA, from this run's own stride
       and its own clean build, rather than naming the flag and no number.
  (6)  the table reconciles with the findings above it: a head cohort is probed
       and counted ineligible, so a run could print two findings over a table
       saying one cohort was probed.
  (8)  `leakaudit schema` says where the installed template is, not only what
       is in it.

THE PAIR for (10) and (7): one frame set, one model, two builders -- one that
reads the second it decides in, one that reads the previous second.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import leakaudit.model_file as mf                                 # noqa: E402
from leakaudit import cli                                         # noqa: E402
from leakaudit.coverage import Coverage                           # noqa: E402

N = 120


@pytest.fixture
def work(tmp_path):
    secs = pd.date_range("2026-05-04 09:30:00", periods=N, freq="1s")
    rng = np.random.default_rng(13)
    pd.DataFrame({"timestamp": [s + pd.Timedelta(milliseconds=250) for s in secs],
                  "price": rng.standard_normal(N)}).to_csv(tmp_path / "snap.csv",
                                                           index=False)
    pd.DataFrame({"k": secs, "volume": rng.integers(1, 500, N)}).to_csv(
        tmp_path / "agg.csv", index=False)
    # Its own module name: `p` is taken by another test module's fixture, and
    # `sys.modules` keeps whichever imported first.
    (tmp_path / "rsp.py").write_text(
        "import pandas as pd\n"
        "def _join(f, shift):\n"
        "    o = f['snap'].copy()\n"
        "    o['timestamp'] = pd.to_datetime(o['timestamp'])\n"
        "    a = f['agg'].copy()\n"
        "    a['k'] = pd.to_datetime(a['k']) + pd.Timedelta(seconds=shift)\n"
        "    o['vol'] = o['timestamp'].dt.floor('1s').map(\n"
        "        a.set_index('k')['volume']).to_numpy()\n"
        "    return o[['timestamp', 'price', 'vol']]\n"
        "def leaky(f):\n"
        "    return _join(f, 0)\n"
        "def clean(f):\n"
        "    return _join(f, 1)\n", encoding="utf-8")
    (tmp_path / "m.json").write_text(json.dumps(
        {"version": 5, "aggregate_frames": {"agg": "k"},
         "decision_column": "timestamp"}), encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    yield tmp_path
    sys.path.remove(str(tmp_path))


def _run(work, fn, *extra):
    return cli.main(["run", "--pipeline", "rsp:%s" % fn,
                     "--frame", "snap=%s" % (work / "snap.csv"),
                     "--frame", "agg=%s" % (work / "agg.csv"),
                     "--model", str(work / "m.json"), *extra])


# --------------------------------------------------------------------------
# (10) one stream
# --------------------------------------------------------------------------

def test_the_REMEDY_and_the_TABLE_are_BOTH_on_stdout(work, capsys):
    code = _run(work, "clean")
    cap = capsys.readouterr()
    assert code == cli.EXIT_INCOMPLETE_SILENT
    assert "INCOMPLETE AND SILENT" in cap.out, cap.out[-2000:]
    assert "COVERAGE (reported, not thresholded" in cap.out
    assert "INCOMPLETE AND SILENT" not in cap.err, (
        "the line telling a reader what to do next is on the stream they are "
        "least likely to have captured: %r" % cap.err)
    assert cap.err == "", cap.err


def test_a_FINDINGS_run_puts_nothing_a_reader_needs_on_stderr(work, capsys):
    code = _run(work, "leaky")
    cap = capsys.readouterr()
    assert code == cli.EXIT_FINDINGS
    assert "finding(s) over" in cap.out and "COVERAGE" in cap.out
    assert cap.err == "", cap.err


def test_the_CONVENTION_is_stated_in_help():
    text = cli.build_parser().format_help()
    for part in ("run", ):
        assert part in text
    run_help = cli.STREAMS
    assert "stdout carries the report" in run_help
    assert "stderr carries refusals" in run_help
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        with pytest.raises(SystemExit):
            cli.build_parser().parse_args(["run", "--help"])
    assert "stdout carries the report" in buf.getvalue()


# --------------------------------------------------------------------------
# (7) the remedy carries the cost, measured here
# --------------------------------------------------------------------------

def test_the_REMEDY_prices_COMPLETE_from_THIS_RUNS_measurements(work, capsys):
    _run(work, "clean")
    out = capsys.readouterr().out
    line = next(l for l in out.splitlines() if "INCOMPLETE AND SILENT" in l)
    m = re.search(r"FOR THIS DATA that is (\d+) pass\(es\) at stride \1, one "
                  r"rebuild each, from (.+?): at least ~([\d.]+) (s|min|h) at "
                  r"the ([\d.]+) s this run's own clean build took", line)
    assert m, line
    passes, basis, spent, unit, build_s = (int(m.group(1)), m.group(2),
                                           float(m.group(3)), m.group(4),
                                           float(m.group(5)))
    assert 1 <= passes <= N, passes
    assert build_s > 0, "the build was timed, not assumed"
    scale = {"s": 1.0, "min": 60.0, "h": 3600.0}[unit]
    # Both numbers are ROUNDED for printing, and independently: at these sizes
    # a build of 0.0015 s prints 0.002 and its double prints 0.003. The
    # tolerance is the rounding, not a fudge -- one unit on the total plus one
    # per pass on the build.
    tol = 0.0005 * (passes + 1) * max(1.0, scale / 60.0)
    assert spent * scale == pytest.approx(passes * build_s, abs=tol, rel=0.05)
    assert ("reach" in basis or "model's floor" in basis), basis
    assert "and more than that" in line, (
        "a floor presented as an estimate: a pass corrupts and compares too")


def test_the_COST_is_absent_where_there_is_nothing_to_price(work, capsys):
    """The negative control. A complete run has no remedy to print, and a run
    that found something is not told to re-run for a silence."""
    _run(work, "leaky")
    out = capsys.readouterr().out
    assert "FOR THIS DATA" not in out


# --------------------------------------------------------------------------
# (6) the table reconciles with the findings above it
# --------------------------------------------------------------------------

def test_the_TABLE_accounts_for_a_FINDING_in_a_HEAD_cohort(work, capsys):
    _run(work, "leaky")
    out = capsys.readouterr().out
    n_findings = int(re.search(r"(\d+) finding\(s\) over", out).group(1))
    probed = int(re.search(r"L3.1 cohorts\s+(\d+) \(", out).group(1))
    head_probed = 0
    m = re.search(r"of those ineligible head cohorts, (\d+) W", out)
    if m:
        head_probed = int(m.group(1))
        assert "finding cohort(s) sit over %d probed cohort(s)" % (
            probed + head_probed) in out, out[-2500:]
    finding_cohorts = len(set(re.findall(
        r"moved when (\d{4}-\d\d-\d\dT\S+) was perturbed", out)))
    assert finding_cohorts <= probed + head_probed, (
        "the table says fewer cohorts were probed than the run listed "
        "findings for: %d findings over %d + %d probed"
        % (finding_cohorts, probed, head_probed))
    assert n_findings >= finding_cohorts >= 1


def test_VERIFY_REFUSES_a_table_that_cannot_hold_its_findings():
    """The known positive for the invariant, constructed."""
    cov = Coverage(cohorts_probed=1, cohorts_unprobed=0, cohorts_ineligible=1,
                   rows_probed=1, rows_unprobed=0, rows_ineligible=1,
                   cohorts_head=1, rows_head=1, cohorts_head_probed=0,
                   findings_listed=2)
    with pytest.raises(ValueError, match="does not describe the result"):
        cov.verify(2, 2)
    # And it accepts the same table once the head cohort it probed is counted.
    ok = Coverage(cohorts_probed=1, cohorts_unprobed=0, cohorts_ineligible=1,
                  rows_probed=1, rows_unprobed=0, rows_ineligible=1,
                  cohorts_head=1, rows_head=1, cohorts_head_probed=1,
                  findings_listed=2)
    ok.verify(2, 2)
    assert "sit over 2 probed cohort(s)" in ok.table()


# --------------------------------------------------------------------------
# (8) where the template is
# --------------------------------------------------------------------------

def test_SCHEMA_says_WHERE_the_installed_template_is(capsys):
    assert str(mf.TEMPLATE_PATH) in mf.SCHEMA_DOC
    assert cli.main(["schema"]) == 0
    out = capsys.readouterr().out
    assert str(mf.TEMPLATE_PATH) in out, "the path a user would pass to --profile"
    assert "which is a path you can pass straight to --profile" in out
