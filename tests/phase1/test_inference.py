"""Inference proposes; it never picks. R232 §5, spec at R215 §3.

**THE DESIGN IN ONE SENTENCE: infer what is IN the data; require what is ABOUT
the world.** Structure is a shape in the frames and is determined. Availability is
a fact about how the data was published and is not in the frames at all, so it is
left blank with the observable evidence beside it.

**THE KNOWN POSITIVE, AND IT DISCRIMINATES.** A frame where structure IS
determinable and availability is NOT: `test_the_known_positive_...` below builds
one, confirms the draft fills the first and leaves the second blank, and — this is
the discriminating half — confirms that **a wrong inference would fill both**. A
draft that filled availability would pass a test that only checked the structure
half, which is exactly the wiring-versus-validity distinction R215 §0 refined.

**EVERY SIGNAL SHIPS WITH ITS WRONG CASE**, from `PRE_BUILD_READS.md` §1's seven.
Each wrong case is a test here, and each asserts the module does NOT answer
confidently on it. That is the reverse of a normal test: what is asserted is the
absence of a conclusion, because a signal that produces a confident answer on its
own wrong case is a signal nobody understands yet.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.inference import (                                # noqa: E402
    HEADER, SIGNALS_OMITTED, SIGNALS_USED, Draft, UnfilledAvailability, accept,
    draft, render_draft)

SECS = pd.date_range("2026-04-01 08:00:00", periods=60, freq="1s")


def _rng():
    return np.random.default_rng(11)


# ---------------------------------------------------------------------------
# THE KNOWN POSITIVE, and the negative that makes it discriminating.
# ---------------------------------------------------------------------------

def test_the_known_positive_structure_filled_availability_blank():
    """Structure determinable, availability not. The draft must fill exactly one
    of the two."""
    rng = _rng()
    frames = {"scans": pd.DataFrame({"scanned_at": SECS,
                                     "items": rng.integers(0, 200, 60)})}
    d = draft(frames)
    assert d.forks["scans"].datetime_columns == ["scanned_at"], (
        "the datetime column IS observable here and was not observed")
    assert d.forks["scans"].mode_is_unfilled, (
        "a mode was assigned. `aggregate_frames` is availability, not structure")
    for cd in d.columns:
        assert cd.availability_is_unfilled, (
            "%s.%s has an availability VALUE. Nothing in the frames carries "
            "when a value became knowable." % (cd.frame, cd.column))


def test_NO_column_anywhere_receives_an_availability_value():
    """The discriminating half. A wrong inference fills both halves, and a test
    that only checked structure would pass it."""
    rng = _rng()
    frames = {
        "a": pd.DataFrame({"ts": SECS, "x": rng.standard_normal(60)}),
        "b": pd.DataFrame({"k": SECS + pd.Timedelta(milliseconds=400),
                           "y": rng.integers(0, 9, 60)}),
    }
    d = draft(frames)
    assert d.forks, "the frames were not observed at all"
    assert all(f.mode_is_unfilled for f in d.forks.values()), (
        "a frame received an availability mode: %s"
        % [f.frame for f in d.forks.values() if not f.mode_is_unfilled])
    filled = [(c.frame, c.column, c.availability)
              for c in d.columns if not c.availability_is_unfilled]
    assert not filled, "availability was inferred for %s" % (filled,)


def test_the_evidence_is_offered_WITHOUT_a_conclusion():
    """The evidence must help the user answer, not answer for them."""
    d = draft({"scans": pd.DataFrame({"scanned_at": SECS, "n": range(60)})})
    ts = [c for c in d.columns if c.column == "scanned_at"][0]
    assert ts.availability_evidence, "no evidence was offered at all"
    joined = " ".join(ts.availability_evidence)
    assert "only you know which" in joined or "not" in joined
    for banned in ("therefore", "so the availability is", "we conclude"):
        assert banned not in joined.lower(), joined


# ---------------------------------------------------------------------------
# THE SEVEN WRONG CASES. Each asserts the ABSENCE of a confident answer.
# ---------------------------------------------------------------------------

def test_S1_wrong_case__a_future_instant_whose_NAME_looks_like_a_release():
    """`expiry_at` matches every naming heuristic and holds a FUTURE instant.
    Inferring `at_source_timestamp` on it puts availability after every decision
    and reports every feature reading it as leaking."""
    d = draft({"contracts": pd.DataFrame(
        {"expiry_at": SECS + pd.Timedelta(days=365), "v": range(60)})})
    col = [c for c in d.columns if c.column == "expiry_at"][0]
    assert col.availability_is_unfilled
    assert "S1" in SIGNALS_OMITTED
    assert not any("release" in e.lower() or "source" in e.lower()
                   for e in col.availability_evidence), (
        "the draft reasoned from the column's NAME: %s" % col.availability_evidence)


def test_S1b_wrong_case__birth_date_fails_the_same_way_in_reverse():
    d = draft({"people": pd.DataFrame(
        {"birth_date": SECS - pd.Timedelta(days=10_000), "v": range(60)})})
    assert all(c.availability_is_unfilled for c in d.columns)


def test_S2_wrong_case__a_1Hz_lattice_is_INDISTINGUISHABLE_from_an_aggregate():
    """The decisive one. Every stamp on an exact second, and no row is an
    aggregate: each is an instantaneous reading knowable AT its stamp, not at
    stamp + 1s. An aggregate over [t, t+1s) has an identical key column, and the
    difference between the two readings is a full second of availability."""
    d = draft({"sensor": pd.DataFrame({"t": SECS, "reading": range(60)})})
    col = [c for c in d.columns if c.column == "t"][0]
    assert col.availability_is_unfilled, (
        "a 100%-on-boundary key column produced an availability value; that is "
        "S2's wrong case shipping as a feature")
    joined = " ".join(col.availability_evidence)
    assert "100.00%" in joined, "the observable was not reported: %s" % joined
    assert "IDENTICAL in both cases" in joined, (
        "the fraction is reported without the fact that it cannot distinguish "
        "the two readings, which is the whole of S2's wrong case: %s" % joined)


def test_S3_wrong_case__two_monotone_clocks_and_no_basis_to_choose():
    """The fixture's own trades frame carries `ts_recv` AND `ts_event`, both
    monotone, both plausible. Monotonicity cannot even rank them, and choosing
    infers a pipeline that may not exist."""
    d = draft({"trades": pd.DataFrame({
        "ts_recv": SECS, "ts_event": SECS - pd.Timedelta(milliseconds=5),
        "px": range(60)})})
    assert d.forks["trades"].mode_is_unfilled, (
        "a key was chosen between two equally monotone datetime columns")
    assert sorted(d.forks["trades"].datetime_columns) == ["ts_event", "ts_recv"]
    why = " ".join(w for _f, _c, w in d.unresolved)
    assert "no basis to choose" in why, why
    assert "ts_recv" in str(d.unresolved) and "ts_event" in str(d.unresolved)


def test_S4_and_S5_wrong_case__constant_in_the_window_is_not_constant():
    """`tick_size` is genuinely static; a quarterly-revised value sampled inside
    one quarter looks identical. Proposing `always` reads an accident of the
    sampling window as a property of the world."""
    d = draft({"cfg": pd.DataFrame({"t": SECS, "tick_size": [0.25] * 60})})
    col = [c for c in d.columns if c.column == "tick_size"][0]
    assert col.availability_is_unfilled
    why = " ".join(w for _f, _c, w in d.unresolved)
    assert "always" in why and "not constant in general" in why, why


def test_S6_wrong_case__the_dependency_map_is_NOT_consulted_at_all():
    """The category error. Which columns are READ is not when they became
    knowable; it can only produce 'read, therefore available' -- the assumption
    of no leak restated as a finding. `draft()` takes frames and nothing else, so
    a dependency map cannot reach it even by accident."""
    import inspect

    from leakaudit import inference
    sig = inspect.signature(draft)
    assert list(sig.parameters) == ["frames"], (
        "draft() accepts something besides the frames: %s" % sig)
    src = inspect.getsource(inference)
    code = "\n".join(ln for ln in src.split("\n")
                     if not ln.strip().startswith("#"))
    body = code.split('"""')[-1]
    for banned in ("probe_columns", "base_columns", "dependency", "audit("):
        assert banned not in body, (
            "the dependency map is reachable from the draft path (%r)" % banned)
    assert "S6" in SIGNALS_OMITTED
    assert "mirror" in SIGNALS_OMITTED["S6"]


def test_S7_wrong_case__a_reference_tables_timestamp_is_its_LOAD_time():
    """Nothing about the row's decision instant, and often far later than the
    fact it records."""
    d = draft({"refdata": pd.DataFrame(
        {"timestamp": SECS, "country_code": ["US"] * 60})})
    col = [c for c in d.columns if c.column == "timestamp"][0]
    assert col.availability_is_unfilled
    assert not any("decision" in e.lower() for e in col.availability_evidence)


# ---------------------------------------------------------------------------
# The audit refuses an unfilled field. It is not a default and not agreement.
# ---------------------------------------------------------------------------

def test_accept_REFUSES_while_any_availability_field_is_blank():
    d = draft({"scans": pd.DataFrame({"scanned_at": SECS, "n": range(60)})})
    with pytest.raises(UnfilledAvailability) as e:
        accept(d, {})
    msg = str(e.value)
    assert "scans.scanned_at (availability)" in msg
    assert "scans (availability mode)" in msg, (
        "the frame-level MODE is not in the refusal, so a user could accept a "
        "draft without ever deciding whether their frame is an aggregate: %s"
        % msg)
    assert "availability model you did not write" in msg


def test_accept_SUCCEEDS_once_the_user_has_answered_BOTH_kinds():
    d = draft({"scans": pd.DataFrame({"scanned_at": SECS, "n": range(60)})})
    model = accept(d, {"scans.scanned_at (availability)": "at_timestamp",
                       "scans (availability mode)": "aggregate:scanned_at"})
    assert model["aggregate_frames"] == {"scans": "scanned_at"}
    assert model["version"] == 3


def test_a_frame_the_user_says_is_NOT_an_aggregate_gets_no_entry():
    """The other half of the fork, and the case the old draft could not express:
    a frame whose timestamp is the decision instant is not an aggregate at all."""
    d = draft({"stations": pd.DataFrame({"timestamp": SECS, "q": range(60)})})
    model = accept(d, {"stations.timestamp (availability)": "at_timestamp",
                       "stations (availability mode)": "decision_frame"})
    assert model["aggregate_frames"] == {}, (
        "the user said this frame carries the decision instant and it was "
        "still declared an aggregate")


def test_a_BLANK_is_not_read_as_agreement_even_if_explicitly_none():
    """The plausible wrong repair: letting the user pass the key with a null to
    mean 'I agree with whatever you inferred'. There is nothing to agree with."""
    d = draft({"scans": pd.DataFrame({"scanned_at": SECS, "n": range(60)})})
    model = accept(d, {"scans.scanned_at (availability)": None,
                       "scans (availability mode)": None})
    assert model["version"] == 3, (
        "an explicit None from the USER is an answer they gave; a blank the "
        "draft left is not. Only the second is refused.")


# ---------------------------------------------------------------------------
# R234 §0 -- the defect, and the station frame is its discriminating case.
# ---------------------------------------------------------------------------

def test_THE_STATION_FRAME_gets_the_fork_and_NOT_a_mode():
    """THE DISCRIMINATING POSITIVE. One datetime column, monotone, on no
    boundary -- and in the live run it carries the DECISION INSTANT, not an
    aggregate. The first draft gave it `aggregate_frames` because that is what a
    lone timestamp looks like. A draft that assigns it any mode fails here."""
    d = draft({"stations": pd.DataFrame({"timestamp": SECS,
                                         "queue_depth": range(60)})})
    fork = d.forks["stations"]
    assert fork.mode_is_unfilled, "a mode was assigned to the station frame"
    assert fork.datetime_columns == ["timestamp"]
    ev = " ".join(fork.evidence)
    assert "THE FORK" in ev
    assert "AGGREGATES an interval" in ev and "DECISION INSTANT" in ev, (
        "the evidence does not name BOTH branches, so it is a hint rather than "
        "a fork: %s" % ev)


def test_NO_frame_anywhere_receives_a_mode_however_suggestive_its_shape():
    """Every shape that previously produced a confident assignment."""
    cases = {
        "one_col_on_boundary": pd.DataFrame({"t": SECS, "v": range(60)}),
        "one_col_off_boundary": pd.DataFrame(
            {"t": SECS + pd.Timedelta(milliseconds=300), "v": range(60)}),
        "two_cols": pd.DataFrame({"a": SECS, "b": SECS, "v": range(60)}),
        "no_datetime": pd.DataFrame({"v": range(60)}),
    }
    d = draft(cases)
    for name, fork in d.forks.items():
        assert fork.mode_is_unfilled, "%s received a mode" % name


def test_the_frame_mode_is_in_the_SAME_unfilled_list_as_the_columns():
    """R234 §0(b): one refusal path, not two. A user meets one list."""
    d = draft({"scans": pd.DataFrame({"scanned_at": SECS, "n": range(60)})})
    fields = d.unfilled_fields
    assert "scans (availability mode)" in fields
    assert "scans.scanned_at (availability)" in fields


def test_the_rendered_draft_shows_the_mode_as_BLANK():
    text = render_draft(draft({"s": pd.DataFrame({"t": SECS, "n": range(60)})}))
    assert "availability mode: <BLANK -- you decide>" in text
    assert "NOT turned into a mode" in text


# ---------------------------------------------------------------------------
# R234 §1 -- the skeleton, generated from the same pass.
# ---------------------------------------------------------------------------

def test_the_written_file_carries_a_column_modes_SKELETON():
    import json
    import tempfile
    from leakaudit.inference import write_draft
    from leakaudit.model_file import FILL_ME

    d = draft({"scans": pd.DataFrame({"scanned_at": SECS, "items": range(60)})})
    out = Path(tempfile.mkdtemp()) / "m.json"
    write_draft(d, out, generated_by="t", commit="c",
                source_frames={"scans": (60, 2)})
    body = json.loads(out.read_text(encoding="utf-8"))
    assert body["column_modes"] == {"scanned_at": FILL_ME}, body.get("column_modes")
    ev = body["draft_provenance"]["column_mode_evidence"]
    assert "scanned_at" in ev and "S2:" in ev["scanned_at"]
    assert "(frame) scans" in ev and "THE FORK" in ev["(frame) scans"]


def test_the_skeleton_is_GENERATED_not_typed_alongside():
    """R234 §1: one source. Every skeleton key must be a column the same pass
    produced evidence for -- a hand-maintained list would drift."""
    import json
    import tempfile
    from leakaudit.inference import write_draft

    frames = {"a": pd.DataFrame({"t": SECS, "x": range(60)}),
              "b": pd.DataFrame({"k": SECS, "y": range(60)})}
    d = draft(frames)
    out = Path(tempfile.mkdtemp()) / "m.json"
    write_draft(d, out, generated_by="t", commit="c",
                source_frames={k: (60, 2) for k in frames})
    body = json.loads(out.read_text(encoding="utf-8"))
    evidenced = {c.column for c in d.columns if c.availability_evidence}
    assert set(body["column_modes"]) == evidenced, (
        "the skeleton and the draft disagree about which columns need a mode")


# ---------------------------------------------------------------------------
# The header sentence is the feature.
# ---------------------------------------------------------------------------

def test_the_HEADER_says_why_half_the_file_is_blank():
    for phrase in ("determined from your data", "not a shape in the frames",
                   "refuse rather than guess"):
        assert phrase in HEADER, phrase


def test_the_rendered_draft_LEADS_with_the_header():
    text = render_draft(draft({"s": pd.DataFrame({"t": SECS, "n": range(60)})}))
    assert text.startswith(HEADER), (
        "the header is not first, so a reader meets a half-filled file before "
        "being told why it is half filled")


def test_the_rendered_draft_names_the_omitted_signals_and_why():
    text = render_draft(draft({"s": pd.DataFrame({"t": SECS, "n": range(60)})}))
    for sig in SIGNALS_OMITTED:
        assert sig in text, "%s is omitted in code and invisible in output" % sig
    assert "mirror" in text, "S6's reason is not in the output a person reads"
    for sig in SIGNALS_USED:
        assert sig in text


def test_an_empty_frame_set_still_produces_a_header_and_no_values():
    d = draft({})
    assert d.notes and d.notes[0] == HEADER
    assert not d.columns and not d.forks and not d.unfilled_fields


def test_a_CSV_LOADED_frame_is_drafted__the_path_the_USER_takes():
    """THE POSITIVE THAT WAS MISSING. Every other test here builds its frames
    with `pd.date_range`, which yields `datetime64`. The CLI loads CSVs, where
    every column arrives as text -- and under pandas 3 a text column's dtype is
    `str`, not `object`. The first version of `_is_datetimeish` asked for
    `object`, so on the real path it reported every timestamp column as
    not-datetime-like and the draft determined NOTHING. Found on the first live
    run through `leakaudit draft`, not by this file.
    """
    data = ROOT / "tests" / "phase1" / "portability_data"
    frames = {"stations": pd.read_csv(data / "stations.csv"),
              "scans": pd.read_csv(data / "scans.csv")}
    assert str(frames["stations"]["timestamp"].dtype) not in ("datetime64[ns]",), (
        "the fixture no longer arrives as text, so this test no longer "
        "exercises the path it exists for")
    d = draft(frames)
    assert sorted(d.forks) == ["scans", "stations"]
    assert d.forks["stations"].datetime_columns == ["timestamp"]
    for fork in d.forks.values():
        assert fork.mode_is_unfilled
    for cd in d.columns:
        assert cd.availability_is_unfilled


def test_a_numeric_column_is_never_read_as_a_timestamp():
    """The discriminating negative for the parse-based test. Integers parse as
    nanosecond epochs if handed to `to_datetime`, so excluding numerics BEFORE
    parsing is what keeps a count column from becoming a clock."""
    d = draft({"f": pd.DataFrame({"count": range(60),
                                  "price": np.linspace(1.0, 2.0, 60)})})
    assert not d.forks["f"].datetime_columns
    assert all(c.role != "timestamp candidate" for c in d.columns)


def test_a_text_column_that_is_NOT_dates_is_not_read_as_a_timestamp():
    d = draft({"f": pd.DataFrame({"sym": ["ES"] * 60, "note": ["x"] * 60})})
    assert not d.forks["f"].datetime_columns
    assert all(c.role != "timestamp candidate" for c in d.columns)
