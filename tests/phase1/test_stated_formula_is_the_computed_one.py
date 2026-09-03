"""The docstring's availability formula, checked against the arithmetic. R207 §1.

WHAT GAP THIS CLOSES, AND WHAT IT DOES NOT. The citation test checks that a
cited thing EXISTS. Three findings were caught that way -- `assert_key_free`,
`gate_inputs_only`, `may_short_circuit` -- all of them citations of things that
did not exist. D-V30A-43 is a fourth of the family and none of that machinery
could see it: `AvailabilityModel` resolves fine, its docstring is well-formed,
and what was wrong was that it DESCRIBED BEHAVIOUR THE CODE DID NOT HAVE. A
module that imports cleanly and lies about itself passes every existence check
ever written.

A GENERAL description-versus-behaviour check is not cheap and is not attempted
here; the report says so in terms. What is cheap is this shape and only this
shape: a docstring that states a CLOSED-FORM availability instant over `key` and
`window`, where two candidate formulas can be made to disagree on constructed
data. That is one convention and one discriminating frame, so it is built.

THE TEST IS BACKWARDS FROM THE USUAL ONE. It does not assert the docstring says
a particular thing -- that would just move the false statement into the test. It
EXTRACTS whatever formula the docstring states and then asks the probe which
formula it is actually running. If someone edits the sentence back to
`key + window`, extraction succeeds, the arithmetic check fails, and the failure
names the disagreement.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402

N = 200
OFFSET_MS = 400          # every key sits 400 ms inside its second
STATED = re.compile(r"declared availability instant is\s*\**`([^`]+)`")


def stated_formula() -> str:
    m = STATED.search(AvailabilityModel.__doc__ or "")
    assert m, (
        "no availability formula found in AvailabilityModel's docstring. Either "
        "the sentence was removed -- in which case this check has no subject and "
        "must not silently pass -- or its wording changed and this pattern needs "
        "updating with it.")
    return " ".join(m.group(1).split())


def _frames():
    """A key that is 400 ms INSIDE each second, so the two formulas disagree.

    Under `floor(key) + window` a cell of this frame becomes knowable at the end
    of the second its key falls in, and the probe's selected seconds -- which are
    exact wall-clock seconds taken from the decision stamps -- match it.
    Under `key + window` nothing matches, because no key equals a whole second.
    """
    secs = pd.date_range("2026-05-04 10:00:00", periods=N, freq="1s")
    rng = np.random.default_rng(23)
    agg = pd.DataFrame({"k": secs + pd.Timedelta(milliseconds=OFFSET_MS),
                        "v": rng.standard_normal(N)})
    snap = pd.DataFrame({
        "timestamp": [s + pd.Timedelta(milliseconds=150) for s in secs]})
    return {"snap": snap, "agg": agg}


def _build(raw):
    out = raw["snap"].copy()
    out["sec"] = pd.to_datetime(out["timestamp"]).dt.floor("s")
    a = raw["agg"].copy()
    a["sec"] = pd.to_datetime(a["k"]).dt.floor("s")
    out["v"] = out["sec"].map(a.set_index("sec")["v"]).to_numpy()
    return out[["timestamp", "v"]]


MODEL = AvailabilityModel(aggregate_frames={"agg": "k"},
                          decision_column="timestamp")


def test_the_docstring_states_a_formula_at_all():
    """If this check loses its subject it fails loudly rather than passing."""
    f = stated_formula()
    assert "window" in f and "key" in f, (
        "the stated instant does not mention both `key` and `window`, so it is "
        "not the closed form this check knows how to verify: %r" % f)


def test_the_STATED_formula_is_the_one_the_probe_RUNS():
    """The whole point. Extract, then measure -- never assert the prose.

    The discriminator is a key that is never a whole second. Under the floored
    reading the probe finds its cells; under the unfloored reading it finds
    none, and the probe raises rather than reporting a false silence.
    """
    stated = stated_formula()
    floors = stated.startswith("floor(")

    raw = _frames()
    res = run_probe_a(raw, _build, MODEL, side="test",
                      cohort_stride=5, max_cohorts=20, seed=9)
    corrupted = [n for n in res.notes if "corrupted" in n and "row(s)" in n]
    runs_floored = bool(corrupted)

    assert floors == runs_floored, (
        "the docstring and the arithmetic disagree. The docstring states the "
        "availability instant is `%s`; the probe %s a key that is never on a "
        "second boundary, which is the behaviour of `%s`. This is exactly "
        "D-V30A-43 -- a description that resolves, imports and reads cleanly "
        "while describing something the code does not do."
        % (stated,
           "FOUND cells for" if runs_floored else "found NO cells for",
           "floor(key) + window" if runs_floored else "key + window"))


def test_the_SCHEMA_DOC_states_the_same_formula_as_the_docstring():
    """The second place the formula is written, and the one users actually read.

    R208 §3 walked the stranger path and found `leakaudit schema` still saying
    the instant is "that key plus the window" -- the exact sentence corrected in
    `AvailabilityModel` the round before. Correcting one statement of a fact and
    leaving its duplicate is the failure this project keeps finding in itself,
    so the check is widened to the population rather than to the one instance.
    """
    from leakaudit.model_file import SCHEMA_DOC

    body = " ".join(SCHEMA_DOC.split())
    assert "floor(key) + window" in body, (
        "`leakaudit schema` does not state the floored instant. It is what a "
        "stranger reads before writing their model file, and it is the only "
        "place most of them will read it: %r"
        % body[body.find("aggregate_frames"):][:260])
    assert "is that key plus the window" not in body, (
        "the superseded unfloored wording is still in the schema doc")


def test_the_discriminator_actually_discriminates():
    """The negative control: on a floored key both formulas agree.

    Without this, the test above could pass on data where the two readings are
    the same number -- which is the precise condition under which the original
    defect survived two rounds unnoticed.
    """
    secs = pd.date_range("2026-05-04 10:00:00", periods=N, freq="1s")
    k = pd.Series(secs + pd.Timedelta(milliseconds=OFFSET_MS))
    assert (k.dt.floor("s") != k).all(), (
        "the constructed key is on second boundaries, so the two candidate "
        "formulas give the same answer and this file proves nothing")

    floored = pd.Series(secs)
    assert (floored.dt.floor("s") == floored).all()
