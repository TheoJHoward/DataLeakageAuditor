"""`DESIGN.md` §5.3 -- auditing a slice, with padding.

    Slicing shifts window warmup, manufacturing artifacts at the head and
    masking leakage deeper in. Any slice carries padding of at least the
    maximum window length before the first probed cohort, present in the
    data, excluded from probing, and reported. Where the maximum window is
    unknown, `audit()` requires `max_window=`; a slice without declared
    padding is refused, not silently run.

WHERE THE THRESHOLD COMES FROM, ESTABLISHED BEFORE THE REFUSAL WAS WRITTEN.
R255 §1 asked whether the required padding is derivable from the availability
model, and required the answer before any refusal existed, on the grounds that a
refusal comparing against an invented number is worse than no refusal. It was
measured off the tree rather than reasoned about. The answer is that the model
determines a FLOOR and does not determine the REQUIREMENT, and those two facts
have different consequences, so they are kept apart here.

WHAT THE MODEL DETERMINES -- the founded terms, each a single declared value:

  `AvailabilityModel.window`   ONE Timedelta for ALL `aggregate_frames`. The
                               model has exactly four fields and this is the
                               only duration among them; there is no per-frame
                               window, so "the max over the frames" is the value
                               itself. A cell is available at `floor(key) +
                               window`, so a bucket at the slice edge whose span
                               is truncated is an INCOMPLETE bucket, and that is
                               founded arithmetic, not a guess.
  a DECLARED `bar_duration`    Not a model field at all -- a sibling argument to
                               `run_probe_a`, default `None`. It is founded only
                               on the DECLARED route.

WHAT THE MODEL DOES NOT DETERMINE, and why each is not a term:

  an INFERRED `bar_duration`   With no declaration, `modes.py` infers the gap to
                               the next timestamp PER ROW. There is no single
                               number: `_infer_bar_duration` reports `agrees`
                               and the tool already declines to name a value
                               when it is False. A floor cannot be built out of
                               a quantity the tool refuses to summarise.
  `at_source_timestamp`        The instant is a value read out of a named
  `explicit`                   column. The lookback it implies is data, not a
                               declaration, and varies row to row.
  `availability_fn`            Arbitrary user code. Nothing is derivable.
  THE PIPELINE'S OWN LOOKBACK  THE DECISIVE ONE. Padding exists because slicing
                               truncates what `build` can READ. The availability
                               model says when a cell became KNOWABLE; it says
                               nothing about how far back the builder reaches.
                               `build` is an opaque `Callable` in the probe's
                               signature. A rolling 30-day mean has a 30-day
                               lookback under a 1-second `window`, and no field
                               on the model moves when it changes.

SO THE REQUIREMENT IS NOT DERIVABLE, WHICH IS WHY `DESIGN.md` §5.3 REQUIRES THE
USER TO DECLARE IT. That is not a gap in this module; it is the design's own
answer, and it is the reason the primary refusal here is a PRESENCE test --
`padding` was not declared -- which needs no threshold at all and so cannot rest
on an unfounded one.

THE FLOOR IS A SEPARATE, WEAKER CHECK AND IS LABELLED AS ONE. A declared padding
below `model.window` leaves the aggregate arithmetic the model itself specifies
incomplete, so it is refusable on the model's own terms. Passing the floor is
NOT evidence the padding is sufficient -- the binding quantity is the builder's
reach and this module cannot see it. `SlicePlan.floor_is_not_sufficiency` says so
in the object, and the note the probe prints says so to the user, because a check
that is easy to mistake for a stronger one is the failure this session kept
finding.

SCOPE, STATED SO IT IS NOT MISTAKEN FOR MORE. This governs the slice the tool
is ASKED for, via `slice_from=`. A caller who truncates their frames before
calling has performed a slice this tool cannot distinguish from data that simply
starts late, and no refusal here reaches them. `DESIGN.md` §5.3 has the same
scope, and naming the boundary is the whole of what can be done about it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import pandas as pd

# The padding was never declared, as distinct from a padding of zero, which is a
# declaration this module can check and refuse. The two states are merged by any
# `None`-as-default and the merge is the defect: `decision_column` carries the
# same sentinel in `availability.py` for the same reason. It is DEFINED there,
# beside `NOT_SET`, because `run_probe_a`'s signature default needs it and that
# module cannot import this one at the top without a cycle. Re-exported here so
# a caller reading the slice rule finds it in the module that owns the rule.
from .availability import NOT_DECLARED, ProbeError


class SliceError(ProbeError):
    """A slice was asked for and cannot be audited as asked.

    A `ProbeError` subclass so the CLI boundary already catches it and exits
    non-zero (`EXIT_USAGE`) without inventing a verdict. R255 §2: insufficient
    padding REFUSES. It does not warn and continue, because a warned-past run
    still emits a verdict over the edge cohorts, and that verdict is the thing
    §5.3 says is wrong.
    """


@dataclass(frozen=True)
class SlicePlan:
    """What was asked, what was founded, and what it does not establish."""

    slice_from: pd.Timestamp
    padding: pd.Timedelta
    required_start: pd.Timestamp
    floor: pd.Timedelta
    floor_driver: str
    frame_starts: Mapping[str, pd.Timestamp]
    #: Modelled frames the data check could NOT read, with why. The
    #: padding-is-present claim does not cover these, and it says so rather
    #: than narrowing in silence.
    unchecked_frames: Mapping[str, str] = None

    #: Reading `floor` as "and therefore the padding is enough" is the mistake
    #: this field exists to block. See the module docstring.
    floor_is_not_sufficiency: str = (
        "the floor is derived from `AvailabilityModel.window` and a declared "
        "`bar_duration` only; the builder's own lookback is not visible to this "
        "tool, so clearing the floor does NOT establish the padding is "
        "sufficient"
    )


def _as_timedelta(value, what: str) -> pd.Timedelta:
    try:
        out = pd.Timedelta(value)
    except (ValueError, TypeError) as e:
        raise SliceError("%s is not a duration: %r (%s)" % (what, value, e))
    if out is pd.NaT or pd.isna(out):
        raise SliceError("%s is not a duration: %r" % (what, value))
    return out


def model_padding_floor(model, declared_bar_duration=None) -> tuple:
    """The largest padding the availability model itself FOUNDS, and its driver.

    R255 §1's second branch shape -- the max over the terms, naming which one
    drove it -- applied to the founded terms only. The unfounded ones are
    enumerated in the module docstring and deliberately absent here: including
    an inferred `bar_duration` would put a per-row quantity with no centre into
    a scalar comparison.
    """
    floor = _as_timedelta(model.window, "`AvailabilityModel.window`")
    driver = "`AvailabilityModel.window` (one value for every aggregate frame)"
    if declared_bar_duration is not None:
        bd = _as_timedelta(declared_bar_duration, "the declared `bar_duration`")
        if bd > floor:
            floor, driver = bd, "the DECLARED `bar_duration`"
    return floor, driver


def frame_starts(raw: Mapping[str, pd.DataFrame], model) -> tuple:
    """Earliest key instant per MODELLED aggregate frame, and what was SKIPPED.

    Frames the model does not describe are not consulted: the probe already
    reports them as `unmodelled_frames`, and a start time read off a frame whose
    key column this module had to guess would be a number with no provenance.

    THE SKIPPED SET IS RETURNED, NOT SWALLOWED. "The padding is present in the
    data" is an absence claim -- no frame reaches back less far than declared --
    and an absence claim carries its population. A frame the model declares and
    the caller did not supply, or whose key column is missing or unparseable, is
    a frame this check said nothing about; dropping it silently would make the
    claim quietly narrower than it reads, which is this session's most-repeated
    defect. It is reported with the plan and printed with the run.
    """
    out, skipped = {}, {}
    for frame, keycol in sorted(model.aggregate_frames.items()):
        df = raw.get(frame)
        if df is None:
            skipped[frame] = "declared by the model and not supplied to the probe"
            continue
        if keycol not in getattr(df, "columns", ()):
            skipped[frame] = "key column %r is not in the frame" % keycol
            continue
        keys = pd.to_datetime(df[keycol], errors="coerce").dropna()
        if len(keys) == 0:
            skipped[frame] = ("key column %r holds no parseable timestamp"
                              % keycol)
            continue
        out[frame] = keys.min()
    return out, skipped


def plan_slice(*, raw, model, slice_from, padding=NOT_DECLARED,
               declared_bar_duration=None) -> SlicePlan:
    """Refuse the slice, or return the plan that describes it.

    Every branch below raises rather than warns. R255 §2, and `DESIGN.md` §5.3's
    own words: refused, NOT silently run.
    """
    start = pd.Timestamp(slice_from)
    if start is pd.NaT or pd.isna(start):
        raise SliceError("`slice_from` is not a timestamp: %r" % (slice_from,))

    # THE PRIMARY REFUSAL, AND THE ONLY ONE THAT NEEDS NO THRESHOLD.
    if isinstance(padding, str) and padding == NOT_DECLARED:
        raise SliceError(
            "a slice was asked for (`slice_from=%s`) and no padding was "
            "declared. DESIGN.md section 5.3: a slice without declared padding "
            "is refused, not silently run -- slicing shifts window warmup, so "
            "the cohorts at the head of the slice are computed from a truncated "
            "history and leakage there is MASKED. The required padding is the "
            "maximum lookback your builder reads, which this tool cannot derive "
            "from the availability model: the model describes when a cell "
            "became knowable, not how far back `build` reaches. Declare it as "
            "`--padding 30D` at the command line, or `padding='30D'` in the "
            "library. It must be at least %s, which is what the model does "
            "found (%s)."
            % ((start,) + model_padding_floor(model, declared_bar_duration)))
    if padding is None:
        raise SliceError(
            "`padding=None` is not a declaration. Pass a duration, or drop "
            "`--slice-from` / `slice_from=` if the whole frame is being "
            "audited.")

    pad = _as_timedelta(padding, "`padding`")
    if pad < pd.Timedelta(0):
        raise SliceError("`padding` is negative: %s" % pad)

    floor, driver = model_padding_floor(model, declared_bar_duration)
    if pad < floor:
        raise SliceError(
            "the declared padding %s is below the floor the availability model "
            "itself founds, %s, driven by %s. Below it the aggregate at the "
            "slice edge spans a truncated bucket, so its value at the first "
            "probed cohort is not the value the unsliced run would compute. "
            "Clearing this floor would not establish the padding is SUFFICIENT "
            "-- the builder's own lookback is not visible here -- but falling "
            "under it is refusable on the model's own arithmetic."
            % (pad, floor, driver))

    required_start = start - pad
    starts, skipped = frame_starts(raw, model)
    short = {f: s for f, s in starts.items() if s > required_start}
    if short:
        raise SliceError(
            "the declared padding of %s before %s requires data from %s, and "
            "these modelled frames do not reach back that far: %s. The padding "
            "must be PRESENT IN THE DATA (DESIGN.md section 5.3) -- declaring "
            "it without supplying it is the same truncated history the "
            "declaration exists to prevent."
            % (pad, start, required_start,
               ", ".join("%s starts %s" % (f, s) for f, s in sorted(short.items()))))

    return SlicePlan(slice_from=start, padding=pad, required_start=required_start,
                     floor=floor, floor_driver=driver, frame_starts=starts,
                     unchecked_frames=skipped)


def split_seconds(seconds, plan: SlicePlan) -> tuple:
    """Split the candidate seconds into (probed, context).

    R255 §3 and `DESIGN.md` §8: the context seconds are present in the data so
    the builder computes correctly over them, and they are NEVER probed. A
    second that was not probed produced no evidence, so it cannot be reported
    as audited-clean -- its outcome is `not_applicable`, which is what
    `context_note` states and what the probe prints.
    """
    probed = [s for s in seconds if s >= plan.slice_from]
    context = [s for s in seconds if s < plan.slice_from]
    return probed, context


def context_note(plan: SlicePlan, n_context: int) -> str:
    """The line the probe prints about the padding rows. Never says clean."""
    return (
        "SLICE: probing cohorts at or after %s, with %s of declared padding "
        "back to %s. %d second(s) fall in the padding and are NOT PROBED -- "
        "they are context the builder reads, not subjects. Their outcome is "
        "`not_applicable`, NOT `observed_silence` and not clean: no probe ran "
        "over them, so this run carries no evidence about them. The padding "
        "clears the model-founded floor of %s (%s); that floor does not "
        "establish sufficiency, because the builder's own lookback is not "
        "visible to this tool."
        % (plan.slice_from, plan.padding, plan.required_start, n_context,
           plan.floor, plan.floor_driver)
        + (
            " THE PADDING-IS-PRESENT CHECK DID NOT COVER %d modelled frame(s): "
            "%s. Nothing here claims those carry the declared padding."
            % (len(plan.unchecked_frames),
               "; ".join("%s -- %s" % kv
                         for kv in sorted(plan.unchecked_frames.items())))
            if plan.unchecked_frames else ""))
