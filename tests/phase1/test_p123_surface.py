"""P1-P3 — the findings view, the exported probe, and the one command. R201.

THE CASE THAT MATTERS MOST IS `test_a_timezone_mismatch_raises_rather_than_
matching_nothing`. The eligibility derivation lived in two test harnesses and
was reimplemented in a third form inside the identity control. Its timezone
rule, got wrong, produces an all-False mask that looks exactly like "no cells
were unavailable" — a silent wrong answer in the direction that hides findings,
in a function strangers never read. It now raises, and the raise is tested.

The findings view's constraint is tested as a property rather than described:
it stores nothing, so mutating the traces it wraps changes what it reports.
A cache would not.
"""
from __future__ import annotations

import contextlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import leakaudit                                                   # noqa: E402
from leakaudit import (                                            # noqa: E402
    AuditResult, AvailabilityModel, ProbeError, align_key, audit,
    eligible_cohorts, run_probe_a)
from leakaudit.cli import main as cli_main                         # noqa: E402


def _raw():
    rng = np.random.default_rng(0)
    return pd.DataFrame({"a": rng.standard_normal(40),
                         "b": rng.standard_normal(40)})


def _build(d):
    return pd.DataFrame({"reads_a": d["a"].rolling(3, min_periods=1).mean()},
                        index=d.index)


def _silent_build(d):
    return pd.DataFrame({"constant": np.ones(len(d))}, index=d.index)


# ---------------------------------------------------------------------------
# P1 — the findings view
# ---------------------------------------------------------------------------

def test_findings_are_reachable_without_importing_protocol():
    r = audit(_raw(), _build)
    assert isinstance(r, AuditResult)
    assert {f.feature for f in r.findings} == {"reads_a"}
    assert all(f.probe_cohorts for f in r.findings)


def test_one_finding_per_registered_unit_not_one_per_strategy():
    """Two preserving strategies corroborate one pair; the registration counts
    that as ONE event. Deriving from records printed it twice -- a count of the
    schedule rather than of what was found, caught by running the command."""
    r = audit(_raw(), _build)
    assert len(r.findings) == 1
    assert len(r.findings[0].strategies) >= 2
    assert "corroborated by" in str(r.findings[0])


def test_the_view_stores_nothing_and_therefore_cannot_drift():
    """THE CONSTRAINT, TESTED AS A PROPERTY. A cache would answer the same
    twice; a view answers what the traces now say."""
    r = audit(_raw(), _build)
    first = len(r.findings)
    trimmed = [t.__class__(**{**t.__dict__, "records": ()}) for t in r.traces]
    assert len(AuditResult(trimmed).findings) == 0
    assert len(r.findings) == first, "the original view was mutated by the copy"


def test_two_accesses_recompute_rather_than_return_the_same_object():
    r = audit(_raw(), _build)
    assert r.findings == r.findings          # equal by value
    assert r.findings is not r.findings      # and not one stored list


def test_a_finding_result_says_so():
    r = audit(_raw(), _build)
    assert r.outcome == "finding"
    assert "finding(s) over" in r.explain()


def test_an_empty_result_says_it_is_OBSERVED_SILENCE_when_probes_ran():
    r = audit(_raw(), _silent_build)
    assert r.findings == []
    assert r.outcome == "observed_silence"
    assert "OBSERVED SILENCE" in r.explain()
    assert "This is evidence." in r.explain()


def test_an_empty_result_distinguishes_none_from_observed_silence():
    """KNOWN POSITIVE for the definition of done's last clause. A probe that did
    not happen must not read as a probe that found nothing."""
    r = audit(_raw(), _silent_build)
    empty = [t.__class__(**{**t.__dict__, "records": (),
                            "selected_eligible_cohorts": (),
                            "resolved_strategies": ()}) for t in r.traces]
    none_result = AuditResult(empty)
    assert none_result.outcome == "none"
    text = none_result.explain()
    assert "NOT EVIDENCE OF ABSENCE" in text
    assert "no probe ran" in text


def test_the_per_combination_outcomes_stay_available():
    """The registered outcome is per combination; the single value is a display
    projection and must not replace it."""
    r = audit(_raw(), _build)
    assert set(r.per_combination) == {"preserving", "promoted"}


def test_str_is_a_projection_that_reads_the_same_traces():
    r = audit(_raw(), _build)
    text = str(r)
    assert r.outcome in text
    for f in r.findings:
        assert f.feature in text


def test_a_view_over_no_traces_is_refused():
    with pytest.raises(ValueError, match="which kind"):
        AuditResult([])


# ---------------------------------------------------------------------------
# P2 — the availability probe in the public surface
# ---------------------------------------------------------------------------

def test_the_availability_probe_is_exported():
    for name in ("AvailabilityModel", "run_probe_a", "eligible_cohorts",
                 "align_key", "traces_for", "run_identity_control"):
        assert name in leakaudit.__all__, "%s is not in the public surface" % name
        assert hasattr(leakaudit, name)


def _agg(tz=None):
    secs = pd.date_range("2026-01-01", periods=60, freq="1s", tz=tz)
    return pd.DataFrame({"ts_floor": secs, "v": np.arange(60.0)})


def _decision(tz=None):
    secs = pd.date_range("2026-01-01", periods=60, freq="1s", tz=tz)
    return pd.Series([s + pd.Timedelta(milliseconds=300) for s in secs])


MODEL = AvailabilityModel(aggregate_frames={"agg": "ts_floor"},
                          decision_column="timestamp")


def test_a_timezone_mismatch_raises_rather_than_matching_nothing():
    """THE CASE THIS EXTRACTION EXISTS FOR. Aware against naive matches nothing,
    and nothing is indistinguishable from a frame carrying no row in any
    selected second. That silence would be reported as a probed pipeline."""
    d = _decision(tz=None)
    with pytest.raises(ProbeError) as e:
        eligible_cohorts({"agg": _agg(tz="UTC")}, MODEL,
                         list(d.dt.floor("s").unique()), d)
    msg = str(e.value)
    assert "matches NOTHING" in msg
    assert "indistinguishable" in msg
    assert "cannot be guessed" in msg


def test_the_mismatch_raises_in_the_other_direction_too():
    d = _decision(tz="UTC")
    with pytest.raises(ProbeError):
        eligible_cohorts({"agg": _agg(tz=None)}, MODEL,
                         list(d.dt.floor("s").unique()), d)


@pytest.mark.parametrize("tz", [None, "UTC"])
def test_matching_zones_align_and_every_second_is_eligible(tz):
    """The negative control. A rule that raised on everything would also never
    produce a silent wrong answer, and would be useless."""
    d = _decision(tz=tz)
    picked = list(d.dt.floor("s").unique())
    res = eligible_cohorts({"agg": _agg(tz=tz)}, MODEL, picked, d)
    assert len(res.eligible) == len(picked)
    assert res.ineligible == ()
    assert res.per_frame["agg"] == len(picked)


def test_differing_zones_on_both_sides_convert_rather_than_raise():
    """Both aware is comparable; only the mixed case is not derivable."""
    d = _decision(tz="UTC")
    agg = _agg(tz="UTC")
    agg["ts_floor"] = agg["ts_floor"].dt.tz_convert("America/New_York")
    picked = list(d.dt.floor("s").unique())
    assert len(eligible_cohorts({"agg": agg}, MODEL, picked, d).eligible) == len(picked)


def test_a_second_no_frame_carries_is_ineligible_and_said_so():
    d = _decision()
    picked = list(d.dt.floor("s").unique()) + [pd.Timestamp("2030-01-01")]
    res = eligible_cohorts({"agg": _agg()}, MODEL, picked, d)
    assert pd.Timestamp("2030-01-01") in res.ineligible


def test_no_eligible_second_at_all_is_reported_not_returned_bare():
    d = _decision()
    far = [pd.Timestamp("2030-01-01"), pd.Timestamp("2030-01-02")]
    res = eligible_cohorts({"agg": _agg()}, MODEL, far, d)
    assert res.eligible == ()
    assert any("would probe nothing" in n for n in res.notes)


def test_align_key_is_reachable_and_names_the_frame_it_refuses():
    with pytest.raises(ProbeError, match="frame 'trades' column 'ts_event'"):
        align_key(_agg(tz="UTC")["ts_floor"], _decision(tz=None),
                  frame="trades", column="ts_event")


# ---------------------------------------------------------------------------
# P3 — one command
# ---------------------------------------------------------------------------

def _write_pipeline(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "userpipe.py"
    p.write_text(body, encoding="utf-8")
    return p


PIPE_LEAKY = """
import pandas as pd
def build(frames):
    d = frames["raw"]
    return pd.DataFrame({"reads_a": d["a"].rolling(3, min_periods=1).mean()},
                        index=d.index)
"""

PIPE_SILENT = """
import pandas as pd, numpy as np
def build(frames):
    d = frames["raw"]
    return pd.DataFrame({"constant": np.ones(len(d))}, index=d.index)
"""


def _run_cli(tmp_path, pipeline_body, extra=()):
    _write_pipeline(tmp_path, pipeline_body)
    df = pd.DataFrame({"a": np.arange(30.0), "b": np.arange(30.0)})
    csv = tmp_path / "data.csv"
    df.to_csv(csv, index=False)
    env_path = str(tmp_path)
    argv = ["run", "--pipeline", "userpipe:build",
            "--frame", "raw=%s" % csv, *extra]
    sys.path.insert(0, env_path)
    try:
        return cli_main(argv)
    finally:
        sys.path.remove(env_path)
        sys.modules.pop("userpipe", None)


def test_the_command_finds_a_leak_and_exits_one(tmp_path, capsys):
    code = _run_cli(tmp_path, PIPE_LEAKY)
    out = capsys.readouterr().out
    assert code == 1
    assert "reads_a" in out


def test_the_command_reports_observed_silence_and_exits_zero(tmp_path, capsys):
    code = _run_cli(tmp_path, PIPE_SILENT)
    out = capsys.readouterr().out
    assert code == 0
    assert "OBSERVED SILENCE" in out
    assert "This is evidence." in out


def test_the_exit_status_distinguishes_the_two_silences():
    """A script reading only the status is the reader who cannot see the prose,
    so the two silences are different statuses, not one."""
    from leakaudit import cli
    assert cli.EXIT_OK_SILENT != cli.EXIT_NOTHING_PROBED


@contextlib.contextmanager
def _importable(tmp_path):
    _write_pipeline(tmp_path, PIPE_LEAKY)
    sys.path.insert(0, str(tmp_path))
    try:
        yield
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop("userpipe", None)


def test_a_missing_frame_file_is_refused_not_skipped(tmp_path):
    with _importable(tmp_path), pytest.raises(SystemExit, match="no such file"):
        cli_main(["run", "--pipeline", "userpipe:build",
                  "--frame", "raw=%s" % (tmp_path / "absent.csv")])


def test_an_unreadable_extension_is_refused_not_skipped(tmp_path):
    bad = tmp_path / "data.xlsx"
    bad.write_text("not really", encoding="utf-8")
    with _importable(tmp_path), pytest.raises(SystemExit) as e:
        cli_main(["run", "--pipeline", "userpipe:build",
                  "--frame", "raw=%s" % bad])
    assert "skipping it would probe less than you asked" in str(e.value)


def test_a_pipeline_spec_without_a_function_is_refused(tmp_path):
    with pytest.raises(SystemExit, match="names no function"):
        cli_main(["run", "--pipeline", "userpipe", "--frame", "raw=x.csv"])


def test_no_frames_is_refused(tmp_path):
    with _importable(tmp_path), pytest.raises(SystemExit,
                                              match="nothing to probe"):
        cli_main(["run", "--pipeline", "userpipe:build"])


def test_the_console_script_is_declared():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "[project.scripts]" in text
    assert "leakaudit = \"leakaudit.cli:main\"" in text
