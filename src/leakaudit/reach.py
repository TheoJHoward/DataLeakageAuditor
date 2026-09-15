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
  * THE SAME COLUMN SET THE PROBE PERTURBS: numeric, excluding the key. The first
    version took every column, handed a datetime to the float branch and crashed;
    and a control perturbing a WIDER set than the probe reports propagation the
    probe cannot cause, so it would refuse strides that are safe.

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

from .availability import (ProbeError, _fast_fingerprint, corrupt_cells,
                           to_decision_clock)

#: Why three. Each sample costs one rebuild, and on the acceptance fixture a
#: rebuild is ~34.6 s, so k=3 is under two minutes once per audit. Below three
#: a single censored or warmup-truncated sample dominates the maximum; above it
#: the cost grows linearly while the bound improves only when a sample happens
#: to exercise a longer path. It is a cost choice, printed as one.
DEFAULT_SAMPLES = 3

#: What a COMPLETE run measures at. R270 §2(a). k scales with what it protects:
#: a complete run's stride is this measurement plus one second, and it guards
#: an hour of passes on the acceptance fixture, so three rebuilds of evidence
#: for an hour of machine time was the wrong ratio. Ten rebuilds at ~35 s is
#: about six minutes there. The samples are spread across the frame by
#: `sample_seconds`, and `ReachResult.spread()` prints where they fell and what
#: each one saw. Still a lower bound; a larger k only makes it a better one.
COMPLETE_SAMPLES = 10


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
    rows: object = None             # the reach in ROWS, R272 §2(c)
    cells_by_frame: dict = field(default_factory=dict)


@dataclass
class ReachResult:
    k: int
    samples: list = field(default_factory=list)
    seed: int = 0
    frames: tuple = ()

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
        body = _coverage_prefix(self, "second") + body
        return (body + " THIS IS A LOWER BOUND: a path no sampled second "
                "exercised would not appear here, and %d samples do not become "
                "all of them." % self.k)

    def spread(self) -> str:
        """Where the samples fell and what each saw. R270 §2(a).

        A maximum alone hides whether ten samples agreed or one outlier set it,
        and whether they covered the frame or bunched at one end. So every
        sample is listed with its second and its reach, and the usable ones'
        smallest and largest are printed beside the maximum the stride uses.
        """
        if not self.samples:
            return "REACH SPREAD: no samples were taken."
        secs = [s.second for s in self.samples]
        good = [s.reach for s in self.uncensored]
        rows = []
        for s in self.samples:
            if s.reach is None:
                what = s.note or "nothing moved"
            elif s.censored:
                what = "%s, CENSORED by the frame's end" % s.reach
            else:
                what = "%s, %s row(s)" % (s.reach, s.rows)
            rows.append("%s -> %s" % (s.second, what))
        summary = ("usable reach min %s, max %s" % (min(good), max(good))
                   if good else "no usable sample")
        return ("REACH SPREAD over %d sample(s), from %s to %s: %s. %d usable, "
                "%d censored, %d with no movement. Samples: %s."
                % (len(self.samples), min(secs), max(secs), summary, len(good),
                   sum(1 for s in self.samples if s.censored),
                   sum(1 for s in self.samples if s.reach is None),
                   "; ".join(rows)))


def _corrupt_one(raw, model, second, seed, decision):
    """Perturb every modelled cell whose key floors to `second`.

    THROUGH THE ONE ENTRY POINT, `availability.corrupt_cells`. R272 §1(a). Until
    R271 this function kept its own copy of the selection, and the copy compared
    a UTC-aware trades key against naive decision seconds: pandas answered
    all-False, no trades cell was ever corrupted, and every reach printed for the
    acceptance fixture -- 14 s, 15 s, 15.9997 s -- was the MBO frame's alone. The
    entry point aligns through `to_decision_clock`, refuses an aware/naive
    comparison, and counts cells per declared frame, which the result prints.
    """
    return corrupt_cells(raw, model, decision,
                         rng=np.random.default_rng(seed),
                         seconds={pd.Timestamp(second)})


def _rows_forward(decision, moved, position) -> int:
    """Rows, in decision-time order, from the first row at or after `position`
    to the furthest row that moved. The unit the stride's positions compare
    against (R272 §2(c)): with at most one row a second, rows never undercount
    positions."""
    ranks = decision.rank(method="first").to_numpy()
    first = int((decision < position).sum()) + 1
    return int(ranks[np.asarray(moved, dtype=bool)].max()) - first


def measured_rows(result):
    """The largest usable reach in ROWS, or None where none was seen."""
    rows = [s.rows for s in getattr(result, "uncensored", [])
            if getattr(s, "rows", None) is not None]
    return max(rows, default=None)


def frames_never_corrupted(result) -> tuple:
    """Declared frames with zero corrupted cells at EVERY sampled position."""
    samples = getattr(result, "samples", [])
    if not samples:
        return ()
    return tuple(f for f in getattr(result, "frames", ())
                 if all(s.cells_by_frame.get(f, 0) == 0 for s in samples))


def _coverage_prefix(result, unit: str) -> str:
    """Cells per declared frame, and which frames no measurement exists for.

    R272 §1(c). A declared frame that contributes no corrupted cell at a
    position is reported as such, and one that contributes none at EVERY
    position has no reach at all -- the number printed after this covers the
    other frames and is never a number about it.
    """
    frames = tuple(getattr(result, "frames", ()) or ())
    samples = getattr(result, "samples", [])
    if not frames or not samples:
        return ""
    k = len(samples)
    parts = []
    for f in frames:
        zero = sum(1 for s in samples if s.cells_by_frame.get(f, 0) == 0)
        if zero:
            parts.append("%s: 0 cells at %d of %d positions" % (f, zero, k))
        else:
            parts.append("%s: cells at %d of %d positions" % (f, k, k))
    text = "CELLS PER DECLARED FRAME: %s. " % "; ".join(parts)
    never = frames_never_corrupted(result)
    if never:
        text += ("NO REACH IS CLAIMED FOR %s: no sampled %s corrupted a cell of "
                 "%s, so nothing below is a measurement of %s. "
                 % (", ".join(never), unit,
                    "it" if len(never) == 1 else "them",
                    "it" if len(never) == 1 else "them"))
    return text


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
                  seed=20260828, at_seconds=None) -> ReachResult:
    """Measure the builder's forward reach. One rebuild per sampled second.

    `at_seconds` measures at NAMED seconds instead of spreading `k` across the
    frame, and `k` becomes their count. R270 §1(c): where a complete run's
    findings sit is where a reach longer than the sampled one would show, so
    that is where the reading of them as interference is tested.
    """
    chosen = (None if at_seconds is None
              else sorted({pd.Timestamp(s) for s in at_seconds}))
    if chosen is not None:
        k = len(chosen)
    res = ReachResult(k=k, seed=seed)
    res.frames = tuple(model.aggregate_frames)
    if k <= 0:
        return res
    d = pd.to_datetime(base[dcol])
    d_np = d.to_numpy()
    if len(d_np) == 0:
        return res
    last = pd.Timestamp(d_np.max())
    fb = _fast_fingerprint(base).to_numpy()
    if chosen is None:
        chosen = sample_seconds(sorted(d.dt.floor("s").unique()), k)

    for i, F in enumerate(chosen):
        corruption = _corrupt_one(raw, model, F, seed + i, d)
        corrupt, cells = corruption.frames, corruption.cells
        s = ReachSample(second=F, cells=cells, to_frame_end=last - F,
                        cells_by_frame=dict(corruption.cells_by_frame))
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
        s.rows = _rows_forward(d, moved, F)
        # The frame ran out, not the builder. Only ever an under-report, which
        # is why the maximum over samples is still a sound lower bound.
        s.censored = s.reach >= s.to_frame_end
        if s.censored:
            s.note = ("moved rows right up to the last one, so the frame's end "
                      "stopped it rather than the builder")
        res.samples.append(s)
    return res


#: How many block positions a run samples. R271 §2(c): ONE rebuild per audit on
#: a default run, a cost ruled and printed in the run's note. A complete run
#: samples `COMPLETE_SAMPLES` positions, because what it protects is hours.
BLOCK_SAMPLES = 1

#: When corrupting the whole history breaks the build, the block falls back to
#: this many seconds before the position, and a lookback longer than it cannot
#: show. The note says so whenever the fallback was used. R271 §2(a).
BLOCK_FALLBACK_SECONDS = 3600


@dataclass
class BlockSample:
    position: pd.Timestamp
    cells: int = 0
    reach: object = None            # pd.Timedelta, or None if nothing moved at or after
    to_frame_end: object = None
    censored: bool = False
    bound: object = None            # pd.Timedelta when the fallback block was used
    note: str = ""
    rows: object = None             # the block reach in ROWS, R272 §2(c)
    cells_by_frame: dict = field(default_factory=dict)


@dataclass
class BlockReachResult:
    """The block reach: the history before a position corrupted in one rebuild.

    R271 §2. The single-second reach asks how far ONE second's corruption moves
    the output. A median, a rank or a threshold can answer "nowhere" while its
    window is minutes, and a batched pass puts several corruptions inside that
    window. So every modelled cell at or before a sampled position is corrupted
    at once -- the probe's column set, its perturbation, its clock -- and the
    largest `d(i) - position` over rows that moved at or after it is read.
    """
    k: int
    samples: list = field(default_factory=list)
    seed: int = 0
    frames: tuple = ()

    @property
    def uncensored(self) -> list:
        return [s for s in self.samples if s.reach is not None and not s.censored]

    @property
    def measured(self):
        """The longest usable block reach, or None when none was seen."""
        return max((s.reach for s in self.uncensored), default=None)

    @property
    def all_censored(self) -> bool:
        """Movement was seen and every instance of it ran to the frame's end."""
        return (any(s.censored for s in self.samples)
                and not self.uncensored)

    @property
    def bounds(self) -> list:
        return sorted({s.bound for s in self.samples if s.bound is not None})

    def note(self) -> str:
        n_cens = sum(1 for s in self.samples if s.censored)
        if self.measured is not None:
            body = ("BLOCK REACH (measured, not declared): corrupting every "
                    "modelled cell at or before a sampled second moved rows up "
                    "to %s later in this builder's output -- the longest "
                    "lookback any feature showed, and what the stride floor has "
                    "to clear. %d sampled block position(s), %d usable, %d "
                    "censored by the frame's end."
                    % (self.measured, self.k, len(self.uncensored), n_cens))
        elif self.all_censored:
            body = ("BLOCK REACH NOT MEASURED: wherever corrupting the history "
                    "moved anything, the movement ran to the frame's last row, "
                    "so the data running out stopped it and not the builder's "
                    "lookback. %d sampled block position(s)." % self.k)
        else:
            body = ("BLOCK REACH NOT MEASURED: corrupting the history before %d "
                    "sampled block position(s) moved no row at or after them, so "
                    "no lookback showed. That is not a lookback of zero." % self.k)
        if self.bounds:
            body += (" THE BLOCK WAS BOUNDED at %s: the whole-history block broke "
                     "the build at %d position(s), so a lookback longer than %s "
                     "cannot show here."
                     % (", ".join(str(b) for b in self.bounds),
                        sum(1 for s in self.samples if s.bound is not None),
                        max(self.bounds)))
        body = _coverage_prefix(self, "block position") + body
        return body + (" THE RESIDUAL: a feature whose response to a "
                       "whole-history corruption is below resolution, and a "
                       "lookback that showed at none of %d sampled block "
                       "position(s)." % self.k)

    def spread(self) -> str:
        if not self.samples:
            return "BLOCK REACH SPREAD: no block positions were sampled."
        pos = [s.position for s in self.samples]
        good = [s.reach for s in self.uncensored]
        rows = []
        for s in self.samples:
            if s.reach is None:
                what = s.note or "nothing moved at or after it"
            elif s.censored:
                what = "%s, CENSORED by the frame's end" % s.reach
            else:
                what = "%s, %s row(s)" % (s.reach, s.rows)
            if s.bound is not None:
                what += " (block bounded at %s)" % s.bound
            rows.append("%s -> %s" % (s.position, what))
        summary = ("usable block reach min %s, max %s" % (min(good), max(good))
                   if good else "no usable position")
        return ("BLOCK REACH SPREAD over %d sample(s), from %s to %s: %s. %d "
                "usable, %d censored, %d with no movement. Positions: %s."
                % (len(self.samples), min(pos), max(pos), summary, len(good),
                   sum(1 for s in self.samples if s.censored),
                   sum(1 for s in self.samples if s.reach is None),
                   "; ".join(rows)))


def _corrupt_block(raw, model, position, seed, decision, after=None):
    """Perturb every modelled cell whose aligned key floors at or before
    `position`, and after `after` when the block is bounded -- through the one
    entry point, `availability.corrupt_cells`. R272 §1(a)."""
    return corrupt_cells(raw, model, decision,
                         rng=np.random.default_rng(seed),
                         through=position, after=after)


def measure_block_reach(raw, build, model, base, dcol, *, k=BLOCK_SAMPLES,
                        seed=20260828, at_seconds=None,
                        fallback_seconds=BLOCK_FALLBACK_SECONDS) -> BlockReachResult:
    """Measure the builder's block reach. One rebuild per position. R271 §2(a).

    THE FALLBACK. Corrupting a whole history can break a build that one second
    never would -- a shape guard, a type check, a validation. Then the block is
    the `fallback_seconds` before the position instead, the exception is kept
    in the sample's note, and the result's note states the bound: a lookback
    longer than it cannot show. If the bounded block breaks the build too, this
    raises rather than returning a number about nothing.
    """
    chosen = (None if at_seconds is None
              else sorted({pd.Timestamp(s) for s in at_seconds}))
    if chosen is not None:
        k = len(chosen)
    res = BlockReachResult(k=k, seed=seed)
    res.frames = tuple(model.aggregate_frames)
    if k <= 0:
        return res
    d = pd.to_datetime(base[dcol])
    d_np = d.to_numpy()
    if len(d_np) == 0:
        return res
    last = d.max()
    fb = _fast_fingerprint(base).to_numpy()
    if chosen is None:
        chosen = sample_seconds(sorted(d.dt.floor("s").unique()), k)

    def _shape_ok(after):
        return (len(after) == len(base)
                and list(after.columns) == list(base.columns))

    for i, F in enumerate(chosen):
        F = pd.Timestamp(F)
        s = BlockSample(position=F, to_frame_end=last - F)
        try:
            corruption = _corrupt_block(raw, model, F, seed + i, d)
            corrupt, s.cells = corruption.frames, corruption.cells
            s.cells_by_frame = dict(corruption.cells_by_frame)
            after = build(corrupt)
            if not _shape_ok(after):
                raise ReachError(
                    "the whole-history block changed the output's shape (%s -> "
                    "%s)" % (base.shape, getattr(after, "shape", None)))
        except Exception as exc:  # noqa: BLE001 -- kept, bounded, re-raised below
            s.bound = pd.Timedelta(seconds=fallback_seconds)
            s.note = ("the whole-history block broke the build (%s: %s), so the "
                      "block here is the %s before the position"
                      % (type(exc).__name__, exc, s.bound))
            corruption = _corrupt_block(raw, model, F, seed + i, d,
                                        after=F - s.bound)
            corrupt, s.cells = corruption.frames, corruption.cells
            s.cells_by_frame = dict(corruption.cells_by_frame)
            after = build(corrupt)
            if not _shape_ok(after):
                raise ReachError(
                    "the bounded %s block also changed the output's shape, so no "
                    "block reach can be measured by comparing rows positionally"
                    % s.bound)
        if s.cells == 0:
            s.note = "; ".join(x for x in (s.note, "no modelled cell at or before "
                                                   "this position") if x)
            res.samples.append(s)
            continue
        moved = fb != _fast_fingerprint(after).to_numpy()
        fwd = moved & (d >= F).to_numpy()
        if not fwd.any():
            s.note = "; ".join(x for x in (s.note, "nothing moved at or after "
                                                   "the position") if x)
            res.samples.append(s)
            continue
        s.reach = pd.Timestamp(d_np[fwd].max()) - F
        s.rows = _rows_forward(d, fwd, F)
        s.censored = s.reach >= s.to_frame_end
        if s.censored:
            s.note = "; ".join(x for x in (s.note, "moved rows right up to the "
                               "last one, so the frame's end stopped it") if x)
        res.samples.append(s)
    return res


def block_floor_rows(result):
    """The block reach in rows plus one, or None where none was measured."""
    m = measured_rows(result)
    return None if m is None else m + 1


def check_block_stride(stride, result) -> None:
    """Refuse a stride, in positions, below the block reach, in rows. R272 §2(c)."""
    fl = block_floor_rows(result)
    if fl is None or stride is None:
        return
    if int(stride) < fl:
        raise ReachError(
            "the stride is %d positions and THIS BUILDER'S BLOCK REACH IS %d "
            "row(s) (%s) -- corrupting the history before one second moved rows "
            "that far forward, at %d sampled block position(s) -- so cohorts "
            "fewer than %d positions apart put one cohort's corruption inside "
            "another's window, and the findings that produces cannot be told "
            "from real ones (D-V30A-114: 163,143 of them on a builder with no "
            "leak). The stride counts positions in the sorted decision seconds "
            "and the block reach counts rows, so the two compare like with like. "
            "Raise the stride to at least %d, or omit it and that floor is used."
            % (int(stride), measured_rows(result), result.measured, result.k,
               fl, fl))


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


def check_reach_stride(stride, result) -> None:
    """Refuse a stride, in positions, at or below the single-second reach, in
    rows. R272 §2(c).

    Until R272 the probe compared this reach in SECONDS against the smallest
    probed gap in seconds. Across an overnight gap one second's corruption
    reaches hours of clock and still only the rows of its window, so the seconds
    check refused strides the rows show to be safe -- and accepted, in the other
    direction, cohorts hours apart in clock and a few rows apart across the gap.
    """
    rows = measured_rows(result)
    if rows is None or not stride:
        return
    if int(stride) <= rows:
        raise ReachError(
            "the stride is %d positions and THIS BUILDER REACHES %d row(s) (%s) "
            "-- measured, not derived: a corruption of one second was seen moving "
            "rows that far forward, at %d sample(s). Cohorts that close put one "
            "cohort's corruption inside another's window. This is a LOWER bound; "
            "raise the stride above %d, or omit it and the floor is used."
            % (int(stride), rows, result.measured, result.k, rows))


def check_padding(padding, result) -> None:
    """Refuse a declared slice padding at or below the measured reach."""
    if result is None or result.measured is None or padding is None:
        return
    declared = pd.Timedelta(padding)
    if declared <= result.measured:
        raise ReachError(_too_short("the declared padding", declared, result))


def head_cutoff(raw, model, decision, result) -> tuple:
    """(cutoff, frame_start, reason) -- where a frame's head ends. R269 §2(b).

    THE REACH WAS FOR THIS. Reach is the builder's lookback measured from
    behaviour: a row at `d` reads back to `d - reach`. So a row deciding before
    `frame_start + reach` reads cells from before the frame begins -- cells that
    are not in the data handed to the probe and so can never be perturbed. Its
    silence is about cells nobody touched, and it is reported as INELIGIBLE, not
    as observed_silence. No declaration is needed to know this, which is the
    point: a plain frame carries no record of what it was cut from, and a
    measurement does not need one.

    `frame_start` is the LATEST start among the modelled aggregate frames, on the
    decision clock, because a row reads every frame and the frame that starts
    last is the one whose head it reaches past first. Frames the model does not
    describe are not consulted, the same rule `slicing.frame_starts` follows.

    Returns (None, None, reason) when there is nothing to measure against, and
    the reason says the residual is then total rather than implying a head of
    zero.
    """
    from .availability import to_decision_clock

    measured = getattr(result, "measured", None)
    k = getattr(result, "k", 0)
    if measured is None:
        return None, None, (
            "HEAD OF FRAME NOT ASSESSED: the reach was not measured, so how far "
            "a row's lookback reaches past the frame's first row is unknown, and "
            "every silence near the start of the frame carries that residual in "
            "full.")
    starts = []
    for fname, keycol in sorted(model.aggregate_frames.items()):
        f = raw.get(fname)
        if f is None or keycol not in getattr(f, "columns", ()):
            continue
        keys = pd.to_datetime(f[keycol], errors="coerce").dropna()
        if len(keys):
            starts.append(to_decision_clock(
                keys, decision, decision_timezone=model.decision_timezone,
                what="frame %r, key %r" % (fname, keycol)).min())
    if not starts:
        return None, None, ("HEAD OF FRAME NOT ASSESSED: no modelled frame has a "
                            "readable key to take its first row from.")
    frame_start = max(starts)
    cutoff = frame_start + measured
    return cutoff, frame_start, (
        "lookback exceeds the frame's head; cells before the frame cannot be "
        "probed. Rows deciding before %s -- the frame's first row at %s plus the "
        "measured reach of %s -- read back past it, so no silence is claimed for "
        "them. The reach is a LOWER BOUND from %d sample(s): a lookback that "
        "showed in none of %d samples is the residual that remains."
        % (cutoff, frame_start, measured, k, k))
