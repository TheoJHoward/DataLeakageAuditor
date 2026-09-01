"""The identity control for L3.1. PREREG.md section 6.11 control 2; R194 §1.

WHAT IT IS. "Replace unavailable cells with an exact copy of themselves. Any
delta is measurement artifact." The registration puts it before every real
probe, once per execution frame, and criterion 4 scores it: silent under the
identity control on both sides.

WHY IT IS NOT A TAUTOLOGY, WHICH IS THE WHOLE CASE FOR BUILDING IT. An identity
perturbation over a deterministic builder is trivially silent IN ITS VALUES, and
that is not what the control tests. It tests THE MECHANISM THAT WRITES VALUES
BACK. An assignment that preserves every value can still promote a column's
dtype or replace its index, and a difference introduced there would surface in
every real probe as a finding belonging to the harness rather than to the
pipeline. The determinism guard compares two clean builds and never touches that
path: nothing is assigned in it at all.

AND A DTYPE PROMOTION IS NOT A COSMETIC DIFFERENCE HERE. Promotion status keys
the combination and decides the tier: a preserving run licenses PROVEN, a
promoting one is REVIEW `dtype_promoted` (section 3.1). A write-back that
silently promotes does not merely inject a spurious finding -- it changes the
tier every real finding is reported at. This is the only instrument that touches
that path.

TWO LIMBS, AND ONLY THE FIRST IS THE REGISTERED CRITERION.

  (a) OUTPUT SILENCE -- the registered limb. Build after the identity write, and
      compare against the baseline exactly. Any moved column is a control
      artifact and criterion 4 fails on that side.

  (b) INPUT INVARIANCE -- BEYOND THE REGISTERED TEXT, reported separately, and
      never used to say the criterion failed when limb (a) passed. The write-back
      is checked for value, dtype and index equality on the frames it touched.
      It exists because a builder can ABSORB an input-side promotion -- resetting
      an index, casting on merge -- so limb (a) can pass while the write-back has
      changed the frame the probe's promotion status is computed from. Limb (a)
      is the criterion; limb (b) is what would catch the tier-changing case, and
      the two are kept apart so that neither can be quoted as the other.

THE WRITE-BACK IS INJECTABLE, and that is what makes the control falsifiable. A
control whose only positive is a value change has not been shown to test the
write-back path at all: any comparison catches a value change. `write_back`
takes the same shape as the real one and the suite supplies variants that
preserve every value and change something else.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping, Sequence

import numpy as np
import pandas as pd

from .availability import AvailabilityModel, ProbeError, _fast_fingerprint

CONTROL_ID = "probe_a_identity"
STRATEGY_ID = "identity"


@dataclass(frozen=True)
class InputCheck:
    """What the write-back did to one column of one perturbed frame."""
    frame: str
    column: str
    n_cells_written: int
    values_equal: bool
    dtype_before: str
    dtype_after: str
    index_equal: bool

    @property
    def invariant(self) -> bool:
        return (self.values_equal and self.index_equal
                and self.dtype_before == self.dtype_after)

    def why(self) -> str:
        if self.invariant:
            return "unchanged"
        parts = []
        if not self.values_equal:
            parts.append("values changed")
        if self.dtype_before != self.dtype_after:
            parts.append("dtype %s -> %s, which moves the promotion status and "
                         "with it the tier every real finding is reported at"
                         % (self.dtype_before, self.dtype_after))
        if not self.index_equal:
            parts.append("index replaced")
        return "; ".join(parts)


@dataclass
class IdentityControlResult:
    side: str
    n_cohorts: int
    determinism_ok: bool = True
    compatibility_ok: bool = True
    output_identical: bool | None = True     # None once the comparison is void
    moved_columns: tuple = ()
    input_checks: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    base_columns: tuple = ()
    # SC-5(f)'s route, computed from the baseline the control already built --
    # a second build to scan for the sentinel would cost as much as the control.
    base_sentinel_columns: dict = field(default_factory=dict)

    @property
    def input_invariant(self) -> bool:
        return all(c.invariant for c in self.input_checks)

    def verdict(self) -> str:
        """The REGISTERED limb only. Limb (b) is reported beside it, never folded in.

        THE STATE VOCABULARY IS THE REGISTERED ONE (section 8.2): the not-run
        reasons are crash, alignment, compatibility, determinism and
        control_artifact, and no other. `not_applicable` covers a combination
        with no eligible cohort selected, per section 6.6's resolution order.
        None of these is ever displayed in a way mistakable for a pass.
        """
        if not self.determinism_ok:
            return "could_not_run(determinism)"
        if not self.n_cohorts:
            return "not_applicable"
        if not self.compatibility_ok:
            return "could_not_run(compatibility)"
        return "silent" if self.output_identical else "control_artifact"

    @property
    def scoreable(self) -> bool:
        """Whether criterion 4 has an answer here. A state that is not scoreable
        is NOT a pass -- section 8.2 forbids displaying it as one."""
        return self.verdict() in ("silent", "control_artifact")


def identity_write_back(frame: pd.DataFrame, column: str, mask) -> None:
    """The real one: write the selected cells back, through the same assignment
    path the perturbation uses. `.loc` with a positional array, so the write is
    exercised rather than optimised away by assigning the Series to itself."""
    frame.loc[mask, column] = frame.loc[mask, column].to_numpy()


def run_identity_control(
    raw: Mapping[str, pd.DataFrame],
    build: Callable[[Mapping[str, pd.DataFrame]], pd.DataFrame],
    model: AvailabilityModel,
    side: str,
    cohort_stride: int = 97,
    max_cohorts: int = 400,
    write_back: Callable[[pd.DataFrame, str, object], None] = identity_write_back,
) -> IdentityControlResult:
    """Section 6.11 control 2, on the frame the probe actually perturbs.

    THE MASK IS THE PROBE'S OWN. Same stride, same cap, same aggregate frames,
    same key handling -- including the timezone alignment, because a control run
    over a mask that never matched would be a silence about the harness.
    """
    res = IdentityControlResult(side=side, n_cohorts=0)

    base = build(dict(raw))
    res.base_columns = tuple(base.columns)
    res.base_sentinel_columns = sentinel_columns(base)
    base2 = build(dict(raw))
    if not base.equals(base2):
        res.determinism_ok = False
        res.notes.append("the builder is not deterministic across two clean runs; "
                         "no control result from it could be attributed")
        return res

    dcol = model.decision_column
    if dcol not in base.columns:
        raise ProbeError("the decision column %r is not in the built output" % dcol)
    d = pd.to_datetime(base[dcol])
    seconds = pd.Index(sorted(d.dt.floor("s").unique()))
    picked = seconds[::cohort_stride][:max_cohorts]
    res.n_cohorts = len(picked)
    if res.n_cohorts == 0:
        return res
    picked_set = set(picked)

    control = {k: v.copy() for k, v in raw.items()}
    touched = 0
    for fname, keycol in model.aggregate_frames.items():
        if fname not in control or control[fname] is None:
            res.notes.append("aggregate frame %r absent from raw; not written" % fname)
            continue
        f = control[fname]
        if keycol not in f.columns:
            raise ProbeError("frame %r has no key column %r" % (fname, keycol))
        key = pd.to_datetime(f[keycol])
        if getattr(key.dt, "tz", None) is not None:
            key = key.dt.tz_convert("UTC").dt.tz_localize(None) if d.dt.tz is None \
                else key.dt.tz_convert(d.dt.tz)
        elif d.dt.tz is not None:
            key = key.dt.tz_localize(d.dt.tz)
        # A POSITIONAL MASK, NOT AN INDEX-ALIGNED ONE. A write-back that
        # replaces the frame's index -- one of the faults this control exists to
        # catch -- leaves an index-aligned boolean Series pointing at labels that
        # no longer exist, and the NEXT column's write raises instead of being
        # measured. The control would then report a crash where the truth is a
        # detected fault. The mask is over the frame's rows, so it is carried as
        # an array over rows.
        mask = key.dt.floor("s").isin(picked_set).to_numpy()
        if not mask.any():
            raise ProbeError(
                "frame %r matched NO selected second. A control run over a mask "
                "that never matched is a silence about the harness, not about "
                "the write-back path." % fname)
        num = [c for c in f.columns
               if c != keycol and pd.api.types.is_numeric_dtype(f[c])]
        n_rows_before = len(f)
        for c in num:
            before = raw[fname][c]
            idx_before = f.index
            dtype_before = str(f[c].dtype)
            write_back(f, c, mask)
            after = f[c]
            res.input_checks.append(InputCheck(
                frame=fname, column=c, n_cells_written=int(mask.sum()),
                values_equal=bool(
                    len(after) == len(before)
                    and np.array_equal(after.to_numpy(), before.to_numpy(),
                                       equal_nan=True)),
                dtype_before=dtype_before, dtype_after=str(after.dtype),
                index_equal=bool(f.index.equals(idx_before))))
            if len(f) != n_rows_before:
                # A WRITE-BACK THAT CHANGES THE ROW COUNT IS RECORDED, NOT
                # RAISED. The mask is positional over the frame's rows, so once
                # the row count moves it no longer describes the frame and the
                # NEXT column's write would raise -- reporting a crash where the
                # truth is a detected fault. That is the failure mode the
                # positional mask was adopted to avoid, in its other form.
                res.notes.append(
                    "the write-back changed frame %r from %d to %d rows; the "
                    "mask no longer describes it, so the remaining columns of "
                    "this frame were not written. Recorded, not raised."
                    % (fname, n_rows_before, len(f)))
                break
        touched += int(mask.sum())
        control[fname] = f
    if touched == 0:
        raise ProbeError("no aggregate cells were selected; the control would "
                         "report a silence about itself")
    res.notes.append("wrote %d aggregate cell selection(s) back across %d second(s)"
                     % (touched, res.n_cohorts))

    after_frame = build(control)
    if len(after_frame) != len(base) or list(after_frame.columns) != list(base.columns):
        # A SHAPE OR COLUMN-SET CHANGE IS A COMPATIBILITY FAILURE, NOT A FINDING
        # AND NOT A CONTROL ARTIFACT. R195 §3, settled from the registration.
        #
        # Section 6.11's third control owns shape and index: "Confirm output
        # shape and index match the baseline... every comparison after that is
        # meaningless, INCLUDING ONES THAT LOOK CLEAN. A failure discards that
        # probe's result." Section 6.11's head is what rules out the other
        # reading: the three controls' failures "are recorded per section 7.7's
        # two-level scheme, NEVER AS FINDINGS". And section 6.6's precedence puts
        # `compatibility` ahead of `control_artifact`, which is the enum for a
        # probe that did not validly happen.
        #
        # The consequence is NOT that the control passed. Section 8.2: no not-run
        # state is displayed in a way mistakable for a pass. Criterion 4 has no
        # answer on this side, `scoreable` is False, and that is reported as
        # itself.
        res.compatibility_ok = False
        res.output_identical = None            # the comparison is void, not clean
        res.moved_columns = ()
        res.notes.append(
            "shape or column set changed under the identity write: %s -> %s. "
            "Every comparison past this point is meaningless, including one that "
            "looks clean, so the result is discarded rather than read."
            % ((len(base), len(base.columns)),
               (len(after_frame), len(after_frame.columns))))
        return res

    moved = []
    for c in base.columns:
        a_ = base[c].astype("string").fillna("<NA>").to_numpy()
        b_ = after_frame[c].astype("string").fillna("<NA>").to_numpy()
        if (a_ != b_).any():
            moved.append(c)
    res.moved_columns = tuple(sorted(moved))
    res.output_identical = not moved
    return res


# ---------------------------------------------------------------------------
# SC-5(f)'s second route: the declared sentinel
# ---------------------------------------------------------------------------
#
# "An as-built artefact of the fixture that is present identically on every side
# is data content, not a finding: it cannot differentiate the sides, and a
# detector firing on it has produced a false positive under the identity
# control." The signature is the declaration's, enumerated ex ante, and it is
# NEVER extended in response to what fires.

SENTINEL_WRAP = 2 ** 32
SENTINEL_MAX_K = 1 << 20      # k is a trade size; this is generous and fixed


def sentinel_columns(frame: pd.DataFrame, wrap: int = SENTINEL_WRAP,
                     max_k: int = SENTINEL_MAX_K) -> dict[str, int]:
    """Columns carrying values matching the declared signature.

    The signature, from the declaration: magnitude approximately 2**32 - k for a
    trade of size k; the sign; the 2**32 wrap. A column qualifies when it holds
    at least one finite value whose magnitude lies in [wrap - max_k, wrap).
    """
    lo, hi = wrap - max_k, wrap
    out: dict[str, int] = {}
    for c in frame.columns:
        s = frame[c]
        if not pd.api.types.is_numeric_dtype(s) or pd.api.types.is_bool_dtype(s):
            continue
        v = pd.to_numeric(s, errors="coerce").to_numpy(dtype="float64", na_value=np.nan)
        n = int(np.sum((np.abs(v) >= lo) & (np.abs(v) < hi)))
        if n:
            out[c] = n
    return out


def sentinel_false_positives(moved_columns: Sequence[str],
                             sentinel_a: Mapping[str, int],
                             sentinel_b: Mapping[str, int]) -> list[str]:
    """Moved columns that carry the sentinel identically on BOTH sides.

    Identical presence on every side is what makes an artefact a sentinel: it
    cannot differentiate the sides, so a firing on it is a false positive under
    this control. A column carrying it on one side only is NOT a sentinel and is
    not excused here.
    """
    return sorted(c for c in moved_columns
                  if c in sentinel_a and c in sentinel_b)
