"""P0 — the entry point stops lying. R200.

FOUR DEFECTS, EACH WITH THE KNOWN POSITIVE THAT SHOWS ITS CHECK FIRES.

  1. Five parameters were accepted and discarded. A caller who supplied an
     availability model got a Layer 1 dependency map and no availability
     verdict, silently. For a tool whose product is a silence that is the worst
     available failure, because the caller acts on a silence that was never a
     probe.
  2. A frame in `raw` and absent from the model was neither probed nor
     mentioned, reporting `none` as though it were `observed_silence`.
  3. `resolve_decision_time` existed and nothing called it, so a reader of the
     source believed validation happened where it did not.
  4. The package's prose cited module paths that do not exist.

THE CITATION CHECK'S KNOWN POSITIVE WAS ALREADY IN THE TREE, which is the
cheapest kind there is: run before the fixes, it found THREE, two of them live
and unknown. Its negative control is the package after the fixes. Both are here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src"), str(Path(__file__).resolve().parent)):
    if p not in sys.path:
        sys.path.insert(0, p)

import citations                                                  # noqa: E402
from leakaudit import Alignment, audit, resolve_decision_time      # noqa: E402
from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402
from leakaudit.identity_control import run_identity_control        # noqa: E402
from protocol.runtime_reference import FailureReason               # noqa: E402

PKG = ROOT / "src" / "leakaudit"


def _raw():
    rng = np.random.default_rng(0)
    return pd.DataFrame({"a": rng.standard_normal(60),
                         "b": rng.standard_normal(60)})


def _build(d):
    out = pd.DataFrame(index=d.index)
    out["reads_a"] = d["a"].rolling(3, min_periods=1).mean()
    return out


# ---------------------------------------------------------------------------
# 1. The five discarded parameters
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("kw", [
    {"availability": {"frame": "key"}},
    {"decision_time": "timestamp"},
    {"meta": {"anything": 1}},
])
def test_an_unwired_parameter_is_refused_not_discarded(kw):
    with pytest.raises(NotImplementedError) as e:
        audit(_raw(), _build, **kw)
    name = next(iter(kw))
    assert name in str(e.value)
    assert "does not consume" in str(e.value)


def test_a_parameter_whose_consumer_arrived_no_longer_refuses():
    """R203 P4. `train_idx` and `test_idx` left the refusal table when the
    checks that read them landed. A refusal that is no longer true is the same
    defect as a discarded parameter, pointing the other way."""
    from leakaudit.contract import _UNWIRED
    assert "train_idx" not in _UNWIRED and "test_idx" not in _UNWIRED
    r = audit(_raw(), _build, train_idx=[0, 1, 2], test_idx=[3, 4])
    by_name = {c.check: c for c in r.checks}
    assert by_name["split_validity"].looked, "the split was accepted and ignored"
    assert by_name["duplicate_rows_across_split"].looked


def test_the_refusal_names_what_does_consume_an_availability_model():
    """A refusal that is only a wall leaves the caller nowhere. This one points."""
    with pytest.raises(NotImplementedError) as e:
        audit(_raw(), _build, availability={"f": "k"})
    assert "run_probe_a" in str(e.value)


def test_the_refusal_says_why_ignoring_would_have_been_worse():
    with pytest.raises(NotImplementedError) as e:
        audit(_raw(), _build, meta={"x": 1})
    assert "looks clean and is not" in str(e.value)


def test_several_at_once_are_all_named():
    with pytest.raises(NotImplementedError) as e:
        audit(_raw(), _build, availability={"f": "k"}, meta={"x": 1})
    msg = str(e.value)
    assert "availability" in msg and "meta" in msg


def test_the_two_argument_surface_still_works():
    """The negative control. A refusal that also broke the good path would be a
    worse tool, not a more honest one."""
    result = audit(_raw(), _build)
    assert {f.feature for f in result.findings} == {"reads_a"}


def test_explicit_none_is_not_a_refusal():
    assert audit(_raw(), _build, availability=None, meta=None).findings


# ---------------------------------------------------------------------------
# 2. The undeclared frame's silence
# ---------------------------------------------------------------------------

def _agg_frames():
    secs = pd.date_range("2026-01-01", periods=120, freq="1s")
    rng = np.random.default_rng(1)
    agg = pd.DataFrame({"ts_floor": secs, "v": rng.standard_normal(120)})
    other = pd.DataFrame({"ts_floor": secs, "w": rng.standard_normal(120)})
    stamps = [s + pd.Timedelta(milliseconds=300) for s in secs]
    snap = pd.DataFrame({"timestamp": stamps})
    return {"snap": snap, "agg": agg, "other": other}


def _agg_build(raw):
    out = raw["snap"].copy()
    out["ts_floor"] = pd.to_datetime(out["timestamp"]).dt.floor("s")
    out["f"] = out["ts_floor"].map(raw["agg"].set_index("ts_floor")["v"]).to_numpy()
    out["g"] = out["ts_floor"].map(raw["other"].set_index("ts_floor")["w"]).to_numpy()
    return out[["timestamp", "f", "g"]]


MODEL = AvailabilityModel(aggregate_frames={"agg": "ts_floor"},
                          decision_column="timestamp")


def test_an_undeclared_frame_is_named_as_not_probed():
    """KNOWN POSITIVE. `other` feeds column g and the model does not describe
    it, so g cannot move whatever the pipeline does. Before this, nothing said
    so and the silence read as `observed_silence`."""
    res = run_probe_a(_agg_frames(), _agg_build, MODEL, side="s",
                      cohort_stride=7, max_cohorts=12)
    assert "other" in res.unmodelled_frames
    assert "snap" in res.unmodelled_frames
    joined = " ".join(res.notes)
    assert "NOT PROBED" in joined and "other" in joined
    assert "did not happen" in joined


def test_a_fully_declared_run_names_nothing_as_unprobed():
    """The negative control: with every frame described, the note is absent."""
    model = AvailabilityModel(
        aggregate_frames={"agg": "ts_floor", "other": "ts_floor",
                          "snap": "timestamp"},
        decision_column="timestamp")
    res = run_probe_a(_agg_frames(), _agg_build, model, side="s",
                      cohort_stride=7, max_cohorts=12)
    assert res.unmodelled_frames == ()
    assert not any("NOT PROBED" in n for n in res.notes)


def test_the_identity_control_says_the_same_thing():
    res = run_identity_control(_agg_frames(), _agg_build, MODEL, side="s",
                               cohort_stride=7, max_cohorts=12)
    joined = " ".join(res.notes)
    assert "NOT WRITTEN" in joined and "other" in joined


# ---------------------------------------------------------------------------
# 3. The validator that nothing called
# ---------------------------------------------------------------------------

def test_the_validator_is_reachable_from_the_package_root():
    """It is public now rather than internal-and-uncalled. `audit()` refuses
    `decision_time` outright, so no reader can believe `audit()` validates it."""
    built = _build(_raw())
    series, al = resolve_decision_time(built, "not_a_column")
    assert series is None and al.ok is False
    assert al.reason is FailureReason.ALIGNMENT
    assert isinstance(Alignment(True), Alignment)


# ---------------------------------------------------------------------------
# 4. The citations
# ---------------------------------------------------------------------------

def test_every_citation_in_the_package_resolves():
    """The negative control for the check, and the assertion that the three it
    found are fixed."""
    checked = citations.assert_citations_resolve(PKG)
    assert checked >= 3, "a scan that checked almost nothing proves almost nothing"


def test_the_check_fires_on_a_dead_citation(tmp_path):
    """KNOWN POSITIVE, synthetic. The real one is recorded in the docstring:
    run before the fixes, this check found three."""
    (tmp_path / "m.py").write_text(
        '"""Cites `leakaudit.trace.gate_inputs_only`, which is not there."""\n',
        encoding="utf-8")
    with pytest.raises(citations.DeadCitation) as e:
        citations.assert_citations_resolve(tmp_path)
    assert "gate_inputs_only" in str(e.value)


def test_a_live_citation_does_not_fire(tmp_path):
    (tmp_path / "m.py").write_text(
        '"""Cites `leakaudit.probe.probe_columns`, which exists."""\n',
        encoding="utf-8")
    assert citations.assert_citations_resolve(tmp_path) == 1


def test_a_recorded_dead_citation_is_exempt_and_reported(tmp_path):
    """Quoting a citation as historically wrong keeps a correction on the
    record. The exemption is narrow -- it needs the marker -- and every exempt
    line is reported rather than silently skipped."""
    (tmp_path / "m.py").write_text(
        '"""Once cited `leakaudit.trace.gone`.  %s"""\n' % citations.MARKER,
        encoding="utf-8")
    dead, exempt, checked = citations.scan(tmp_path)
    assert dead == [] and checked == 0
    assert len(exempt) == 1 and exempt[0]["cites"] == "leakaudit.trace.gone"


def test_an_unmarked_historical_citation_still_fires(tmp_path):
    """The pair to the test above: without the marker, prose that merely reads
    as historical is still a live claim."""
    (tmp_path / "m.py").write_text(
        '"""This used to cite `leakaudit.trace.gone`."""\n', encoding="utf-8")
    with pytest.raises(citations.DeadCitation):
        citations.assert_citations_resolve(tmp_path)


def test_an_empty_population_raises_rather_than_passing(tmp_path):
    with pytest.raises(citations.DeadCitation, match="empty population"):
        citations.assert_citations_resolve(tmp_path)


def test_every_citation_inside_a_refusal_message_resolves():
    """R201 §1's condition. The refusals cite module paths, which are exactly
    what the citation check polices -- so a refusal cannot become the next dead
    citation. Read from the dict at RUN TIME rather than from the source, so a
    message composed rather than written literally is still covered."""
    from leakaudit.contract import _UNWIRED
    assert _UNWIRED, "a check over an empty registry proves nothing"
    seen = 0
    for name, message in _UNWIRED.items():
        for m in citations._CITATION.finditer(message):
            seen += 1
            assert citations._resolves(m.group(1)), (
                "the refusal for %r cites `%s`, which does not resolve"
                % (name, m.group(1)))
    assert seen >= 2, "no refusal cited anything; this check would pass vacuously"
