"""leakaudit -- runtime leakage auditing by intervention.

Phase 1, under development. Nothing here is a registered detector; the
registration is `PREREG.md` and this package implements against it.

SC-7(c) IS ENFORCED BY SIGNATURE, NOT BY DISCIPLINE. The declared ground-truth
map is the scoring key, and PREREG.md SC-7(b)/(c) withhold it from the tool:

    A detector that could read it would be graded against a key it had seen, and
    the run would measure retrieval rather than discrimination. The map is an
    artifact of the harness, not an input to the tool. A run that received the
    key has not produced a gate result, whatever it reports.

The reducers already draw that boundary: `compute_runtime_metrics(traces,
labels)` takes `CaseLabels` as a SEPARATE argument. This package produces
`CombinationTrace` and never accepts, imports, or constructs `CaseLabels` -- so
the withholding is structural.

`tests/phase1/sc7c.py` states the invariant executably: `assert_key_free` parses
every module here and fails if any imports the name, binds the harness module,
constructs it, or reaches it by attribute. It is exercised against one violating
copy per route, with a negative control, in `tests/phase1/test_sc7c.py`.

*(Until R173 this cited `leakaudit.trace.assert_key_free`, which did not exist.
The invariant held -- verified across nine modules -- but nothing checked it, and
a cited checker that is absent is a false statement in the code carrying the
claim.)*
"""
from .contract import ContractError, audit, normalise_raw
from .determinism import DeterminismResult, check_frame, frames_equal
from .probe import DETECTOR_ID, ProbeResult, cohort_id_for, probe_columns
from .detectors import (
    NULL_DETECTOR_ID, VALUE_DETECTOR_ID, probe_nulls, probe_values)
from . import fixture_adapter

__all__ = [
    "audit", "normalise_raw", "ContractError",
    "check_frame", "frames_equal", "DeterminismResult",
    "probe_columns", "ProbeResult", "cohort_id_for", "DETECTOR_ID",
    "probe_values", "probe_nulls", "VALUE_DETECTOR_ID", "NULL_DETECTOR_ID",
    "fixture_adapter",
]
