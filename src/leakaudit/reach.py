"""How far a corruption propagates through THIS builder, measured. R267 §2.

Two features carried the same sentence: *clearing the floor is not sufficiency,
because the builder's lookback is not in the model.* D's padding and the stride
floor both stopped where the declaration stopped. But this tool's whole claim is
that **runtime perturbation measures what declarations cannot**, and the
builder's reach is exactly such a quantity — so it is measured here instead of
being declared away in two places.

THE MEASUREMENT. Perturb one probed second `F` in an otherwise clean build,
rebuild once, and take the largest `d(i) - F` over every row that moved. That is
how far forward a corruption of `F` propagates through this builder. It needs no
model and makes no assumption about what the pipeline does: the rows either
moved or they did not.

  * ONE REBUILD PER SAMPLED SECOND, and one clean build shared by all of them.
    The row comparison is `availability.py`'s own fingerprint over the whole
    output, so nothing here is band-limited.
  * THE SAME PERTURBATION THE PROBE APPLIES. `perturb_cells` is imported rather
    than reimplemented; a weaker perturbation would under-report on exactly the
    integer and boolean columns its branches exist for.

WHAT k SAMPLES ESTABLISH, AND WHAT THEY DO NOT. The result is a **lower bound**
on reach and is reported as one. A path through the builder that no sampled
second exercised is the residual that remains, and it does not shrink to nothing
at any finite k.

CENSORING, WHICH THE MEASUREMENT FINDS RATHER THAN ASSUMES. A corruption at `F`
cannot be observed moving rows that do not exist, so a sample close to the end
of the frame reports the distance to the last row rather than the builder's
reach. **Measured at R267 on a builder with a known 60-second lookback:** samples
at three quartiles returned 59.5s, 44.5s and 22.5s, and the last two exactly
equalled their distance to the final decision row. Head samples are censored the
other way, by warmup, where a rolling window is still filling.

So each sample is marked censored when its reach equals its distance to the last
decision row, and censoring only ever UNDER-reports — which is why the maximum
over samples remains a sound lower bound, and why a run whose samples are *all*
censored has measured nothing and says so rather than returning its largest
censored number as a reach.

Written with the Write tool per D2.1.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .availability import ProbeError, _fast_fingerprint, perturb_cells

#: Why three. Each sample costs one rebuild, and on the acceptance fixture a
#: rebuild is ~34.6 s, so k=3 is under two minutes once per audit. Below three
#: a single censored or warmup-truncated sample dominates the maximum; above it
#: the cost grows linearly while the bound improves only when a sample happens
#: to exercise a longer path. It is a cost choice, printed as one.
DEFAULT_SAMPLES = 3


class ReachError(ProbeError):
    """The reach control cannot answer, and says so rather than guessing."""


@dataclass
class ReachSample:
    second: pd.Timestamp
    cells: int
    reach: object = None            # pd.Timedelta, or None if nothing moved
    to_frame_end: object = None     # pd.Timedelta from this second to the last row
    censored: bool = False
    note: str = ""


@dataclass
class ReachResult:
    k: int
    samples: list = field(default_factory=list)
    seed: int = 0

    @property
    def uncensored(self) -> list:
        return [s for s in self.samples if s.reach is not None and not s.censored]

    @property
    def measured(self):
        """The lower bound on reach, or None when nothing uncensored was seen."""
        good = self.uncensored
        return max((s.reach for s in good), default=None)

    @property
    def all_censored(self) -> bool:
        return bool(self.samples) and not self.uncensored

    def note(self) -> str:
        if self.measured is not None:
            body = ("REACH (measured, not declared): a corruption of one second "
                    "moves rows up to %s later in this builder's output. "
                    "%d sample(s), %d usable, %d censored by the frame's end."
                    % (self.measured, self.k, len(self.uncensored),
                       len(self.samples) - len(self.uncensored)))
        elif self.all_censored:
            body = ("REACH NOT MEASURED: all %d sample(s) were censored by the "
                    "frame's end -- each moved rows right up to the last one, so "
                    "what stopped the propagation was the data running out and "
                    "not the builder. No reach is claimed." % self.k)
        else:
            body = ("REACH NOT MEASURED: no sampled second moved any row, so "
                    "this builder showed no propagation at all on the sampled "
                    "seconds. That is not a reach of zero.")
        return (body + " THIS IS A LOWER BOUND: a path no sampled second "
                "exercised would not appear here, and %d samples do not become "
                "all of them." % self.k)


def _corrupt_one(raw, model, second, seed) -> tuple:
    """Perturb every modelled aggregate cell whose key floors to `second`."""
    rng = np.random.default_rng(seed)
    out = {k: v.copy() for k, v in raw.items()}
    cells = 0
    for fname, keycol in sorted(model.aggregate_frames.items()):
        f = out.get(fname)
        if f is None or keycol not in getattr(f, "columns", ()):
            continue
        keys = pd.to_datetime(f[keycol], errors="coerce").dt.floor("s")
        mask = (keys == second).to_numpy()
        if not mask.any():
            continue
        # THE SAME COLUMN SET THE PROBE PERTURBS: numeric, excluding the key.
        # A first version took every column and handed `released_at` -- a
        # datetime -- to the float branch, which raised. The probe never had
        # that bug because it selects numeric columns first, and reach measuring
        # a WIDER set than the probe corrupts would report propagation the
        # probe cannot cause.
        num = [c for c in f.columns
               if c != keycol and pd.api.types.is_numeric_dtype(f[c])]
        for c in num:
            n = int(mask.sum())
            perturb_cells(f, c, mask, n, rng)
            cells += n
        out[fname] = f
    return out, cells


def sample_seconds(seconds, k) -> list:
    """k seconds spread over the eligible set, deterministically.

    Evenly spaced rather than random: a random sample would need a printed seed
    to be reproducible, and an audit that cannot be re-run is not evidence. The
    HEAD is skipped where there is room, because a rolling window still filling
    there truncates propagation and a head sample under-reports.
    """
    secs = list(seconds)
    if not secs or k <= 0:
        return []
    if len(secs) <= k:
        return secs
    lo = 1 if len(secs) > k + 1 else 0
    span = len(secs) - lo
    return [secs[lo + (i * span) // (k + 1)] for i in range(1, k + 1)]


def measure_reach(raw, build, model, base, dcol, *, k=DEFAULT_SAMPLES,
                  seed=20260828) -> ReachResult:
    """Measure the builder's forward reach. One rebuild per sampled second."""
    res = ReachResult(k=k, seed=seed)
    if k <= 0:
        return res
    d = pd.to_datetime(base[dcol])
    d_np = d.to_numpy()
    if len(d_np) == 0:
        return res
    last = pd.Timestamp(d_np.max())
    fb = _fast_fingerprint(base).to_numpy()

    for i, F in enumerate(sample_seconds(sorted(d.dt.floor("s").unique()), k)):
        corrupt, cells = _corrupt_one(raw, model, F, seed + i)
        s = ReachSample(second=F, cells=cells, to_frame_end=last - F)
        if cells == 0:
            s.note = "no modelled aggregate cell falls in this second"
            res.samples.append(s)
            continue
        after = build(corrupt)
        if len(after) != len(base) or list(after.columns) != list(base.columns):
            raise ReachError(
                "the corrupted build changed shape (%s -> %s) while measuring "
                "reach, so rows cannot be compared positionally"
                % ((len(base), len(base.columns)),
                   (len(after), len(after.columns))))
        moved = fb != _fast_fingerprint(after).to_numpy()
        if not moved.any():
            s.note = "nothing moved"
            res.samples.append(s)
            continue
        s.reach = pd.Timestamp(d_np[moved].max()) - F
        # The frame ran out, not the builder. Only ever an under-report, which
        # is why the maximum over samples is still a sound lower bound.
        s.censored = s.reach >= s.to_frame_end
        if s.censored:
            s.note = ("moved rows right up to the last one, so the frame's end "
                      "stopped it rather than the builder")
        res.samples.append(s)
    return res


def _too_short(what, declared, result) -> str:
    return (
        "%s is %s and THIS BUILDER REACHES %s -- measured, not derived. A "
        "corruption of one second was seen moving rows %s later in the output, "
        "so %s of %s does not clear the propagation it has to clear. This is a "
        "LOWER bound from %d sample(s); the real reach can only be longer. "
        "Raise %s above %s, or re-run with more samples if you believe the "
        "measurement caught a path your audit will not."
        % (what, declared, result.measured, result.measured, what, declared,
           result.k, what, result.measured))


def check_stride_separation(separation, result) -> None:
    """Refuse cohorts closer together than the measured reach. R267 §2(d).

    TAKES THE MEASURED SEPARATION, NOT THE STRIDE. `cohort_stride` counts index
    positions in the set of seconds the data carries, so on a frame with gaps a
    stride of 97 is not 97 seconds. What has to exceed the reach is the smallest
    gap between two seconds actually corrupted, and comparing a count against a
    duration would be comparing two different quantities.
    """
    if result is None or result.measured is None or separation is None:
        return
    declared = pd.Timedelta(separation)
    if declared <= result.measured:
        raise ReachError(_too_short(
            "the smallest gap between corrupted cohorts", declared, result))


def check_padding(padding, result) -> None:
    """Refuse a declared slice padding at or below the measured reach."""
    if result is None or result.measured is None or padding is None:
        return
    declared = pd.Timedelta(padding)
    if declared <= result.measured:
        raise ReachError(_too_short("the declared padding", declared, result))
