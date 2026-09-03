"""The opt-in tests' recorded result is CURRENT, checked in the default suite.

WHAT WAS WRONG. `test_every_opt_in_test_has_a_recorded_result` runs always and
checks that a result EXISTS. It cannot check that the result is still about the
code now on disk, and nothing else did.

WHAT WAS NOT WRONG, corrected here because the false version was written into two
deltas and one committed docstring before the content read caught it: **the
record has never gone content-stale.** It went COMMIT-stale twice, and both
"stale" findings were false positives of exactly the commit-ancestry comparator
this check was then built to avoid. **Zero demonstrated true positives.** The
justification is that the suite line's "passing as of" is a currency claim
needing a check behind it, and that this would detect content-staleness if it
occurred -- not that it has already caught anything.

THE COMPARATOR IS CONTENT, NOT COMMIT ANCESTRY. R213 §3. A check keyed to "is the
attested commit HEAD" goes red on every unrelated commit, gets overridden within
a week, and is then worse than nothing: a red light everyone has learned to walk
past. The record attests a digest per module for the modules these tests actually
EXECUTE, so it fires when something that could change the answer changed and
stays quiet otherwise.

WHICH MODULES, AND WHY THEY ARE NOT THE PROBE'S. Measured with
`probe_path_guard.record_modules()` -- the same instrument, a different question.
The two sets turn out to be DISJOINT: the probe executes `availability.py`,
`modes.py`, `availability_trace.py` and the frozen reducer; these tests execute
`fixture_adapter.py`, `determinism.py` and the fixture's own producing code. The
probe is handed frames; these tests produce them. Two records, not one.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import opt_in_currency as oic                                     # noqa: E402


def test_the_recorded_result_is_CURRENT():
    s = oic.status()
    assert s["state"] == "current", (
        "the opt-in tests' recorded result no longer describes the code on "
        "disk. Moved: %s. Gone: %s. Two of those tests are KNOWN POSITIVES for "
        "the adapter's equality claim, so until they are re-run, any clean "
        "result resting on that surface is believed without them. Re-run with "
        "`python tools/opt_in_currency.py --measure %s`."
        % (s.get("moved"), s.get("gone"), s.get("run")))


def test_the_attested_set_is_NOT_EMPTY_and_names_the_adapter():
    doc = oic.load()
    _key, run = oic.latest_run(doc)
    att = run.get(oic.ATTESTS) or {}
    assert att, "an empty attestation would make this check vacuously current"
    assert "src/leakaudit/fixture_adapter.py" in att, (
        "the adapter is the thing these tests attest; if it is not in the set, "
        "the set was not measured from a real run: %s" % sorted(att))


def test_the_two_module_SETS_ARE_RECORDED_SEPARATELY():
    """They answer different questions and must not be merged for tidiness."""
    import probe_path_guard as ppg

    probe = ppg.path_set()
    _key, run = oic.latest_run(oic.load())
    opt_in = set(run[oic.ATTESTS])
    assert opt_in, "no attested set"
    assert probe & opt_in == set(), (
        "the two sets overlap, which is fine in principle but means this "
        "assertion needs rewriting rather than deleting -- it exists to notice "
        "when the two questions stop being separate: %s" % sorted(probe & opt_in))


def test_the_suite_line_states_currency_and_not_just_a_count():
    line = oic.suite_line()
    assert "deferred (opt-in)" in line, line
    assert "skipped" not in line, (
        "`skipped` is the word that makes a cost-deferred passing test look "
        "like an inapplicable one: %s" % line)
    assert "as of" in line or "STALE" in line or "UNATTESTED" in line, line


# ---------------------------------------------------------------------------
# THE POSITIVE. A currency check that cannot go red is a green light, not a
# check, and this is the defect it exists to catch: a module it attests moved.
# ---------------------------------------------------------------------------

def test_a_MOVED_module_is_reported_stale(tmp_path, monkeypatch):
    rec = tmp_path / "fixture_run_record.json"
    rec.write_text(json.dumps({"run_2026_01_01": {
        "date": "2026-01-01", "commit": "abc1234",
        oic.ATTESTS: {"src/leakaudit/fixture_adapter.py": "0" * 64},
    }}), encoding="utf-8")
    monkeypatch.setattr(oic, "RECORD", rec)

    s = oic.status()
    assert s["state"] == "stale", s
    assert "src/leakaudit/fixture_adapter.py" in s["moved"]
    line = oic.suite_line()
    assert "STALE" in line and "fixture_adapter" in line, line
    assert "Re-run them before believing" in line, line


def test_a_VANISHED_module_is_reported_too(tmp_path, monkeypatch):
    rec = tmp_path / "fixture_run_record.json"
    rec.write_text(json.dumps({"run_2026_01_01": {
        "date": "2026-01-01", "commit": "abc1234",
        oic.ATTESTS: {"src/leakaudit/deleted_module.py": "0" * 64},
    }}), encoding="utf-8")
    monkeypatch.setattr(oic, "RECORD", rec)
    s = oic.status()
    assert s["state"] == "stale" and s["gone"], s


def test_a_record_with_NO_attestation_says_unattested_not_current(tmp_path,
                                                                  monkeypatch):
    """The failure mode a boolean check would have: absent read as fine."""
    rec = tmp_path / "fixture_run_record.json"
    rec.write_text(json.dumps({"run_2026_01_01": {
        "date": "2026-01-01", "commit": "abc1234"}}), encoding="utf-8")
    monkeypatch.setattr(oic, "RECORD", rec)
    s = oic.status()
    assert s["state"] == "unattested", s
    assert "current" != s["state"]


@pytest.mark.parametrize("content,fragment", [
    (None, "is missing"),
    ("{not json", "could not be read as JSON"),
    (json.dumps({"what_this_is": "x"}), "no `run_*` entry"),
])
def test_an_unreadable_record_REFUSES(tmp_path, monkeypatch, content, fragment):
    rec = tmp_path / "fixture_run_record.json"
    if content is not None:
        rec.write_text(content, encoding="utf-8")
    monkeypatch.setattr(oic, "RECORD", rec)
    with pytest.raises(oic.OptInRecordError) as e:
        oic.status()
    assert fragment in str(e.value), str(e.value)


def test_the_newest_run_is_the_one_read(tmp_path, monkeypatch):
    """Dated keys sort as strings; a wrong pick would attest an older code state."""
    rec = tmp_path / "fixture_run_record.json"
    rec.write_text(json.dumps({
        "run_2026_08_26": {"date": "2026-08-26", "commit": "old"},
        "run_2026_09_03": {"date": "2026-09-03", "commit": "new"},
        "run_2026_09_02": {"date": "2026-09-02", "commit": "mid"},
    }), encoding="utf-8")
    monkeypatch.setattr(oic, "RECORD", rec)
    key, run = oic.latest_run(oic.load())
    assert key == "run_2026_09_03" and run["commit"] == "new"
