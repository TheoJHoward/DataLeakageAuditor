"""The path set is data, the guard reads it, and it fails loudly. R212 §2.

THE ONE FAILURE THIS MODULE REFUSES TO HAVE is covering nothing quietly. A guard
whose population file has moved, been emptied, or been half-written must refuse,
not pass. That is the discarded-parameter defect a third time in this project,
and it is the shape the halt list names.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src"), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import probe_path_guard as ppg                                    # noqa: E402

# THE RECORDER IS 3.12+, AND ITS ABSENCE IS `unsupported`, NOT `failed`. R229 §2.
#
# `record_modules` uses `sys.monitoring`. On CPython 3.11 -- which this project
# declares as its floor -- these three tests raised `AttributeError` and were
# reported as FAILURES, which is a false statement about the tool: nothing is
# broken there, the instrument simply does not run. `PREREG.md` §8.2 accounts
# `unsupported` separately from findings everywhere, and this is the same
# discipline the cost-deferred fixture tests already get.
#
# The reason it is a gate and not a fallback is MEASURED and lives in
# `ppg.FALLBACK_MEASURED`: setprofile was affordable (x1.8) and recorded HALF the
# modules, which is the wrong direction for a staleness guard.
needs_monitoring = pytest.mark.skipif(
    not ppg.MONITORING_AVAILABLE,
    reason="UNSUPPORTED on CPython %s: this guard's recorder needs "
           "`sys.monitoring` (3.12+). Not a failure and not a pass -- the "
           "instrument did not run here. See ppg.FALLBACK_MEASURED for why "
           "there is no setprofile fallback."
           % ".".join(str(v) for v in sys.version_info[:3]))


def test_the_recorded_set_loads_and_names_the_probe_module():
    s = ppg.path_set()
    assert "src/leakaudit/availability.py" in s
    assert "protocol/runtime_reference.py" in s
    assert len(s) >= 4


def test_the_set_records_the_commit_it_was_measured_at():
    """Without it, staleness is a memory rather than a check."""
    assert ppg.measured_at()


def test_every_recorded_module_EXISTS():
    """A population naming a file that is gone covers less than it says."""
    for m in ppg.path_set():
        assert (ROOT / m).is_file(), "%s is recorded and absent" % m


def test_the_not_on_path_list_and_the_path_set_are_DISJOINT():
    doc = ppg.load()
    overlap = set(doc["path_set"]) & set(doc.get("not_on_the_path", []))
    assert not overlap, "a module is recorded as both on and off the path: %s" % overlap


def test_the_two_lists_together_COVER_the_package():
    """A module in neither list is a module nobody classified."""
    doc = ppg.load()
    named = set(doc["path_set"]) | set(doc.get("not_on_the_path", [])) | set(
        doc.get("added_by_judgment_not_by_the_trace", {}))
    on_disk = {"src/leakaudit/%s" % p.name
               for p in (ROOT / "src" / "leakaudit").glob("*.py")}
    missing = on_disk - named
    assert not missing, (
        "these modules are in neither list, so the rule does not say whether an "
        "edit to them needs the guard: %s" % sorted(missing))


# ---------------------------------------------------------------------------
# THE REFUSALS. Each is the file being unreadable in a different way, and each
# must raise rather than return an empty set.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("content,fragment", [
    (None, "is missing"),
    ("{not json", "could not be read as JSON"),
    (json.dumps({"measured_at_commit": "x", "method": "y"}), "has no 'path_set'"),
    (json.dumps({"path_set": [], "measured_at_commit": "x", "method": "y"}),
     "empty or non-list"),
    (json.dumps({"path_set": "availability.py", "measured_at_commit": "x",
                 "method": "y"}), "empty or non-list"),
    (json.dumps({"path_set": ["a"], "method": "y"}), "has no 'measured_at_commit'"),
])
def test_an_unreadable_population_REFUSES(tmp_path, monkeypatch, content, fragment):
    p = tmp_path / "PROBE_PATH_SET.json"
    if content is not None:
        p.write_text(content, encoding="utf-8")
    monkeypatch.setattr(ppg, "SET_FILE", p)
    with pytest.raises(ppg.ProbePathSetError) as e:
        ppg.path_set()
    assert fragment in str(e.value), str(e.value)


def test_the_refusal_is_not_an_empty_set(tmp_path, monkeypatch):
    """The whole point, stated as its own test."""
    monkeypatch.setattr(ppg, "SET_FILE", tmp_path / "gone.json")
    with pytest.raises(ppg.ProbePathSetError):
        ppg.path_set()


# ---------------------------------------------------------------------------
# THE STALENESS TRIGGER. It reports a module that EXECUTED and is not recorded.
# ---------------------------------------------------------------------------

@needs_monitoring
def test_watch_is_quiet_when_nothing_unrecorded_runs():
    said = []
    with ppg.watch(report=said.append):
        pass
    assert len(said) == 1 and "no drift" in said[0], said


@needs_monitoring
def test_watch_REPORTS_a_module_that_ran_and_is_not_recorded(monkeypatch, tmp_path):
    """The positive: pretend availability.py was never recorded, then run it."""
    p = tmp_path / "PROBE_PATH_SET.json"
    p.write_text(json.dumps({
        "path_set": ["protocol/runtime_reference.py"],
        "measured_at_commit": "deadbeef", "method": "test"}), encoding="utf-8")
    monkeypatch.setattr(ppg, "SET_FILE", p)

    said = []
    with ppg.watch(report=said.append):
        from leakaudit.availability import _window_text
        import pandas as pd
        _window_text(pd.Timedelta("1s"))

    assert len(said) == 1
    assert "STALE" in said[0], said[0]
    assert "src/leakaudit/availability.py" in said[0], said[0]
    assert "deadbeef" in said[0], (
        "the report does not say WHEN the set was measured, which is what tells "
        "a reader whether re-measuring is overdue: %s" % said[0])


@needs_monitoring
def test_watch_does_not_report_third_party_frames(monkeypatch, tmp_path):
    """pandas running is not drift in this package's path set."""
    p = tmp_path / "PROBE_PATH_SET.json"
    p.write_text(json.dumps({
        "path_set": ["src/leakaudit/availability.py"],
        "measured_at_commit": "x", "method": "test"}), encoding="utf-8")
    monkeypatch.setattr(ppg, "SET_FILE", p)
    said = []
    with ppg.watch(report=said.append):
        import pandas as pd
        pd.DataFrame({"a": [1, 2, 3]}).sum()
    assert "no drift" in said[0], said[0]
