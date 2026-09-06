"""The guard's SAME is discriminating, not a coincidence of two numbers. R231 §4.

WHAT THE GUARD ESTABLISHED AND WHAT IT DID NOT. `tools/wholeframe_guard.py`
compares eight terms against the committed population run and reports SAME. That
establishes that eight numbers match eight committed numbers. It was read as "the
probe still works", which is a wider claim — **the guard's SAME was a believed
silence**, which is R215 §0's refinement pointed at the guard itself.

THE RELATION. The contaminated side is the fixture with a known leak; the
corrected side is the same fixture without it. So the contaminated side MUST FIND
and the corrected side MUST NOT. Until R231 that held only because the committed
baseline happened to encode it — a property of the arrangement rather than a
checked fact.

WHY CHECKING IT SEPARATELY IS NOT REDUNDANT, which is the question to ask of any
second check. The term comparison's authority is a file in this repository. A
baseline edited by a bad merge, a regenerated artifact or a hand would make the
comparison pass against the edited values. **The relation is a property of the
RUN, not of the baseline**, so it survives a corrupted baseline and fails on one
that no longer describes a discriminating probe.

WHY THESE TESTS DO NOT RUN THE GUARD. The guard costs about nine minutes and
needs the acceptance fixture. The relation is a pure function of the two sides'
results, so it is tested directly against constructed inputs — including the
failure modes that matter, which a passing live run would never exhibit.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import wholeframe_guard as wg                                    # noqa: E402

GOOD = {"contaminated": {"verdict": "finding", "records": 5220},
        "corrected": {"verdict": "observed_silence", "records": 0}}


def test_the_real_shape_holds():
    assert wg.relation_holds(GOOD)
    assert all("OK" in line for line in wg.relation_report(GOOD))


def test_BOTH_SIDES_SILENT_fails__the_probe_finding_nothing_anywhere():
    """The failure the term comparison would also catch, asserted here so the
    relation is known to cover it rather than assumed to."""
    bad = {"contaminated": {"verdict": "observed_silence", "records": 0},
           "corrected": {"verdict": "observed_silence", "records": 0}}
    assert not wg.relation_holds(bad)
    assert any("FAIL" in line and "contaminated" in line
               for line in wg.relation_report(bad))


def test_BOTH_SIDES_FINDING_fails__the_probe_firing_everywhere():
    bad = {"contaminated": {"verdict": "finding", "records": 5220},
           "corrected": {"verdict": "finding", "records": 5220}}
    assert not wg.relation_holds(bad)
    assert any("FAIL" in line and "corrected" in line
               for line in wg.relation_report(bad))


def test_the_sides_REVERSED_fails():
    """The case a baseline edit could make the comparison accept: the two sides
    swapped, so the corrected fixture is the one reporting the leak."""
    bad = {"contaminated": {"verdict": "observed_silence", "records": 0},
           "corrected": {"verdict": "finding", "records": 5220}}
    assert not wg.relation_holds(bad)


def test_a_VERDICT_without_records_fails():
    """`finding` with zero records is a verdict nothing supports, and the
    verdict alone would have passed a check that read only verdicts."""
    assert not wg.relation_holds(
        {"contaminated": {"verdict": "finding", "records": 0},
         "corrected": {"verdict": "observed_silence", "records": 0}})


def test_a_MISSING_side_fails_rather_than_defaulting_to_true():
    """An absent key is not a passing check. The guard would reach this if a
    side crashed and its entry was never written."""
    assert not wg.relation_holds({"contaminated": GOOD["contaminated"]})
    assert not wg.relation_holds({"corrected": GOOD["corrected"]})
    assert not wg.relation_holds({})


def test_the_report_names_WHICH_limb_failed():
    """A boolean tells somebody the guard is wrong; the report tells them
    where."""
    bad = {"contaminated": {"verdict": "finding", "records": 5220},
           "corrected": {"verdict": "finding", "records": 12}}
    lines = wg.relation_report(bad)
    failed = [ln for ln in lines if "FAIL" in ln]
    assert len(failed) == 2, lines
    assert all("corrected" in ln for ln in failed), failed
    assert "records=12" in " ".join(failed)


def test_the_guard_CHECKS_the_relation_before_printing_the_comparison():
    """A term-by-term SAME read from sides that do not discriminate is a
    coincidence of two numbers, so the comparison must not be printed at all."""
    src = (ROOT / "tools" / "wholeframe_guard.py").read_text(encoding="utf-8")
    rel = src.index("if not relation_holds(out):")
    cmp_ = src.index('print("\\nCOMPARISON, term by term:")')
    assert rel < cmp_, (
        "the relation is checked after the comparison is printed, so a reader "
        "sees SAME before being told it means nothing")
    assert "return 3" in src[rel:cmp_], (
        "the relation failing does not halt the guard: it must exit non-zero "
        "with a code distinct from the MOVED halt, so a caller can tell 'the "
        "numbers changed' from 'the numbers mean nothing'")
    assert "return 2" in src[cmp_:], "the MOVED halt is gone"
    assert "raise SystemExit(main())" in src, (
        "main()'s return code never reaches the process, so a failing guard "
        "exits zero")


def test_the_guard_lives_in_the_REPOSITORY_not_in_a_scratch_directory():
    """R231 §4, and TB-23's lesson applied to the guard itself: an assertion in
    a file that can vanish is an assertion nobody can re-run."""
    p = ROOT / "tools" / "wholeframe_guard.py"
    assert p.is_file()
    src = p.read_text(encoding="utf-8")
    assert "parents[1]" in src, (
        "the guard hardcodes a repository path, so it runs on one machine only")
    assert "Temp" not in src and "scratchpad" not in src, (
        "the guard still refers to a scratch directory")


# ---------------------------------------------------------------------------
# THE CONSTANTS. R232 §4.
# ---------------------------------------------------------------------------

SCOPE = {"stride": 997, "max_cohorts": 300, "seed": 20260828,
         "instruments": ["cl", "es", "zc"], "months": ["2025-01", "2025-08"]}
ARGS = ("zc", "2025-01", 997, 20260828, 300)


def test_the_baseline_ALREADY_carries_its_constants():
    """R232 §4 supposed the baseline would have to start recording them. It
    already does -- `scope`, written by the generating harness -- so this is a
    READ rather than an addition, and no dated acceptance artifact is edited."""
    import json
    prior = json.loads(
        (ROOT / "evidence" / "phase1" / "criteria_12_population.json")
        .read_text(encoding="utf-8"))
    scope = prior["scope"]
    for k in ("stride", "max_cohorts", "seed", "instruments", "months"):
        assert k in scope, "the baseline's scope no longer records %r" % k


def test_the_REAL_baseline_matches_the_REAL_guard_constants():
    """The live case. If this fails, every prior comparison was between two
    different runs and nobody would have known."""
    import json
    import re
    prior = json.loads(
        (ROOT / "evidence" / "phase1" / "criteria_12_population.json")
        .read_text(encoding="utf-8"))
    src = (ROOT / "tools" / "wholeframe_guard.py").read_text(encoding="utf-8")
    m = re.search(r"SYM, MONTH, STRIDE, SEED, MAXC = "
                  r'"(\w+)", "([\d-]+)", (\d+), (\d+), (\d+)', src)
    assert m, "the guard's constants line has changed shape"
    sym, month, stride, seed, maxc = (m.group(1), m.group(2), int(m.group(3)),
                                      int(m.group(4)), int(m.group(5)))
    assert wg.constants_match(prior["scope"], sym, month, stride, seed, maxc), (
        wg.constants_report(prior["scope"], sym, month, stride, seed, maxc))


def test_a_DIFFERENT_stride_is_refused():
    assert not wg.constants_match(SCOPE, "zc", "2025-01", 500, 20260828, 300)


def test_a_DIFFERENT_seed_is_refused():
    assert not wg.constants_match(SCOPE, "zc", "2025-01", 997, 1, 300)


def test_a_DIFFERENT_max_cohorts_is_refused():
    assert not wg.constants_match(SCOPE, "zc", "2025-01", 997, 20260828, 50)


def test_an_INSTRUMENT_the_baseline_never_covered_is_refused():
    assert not wg.constants_match(SCOPE, "nq", "2025-01", 997, 20260828, 300)


def test_a_MONTH_the_baseline_never_covered_is_refused():
    assert not wg.constants_match(SCOPE, "zc", "2025-12", 997, 20260828, 300)


def test_a_MISSING_scope_is_refused_rather_than_treated_as_agreement():
    """An absent frame is not a matching frame. This is the case a regenerated
    or truncated baseline would present."""
    assert not wg.constants_match({}, *ARGS)
    assert not wg.constants_match(None, *ARGS)


def test_the_report_names_WHICH_constant_differs():
    lines = wg.constants_report(SCOPE, "zc", "2025-01", 500, 20260828, 300)
    failed = [ln for ln in lines if "FAIL" in ln]
    assert len(failed) == 1, lines
    assert failed[0].startswith("stride")
    assert "baseline=997" in failed[0] and "guard=500" in failed[0]


def test_the_constants_are_checked_BEFORE_anything_is_probed():
    """A warning on a seven-minute run is a line somebody scrolls past, and
    refusing after the computation spends seven minutes to say the comparison
    was never going to mean anything."""
    src = (ROOT / "tools" / "wholeframe_guard.py").read_text(encoding="utf-8")
    halt = src.index("if not constants_match(")
    capture = src.index("cap = fa.read_inputs(")
    assert halt < capture, (
        "the constants are checked after the fixture is captured, so a mismatch "
        "costs a capture before it refuses")
    assert "return 4" in src[halt:capture], (
        "a constants mismatch does not refuse with its own exit code")


def test_the_three_halts_have_DISTINCT_exit_codes():
    """A caller must be able to tell 'the numbers changed' from 'the numbers
    mean nothing' from 'these are not the same run'."""
    src = (ROOT / "tools" / "wholeframe_guard.py").read_text(encoding="utf-8")
    for code, why in ((2, "MOVED"), (3, "relation"), (4, "constants")):
        assert "return %d" % code in src, "%s halt (%d) is gone" % (why, code)
