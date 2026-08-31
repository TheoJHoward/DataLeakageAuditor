"""The affected output cohort names the output that MOVED, not the cohort probed.

`PREREG.md` line 291 registers the runtime scoring unit as the feature and the
affected output cohort; §7.2 keeps probe cohorts separate from it, as
corroborating evidence rather than part of the key. `FindingRecord` declares
three fields for that reason.

Until R184 the probe wrote the probed cohort's identifier into both the
probe-cohort field and the affected-output field, so every finding reported the
column it had perturbed and never the column that moved. The unit the whole
scoring apparatus is keyed on carried no information, and nothing failed,
because two fields agreeing looks exactly like two fields being filled.

THE FIXTURE HERE IS SYNTHETIC, DELIBERATELY. The instrument's own domain is the
acceptance fixture, and a test drawn from it would exercise the same builder the
probe is being checked against. A three-column frame with a build whose
dependencies are known by construction lets the expected answer be written down
before the probe runs, which is what makes the positive a positive.
"""
from __future__ import annotations

import pandas as pd
import pytest

from leakaudit.probe import output_cohort_id, output_column_of, probe_columns

READS = "reads_a"      # output built from src.a -- perturbing a MUST move it
IGNORES = "ignores_b"  # output built from src.c -- perturbing b must move nothing


def _frames():
    return {"src": pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                                 "b": [9.0, 8.0, 7.0, 6.0, 5.0, 4.0],
                                 "c": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0]})}


def _build(frames):
    """Deterministic, and its dependency structure is the test's ground truth:
    the first output reads `a` and nothing else; the second reads `c`."""
    src = frames["src"]
    return pd.DataFrame({READS: src["a"] * 2.0,
                         IGNORES: src["c"] + 1.0})


def _findings(result):
    out = []
    for trace in (result.preserving, result.promoted):
        for r in trace.records:
            if r.finding is not None:
                out.append(r.finding)
    return out


def test_known_positive_the_field_carries_the_moved_output():
    """Perturbing `a` moves `reads_a`; the field must say so."""
    result = probe_columns(_frames(), _build, case_id="synthetic")
    hits = [f for f in _findings(result) if f.probe_cohort == "col:src.a"]
    assert hits, "probing a column the build reads produced no finding at all"

    for f in hits:
        assert f.feature == READS, (
            "the moved output should be %r, got %r" % (READS, f.feature))
        assert f.affected_output_cohort == "col:out.%s" % READS, (
            "affected_output_cohort is %r; expected the MOVED OUTPUT's cohort"
            % f.affected_output_cohort)
        assert f.affected_output_cohort != f.probe_cohort, (
            "affected_output_cohort still duplicates probe_cohort (%r) -- this "
            "is the defect the repair removes, and it is invisible unless the "
            "two are compared" % f.probe_cohort)


def test_known_positive_a_second_column_routes_to_its_own_output():
    """`c` feeds `ignores_b` only, so its findings name that output and not the
    other. One route firing correctly does not show the field is derived from
    the moved output rather than fixed to a constant."""
    result = probe_columns(_frames(), _build, case_id="synthetic")
    hits = [f for f in _findings(result) if f.probe_cohort == "col:src.c"]
    assert hits, "probing `c` produced no finding, so this route proves nothing"
    for f in hits:
        assert f.feature == IGNORES
        assert f.affected_output_cohort == "col:out.%s" % IGNORES


def test_negative_control_a_probe_that_moves_nothing_emits_no_finding():
    """Without this the positives above would be satisfied by a check that
    fires on everything. `b` is read by no output."""
    result = probe_columns(_frames(), _build, case_id="synthetic")
    hits = [f for f in _findings(result) if f.probe_cohort == "col:src.b"]
    assert not hits, (
        "perturbing a column no output reads produced %d finding(s): %r"
        % (len(hits), [(f.feature, f.affected_output_cohort) for f in hits]))


def test_the_probed_cohort_is_still_recorded_as_corroboration():
    """§7.2 keeps probe cohorts as corroborating evidence. The repair moves the
    affected-output field off the probe cohort; it does not discard the probe
    cohort, and a repair that lost it would trade one empty field for another."""
    result = probe_columns(_frames(), _build, case_id="synthetic")
    hits = _findings(result)
    assert hits
    assert all(f.probe_cohort.startswith("col:src.") for f in hits), (
        "probe_cohort no longer names the probed input column")


# ---------------------------------------------------------------------------
# The identifier's form: a collision guard, and the one sanctioned inverse.
# ---------------------------------------------------------------------------

def test_an_input_frame_named_out_is_refused():
    """The output frame's name is a free choice, so nothing stops a caller
    choosing it too. Both would print as `col:out.<column>` and no consumer
    could tell a probed input from a moved output -- a silent collision, which
    is the kind this project stops by making the path unavailable rather than by
    noticing it later."""
    frames = _frames()
    frames["out"] = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]})
    with pytest.raises(ValueError) as exc:
        probe_columns(frames, _build, case_id="synthetic")
    assert "col:out." in str(exc.value)


def test_the_matching_rule_round_trips():
    """A harness matching this field back to a column name uses ONE function.
    String surgery repeated at call sites is several chances to disagree about
    the prefix, and the disagreement shows up as a silent non-match."""
    for col in ("net_delta_1s", "trade_volume_1s", "a.b", "x"):
        assert output_column_of(output_cohort_id(col)) == col


def test_the_matching_rule_refuses_a_probe_cohort():
    """Passing a probe cohort by mistake returns nothing, not a plausible wrong
    column. `col:src.a` is a real cohort id of the other kind."""
    assert output_column_of("col:src.a") is None
    assert output_column_of("not-a-cohort-id") is None


def test_the_field_the_probe_emits_is_readable_by_that_rule():
    """The two halves have to agree: the id the probe writes is the id the
    inverse reads. Testing them separately would let them drift apart."""
    result = probe_columns(_frames(), _build, case_id="synthetic")
    hits = [f for f in _findings(result) if f.probe_cohort == "col:src.a"]
    assert hits
    for f in hits:
        assert output_column_of(f.affected_output_cohort) == f.feature, (
            "the inverse does not recover the feature the probe recorded")
