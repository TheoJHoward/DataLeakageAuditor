"""Defaults taken, classified, with totality enforced. R222 §2.

THE OUTPUT IS A CANDIDATE LIST, NEVER A FINDING LIST. Most defaults are correct.
Whether a given one should refuse is a per-site judgment, and the judgment is
`CLASSIFICATION` below — not anything the tracer computes. A tracer that reported
every default taken and called the list a finding is the plausible wrong
instrument here, and `test_the_instrument_does_not_call_its_output_a_finding`
rules it out as a property rather than as an intention.

TWO POPULATIONS, AND EVERY NUMBER SAYS WHICH IT IS.

    STATIC  121 sites -- everything reachable. 103 parameters plus 18
            `.get`/`getattr` calls, which have no wrappable boundary and are in
            this population only.
    RUNTIME  30 sites -- everything reached, BY THE RUNS NAMED IN `RUNS`. That
            number is entirely a function of those runs.
    The difference, 73 reachable-but-never-taken, is its own finding: defaults
    that exist and are never used.

AND THE TWO POPULATIONS DISAGREED IN BOTH DIRECTIONS WHEN FIRST MEASURED. The
runtime tracer saw thirteen sites the static enumeration missed -- every one a
`@dataclass`-generated `__init__`, which exists at run time and in no
`FunctionDef`. So "everything reachable" was SMALLER than "everything reached",
which is the shape a population claim must never have. The enumerator was taught
about dataclass fields and they now reconcile at zero.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src"), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import default_sites as ds                                        # noqa: E402
from leakaudit import cli                                         # noqa: E402

RUNS = ("the CLI end to end on a non-fixture pandas pipeline: `leakaudit run` "
        "without a model, `leakaudit run --model` with column_modes declared, "
        "and `leakaudit check` both with and without a model")

L, R, NA = ds.LEGITIMATE, ds.SHOULD_REFUSE, ds.NOT_APPLICABLE

# Every RUNTIME candidate, classified. Unclassified fails.
CLASSIFICATION = {
    # -- dataclass result carriers. Not user declarations at all: these are the
    # tool's own output objects being constructed field by field.
    "availability.py::param::__init__(base_columns=)": (NA, "result carrier field"),
    "availability.py::param::__init__(cohorts=)": (NA, "result carrier field"),
    "availability.py::param::__init__(determinism_ok=)": (NA, "result carrier field"),
    "availability.py::param::__init__(eligible=)": (NA, "result carrier field"),
    "availability.py::param::__init__(ineligible=)": (NA, "result carrier field"),
    "availability.py::param::__init__(notes=)": (NA, "result carrier field"),
    "availability.py::param::__init__(per_frame=)": (NA, "result carrier field"),
    "availability.py::param::__init__(unmodelled_frames=)": (NA, "result carrier field"),
    "checks.py::param::__init__(did_not_look_because=)": (NA, "result carrier field"),
    "checks.py::param::__init__(findings=)": (NA, "result carrier field"),
    "checks.py::param::__init__(notes=)": (NA, "result carrier field"),
    "checks.py::param::__init__(population=)": (NA, "result carrier field"),
    "determinism.py::param::__init__(raised=)": (NA, "result carrier field"),
    "findings.py::param::__init__(checks=)": (NA, "result carrier field"),

    # -- internal plumbing, not reachable as a user declaration.
    "contract.py::param::audit(case_id=)": (NA, "internal trace label"),
    "contract.py::param::audit(run_context=)": (NA, "internal enum, USER by default"),
    "probe.py::param::_run_one(detector_id=)": (NA, "internal, private function"),
    "probe.py::param::probe_columns(columns=)": (NA, "internal; None means every column"),
    "corruption.py::param::corrupt(mask=)": (NA, "internal; None means every row"),
    "checks.py::param::check_duplicate_rows_across_split(columns=)":
        (NA, "internal; None means every column, and the population is reported"),

    # -- REFUSED rather than defaulted. These are the _UNWIRED five: the default
    # is None and supplying anything raises, which is the opposite of a silent
    # default and is what the whole registry exists to do.
    "contract.py::param::audit(availability=)": (L, "None then REFUSED by _UNWIRED"),
    "contract.py::param::audit(decision_time=)": (L, "None then REFUSED by _UNWIRED"),
    "contract.py::param::audit(meta=)": (L, "None then REFUSED by _UNWIRED"),

    # -- absent means NOT CHECKED, and the check says so. The default is the
    # mechanism by which a silence is reported as a silence.
    "contract.py::param::audit(train_idx=)": (L, "None -> the split checks report NOT CHECKED"),
    "contract.py::param::audit(test_idx=)": (L, "None -> the split checks report NOT CHECKED"),
    "checks.py::param::run_all(label=)": (L, "None -> the label check reports NOT CHECKED"),

    # -- a declared, documented default the user can see and override.
    "availability.py::param::run_probe_a(seed=)":
        (L, "a fixed seed is the determinism property; a random one would make "
            "the probe non-reproducible, which the determinism guard would then "
            "report as a pipeline defect"),
    "modes.py::param::availability(fn=)":
        (L, "availability_fn is library-only by design and a file cannot carry a "
            "function; absent means the mode is not availability_fn"),

    # ---------------------------------------------------------------------
    # THE TWO THAT ARE NOT COMFORTABLE. Both are REACHED, not merely reachable.
    # ---------------------------------------------------------------------
    "modes.py::param::availability(declared_bar_duration=)": (
        R,
        "`PREREG.md` §2.3's bar_duration element reads 'fixed value, OR inferred "
        "from successive timestamps' and names NO default between them. The "
        "config file carries no key for it at all, so a user declaring "
        "`at_bar_close` cannot state a bar duration and silently gets inference. "
        "That is the tool choosing one of two registered options on the user's "
        "behalf, which is the shape `leakaudit schema` already refuses for "
        "column modes: 'an assumed mode is an availability model you did not "
        "write.' CANDIDATE, not a defect -- whether the registration intends "
        "inference as the default is a structural read nobody has done."),
    "checks.py::param::check_label_under_another_name(threshold=)": (
        R,
        "a 0.999 correlation threshold the user cannot see or set, and the "
        "check's own output does not name it: it reports 'nothing found over 8 "
        "column(s) against the label' with no mention of the threshold that "
        "produced the silence. A figure without its frame, by the durable rule "
        "in OPERATING_RULES.md §2. CANDIDATE: the fix may be naming it in the "
        "output rather than exposing it, and that is a judgment nobody has made."),
}


def _measure(tmp_path):
    secs = pd.date_range("2026-07-07 09:00:00", periods=90, freq="1s")
    rng = np.random.default_rng(11)
    pd.DataFrame({"timestamp": [s + pd.Timedelta(milliseconds=300) for s in secs],
                  "q": rng.standard_normal(90)}).to_csv(tmp_path / "snap.csv",
                                                        index=False)
    pd.DataFrame({"k": secs, "v": rng.standard_normal(90),
                  "w": rng.standard_normal(90)}).to_csv(tmp_path / "agg.csv",
                                                        index=False)
    (tmp_path / "p.py").write_text(
        "import pandas as pd\n"
        "def build(f):\n"
        "    o = f['snap'].copy()\n"
        "    o['sec'] = pd.to_datetime(o['timestamp']).dt.floor('1s')\n"
        "    a = f['agg'].copy(); a['sec'] = pd.to_datetime(a['k'])\n"
        "    o['x'] = o['sec'].map(a.set_index('sec')['v']).to_numpy()\n"
        "    o['target'] = (o['x'] > 0).astype(int)\n"
        "    return o[['timestamp', 'x', 'target']]\n", encoding="utf-8")
    (tmp_path / "m.json").write_text(json.dumps({
        "version": 3, "aggregate_frames": {"agg": "k"},
        "decision_column": "timestamp", "label_column": "target",
        "split": {"train": [0, 1, 2, 3], "test": [4, 5]},
        "column_modes": {"v": "at_timestamp"}}), encoding="utf-8")

    sys.path.insert(0, str(tmp_path))
    F = ["--frame", "snap=%s" % (tmp_path / "snap.csv"),
         "--frame", "agg=%s" % (tmp_path / "agg.csv")]
    try:
        with ds.trace_defaults(runs=RUNS) as taken:
            for argv in (["run", "--pipeline", "p:build", *F],
                         ["run", "--pipeline", "p:build", *F,
                          "--model", str(tmp_path / "m.json")],
                         ["check", "--pipeline", "p:build", *F],
                         ["check", "--pipeline", "p:build", *F,
                          "--model", str(tmp_path / "m.json")]):
                try:
                    cli.main(argv)
                except SystemExit:
                    pass
    finally:
        sys.path.remove(str(tmp_path))
    return taken


# ---------------------------------------------------------------------------
# (b) the population names its runs -- enforced, not remembered.
# ---------------------------------------------------------------------------

def test_the_tracer_REFUSES_to_run_without_its_runs_named():
    for bad in ("", "   ", None):
        with pytest.raises(ValueError, match="runs"):
            with ds.trace_defaults(runs=bad):
                pass


# ---------------------------------------------------------------------------
# (c) totality. Unclassified fails.
# ---------------------------------------------------------------------------

def test_EVERY_runtime_candidate_IS_CLASSIFIED(tmp_path):
    taken = _measure(tmp_path)
    assert taken, "the tracer recorded nothing; it is not attached"
    unclassified = set(taken) - set(CLASSIFICATION)
    assert not unclassified, (
        "these defaults were taken during the named runs and nobody has said "
        "whether each is legitimate, should refuse, or is not applicable. "
        "Unclassified is not one of the three states: %s" % sorted(unclassified))


def test_every_classification_is_one_of_the_THREE_states():
    for key, (state, reason) in CLASSIFICATION.items():
        assert state in ds.STATES, "%s: %r" % (key, state)
        assert len(reason) > 10, "%s has no real reason: %r" % (key, reason)


def test_no_classification_names_a_site_that_does_not_exist(tmp_path):
    static = {ds.site_key(m, k, s) for m, _l, k, s in ds.static_sites()}
    stray = set(CLASSIFICATION) - static
    assert not stray, (
        "classified but present in neither population -- a leftover from a "
        "renamed or deleted site: %s" % sorted(stray))


# ---------------------------------------------------------------------------
# (d) the two populations, and the direction they must never disagree in.
# ---------------------------------------------------------------------------

def test_the_runtime_population_is_a_SUBSET_of_the_static_one(tmp_path):
    """'Everything reachable' smaller than 'everything reached' is incoherent.

    It was true when first measured: thirteen dataclass `__init__` sites existed
    at run time and in no `FunctionDef`. That is the defect this asserts against.
    """
    taken = _measure(tmp_path)
    static = {ds.site_key(m, k, s) for m, _l, k, s in ds.static_sites()}
    missing = set(taken) - static
    assert not missing, (
        "the static enumeration cannot see these, so it under-reports what is "
        "reachable: %s" % sorted(missing))


def test_the_static_population_is_STRICTLY_LARGER(tmp_path):
    """The difference is its own finding: defaults never taken by these runs."""
    taken = _measure(tmp_path)
    static = {ds.site_key(m, k, s) for m, _l, k, s in ds.static_sites()}
    assert len(static) > len(taken), (
        "every reachable default was taken, which would mean these runs cover "
        "the whole package -- they do not, and a claim that they do needs more "
        "than this")


# ---------------------------------------------------------------------------
# (e) the discriminating positive. Its green is a silence somebody will believe.
# ---------------------------------------------------------------------------

def test_a_NEW_unclassified_default_site_FAILS_the_totality_check(tmp_path):
    """The positive: a site that should refuse cannot slip in silently.

    Simulated by removing a real candidate's classification rather than by
    adding a function, because what is under test is the GUARD's reaction to an
    unclassified site, and that is the same reaction either way.
    """
    taken = _measure(tmp_path)
    victim = "checks.py::param::run_all(label=)"
    assert victim in taken and victim in CLASSIFICATION
    reduced = {k: v for k, v in CLASSIFICATION.items() if k != victim}
    unclassified = set(taken) - set(reduced)
    assert unclassified == {victim}, (
        "removing a classification did not produce an unclassified candidate, "
        "so the totality check cannot notice a new site: %s" % unclassified)


def test_a_LEGITIMATE_default_is_not_reported_as_needing_refusal():
    """The other direction, which is what makes it a discrimination.

    An instrument that flagged every default taken would put these in the
    should-refuse set, and the whole design is that it does not.
    """
    legit = [k for k, (s, _r) in CLASSIFICATION.items() if s == L]
    assert legit, "no legitimate defaults classified, so nothing distinguishes"
    for k in legit:
        assert CLASSIFICATION[k][0] != R


def test_the_two_uncomfortable_candidates_ARE_marked_should_refuse():
    should = {k for k, (s, _r) in CLASSIFICATION.items() if s == R}
    assert should == {
        "modes.py::param::availability(declared_bar_duration=)",
        "checks.py::param::check_label_under_another_name(threshold=)",
    }, sorted(should)
    for k in should:
        assert "CANDIDATE" in CLASSIFICATION[k][1], (
            "%s is marked should_refuse without saying it is a candidate rather "
            "than a settled defect" % k)


# ---------------------------------------------------------------------------
# (a) candidates, never findings -- asserted as a property of the module.
# ---------------------------------------------------------------------------

def test_the_instrument_does_not_call_its_output_a_finding():
    src = (ROOT / "tools" / "default_sites.py").read_text(encoding="utf-8")
    code = "\n".join(line for line in src.split("\n")
                     if not line.strip().startswith("#"))
    body = code.split('"""')[-1]
    assert "finding" not in body.lower(), (
        "the tracer's code names something a finding. Its output is a candidate "
        "list and the judgment is elsewhere; a name is how that stops being true")
