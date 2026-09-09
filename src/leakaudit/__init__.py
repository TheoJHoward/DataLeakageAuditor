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

*(Until R173 this cited `leakaudit.trace.assert_key_free`, which did not exist.  [dead-citation-recorded]
The invariant held -- verified across nine modules -- but nothing checked it, and
a cited checker that is absent is a false statement in the code carrying the
claim. That fix addressed the INSTANCE. `tests/phase1/citations.py` addresses the
class, and the first thing it did was find two more live ones -- in
`contract.py` and `corruption.py` -- neither of which review had caught. The
marker on the line above is what keeps a quoted historical citation on the record
without the check reading it as a live claim; every exempt line is reported.)*
"""
from .contract import (
    Alignment, ContractError, audit, normalise_raw, resolve_decision_time)
from .determinism import DeterminismResult, check_frame, frames_equal
from .checks import (
    CheckFinding, CheckResult, check_constant_columns,
    check_duplicate_rows_across_split, check_pairwise_label_correlation,
    check_split_validity, run_all)
from .findings import AuditResult, Finding
from .probe import DETECTOR_ID, ProbeResult, cohort_id_for, probe_columns
from .detectors import (
    NULL_DETECTOR_ID, VALUE_DETECTOR_ID, probe_nulls, probe_values)
from .availability import (
    NOT_DECLARED, AvailabilityModel, EligibleCohorts, ProbeAResult, ProbeError,
    align_key, eligible_cohorts, run_probe_a)
# SLICING. `DESIGN.md` §5.3, R255. A slice without declared padding is refused,
# and the padding this tool cannot derive is the builder's own lookback -- see
# the module docstring, which records the establish that preceded the refusal.
from .slicing import (
    SliceError, SlicePlan, model_padding_floor, plan_slice, split_seconds)
from .availability_trace import traces_for
# THE LABEL PROBE. R261 §4, built after R261 §1 repaired the attribution rule
# both rows now share. Exported because R201 P2's lesson was that the instrument
# a user most needs was absent from this list.
from .label_probe import (
    LabelAvailability, LabelDeclarationError, LabelProbeResult, RawLabel,
    resolve_label_declaration, run_probe_l2a)
from .identity_control import IdentityControlResult, run_identity_control
# INFERENCE. R232 §5. It proposes and never picks: structure is
# determined from the frames, availability is left blank because it is
# not in them, and `accept` refuses a draft whose blanks are still blank.
from .inference import (  # noqa: F401
    Draft, UnfilledAvailability, accept, draft, render_draft)
from .modes import (
    ALL_MODES, FILE_MODES, ColumnMode, ModeError, availability,
    availability_matrix, bar_duration, undeclared_columns)
from . import fixture_adapter

__all__ = [
    # the entry point and what it returns
    "audit", "AuditResult", "Finding",
    # P4 -- the checks that need no availability model.
    "run_all", "CheckResult", "CheckFinding", "check_split_validity",
    "check_duplicate_rows_across_split", "check_constant_columns",
    "check_pairwise_label_correlation",
    "Draft",
    "UnfilledAvailability",
    "accept",
    "draft",
    "render_draft",
    "normalise_raw", "ContractError", "resolve_decision_time", "Alignment",
    "check_frame", "frames_equal", "DeterminismResult",
    # Layer 1 -- the column dependency probe. No availability model needed.
    "probe_columns", "ProbeResult", "cohort_id_for", "DETECTOR_ID",
    "probe_values", "probe_nulls", "VALUE_DETECTOR_ID", "NULL_DETECTOR_ID",
    # THE AVAILABILITY PROBE. Exported at R201 P2: it is the only instrument
    # that separated the acceptance pair, and it was not in this list.
    # L2a -- the label probe, and the two declarations it refuses without.
    "run_probe_l2a", "LabelProbeResult", "LabelAvailability", "RawLabel",
    "LabelDeclarationError", "resolve_label_declaration",
    "AvailabilityModel", "run_probe_a", "ProbeAResult", "ProbeError",
    "eligible_cohorts", "EligibleCohorts", "align_key", "traces_for",
    "run_identity_control", "IdentityControlResult",
    # P5 -- the per-column availability modes. AVAILABILITY_MODES.md is the
    # arithmetic, written before the parser that reads it.
    "ColumnMode", "ModeError", "availability", "availability_matrix",
    "bar_duration", "undeclared_columns", "FILE_MODES", "ALL_MODES",
    # the slice rule
    "SliceError", "SlicePlan", "NOT_DECLARED", "model_padding_floor",
    "plan_slice", "split_seconds",
    "fixture_adapter",
]
