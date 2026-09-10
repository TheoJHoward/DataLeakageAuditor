"""L2a -- the label probe. `PREREG.md` §4 row L2a, §2.4, §4.2; `DESIGN.md` §2.7.

WHAT IT ASKS, in one sentence: does the built output depend on label values the
declared label availability says had not yet been realized at the row's decision
time?

THE REGISTERED ROW, quoted, because this is a registered detector implemented
after the registration closed and the registration governs it:

    | L2a | Features from unavailable label values | PROVEN / REVIEW per §3 |
    Availability-restricted label perturbation | callable + label column +
    (temporal: `label_availability`; non-temporal: §2.5 policy) |

THE LABEL'S CLOCK IS ITS OWN, and that is what makes this a second probe rather
than a column of the first. `PREREG.md` §2.4:

    a(y_j) = label timestamp + label horizon + publication delay

All three terms are user-declared, as ONE declaration. No profile may default any
term, and the publication delay defaults to zero ONLY when the user supplies the
declaration -- a missing declaration is not a declaration with a zero in it.

ONE RULE, TWO PROBES. What a moved row MEANS is `availability.classify_cohorts`,
shared with L3.1 and not reimplemented here. R261 §1 repaired that rule after
R260 §3(c) measured L3.1's old bucket geometry reporting a leak as
`observed_silence`; building L2a on the old rule would have reproduced the defect
in a second place, which is why the establish preceded the build.

ONE COHORT PER REBUILD, AND THE REGISTRATION ASKS FOR THAT. §4.2 says "at cohort
*d*, corrupt only label cells unavailable at *d*", which is a mask per cohort,
and `DESIGN.md` §5.1 gives this row a `C x S` term -- cohorts times strategies --
so a rebuild per cohort is the registered cost model rather than a slow choice.
It also means no two cohorts share a batch, so the attribution overlap L3.1 has
to derive a stride against cannot arise here: `cohort_stride` is a SAMPLING
choice and nothing else, and the run says so.

WHAT IS NOT BUILT, AND IT REFUSES RATHER THAN GUESSING. The non-temporal mode of
§4.2 runs under `labels_available_during_feature_construction = false` and has no
decision times -- so it has no cohorts, and §7.2's scoring unit is *feature x
affected output cohort*. Building it would mean inventing a cohort identity the
registration does not supply, which is a registration finding and not a judgment
call. It is recorded as item 7(ii) of `NEXT_REGISTRATION_REQUIREMENTS.md` and the
mode refuses with that reason.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .availability import (CohortResult, ProbeError, align_key,
                           classify_cohorts, require_decision_column,
                           silence_note)

#: The registered row this module implements. Every finding carries it, so a
#: reader holding two runtime findings can tell which row produced which --
#: `PREREG.md` §6.2's criteria adjudicate "runtime findings" and name no row,
#: which is recorded as a registration finding; the tool's own output does not
#: have to inherit the ambiguity.
DETECTOR_ID = "L2a"

ZERO = pd.Timedelta(0)


class LabelDeclarationError(ProbeError):
    """An L2a declaration is present and cannot be used as written."""


@dataclass(frozen=True)
class LabelAvailability:
    """`a(y_j) = base + horizon + publication_delay`, all three declared.

    `base_column` names the column of the LABEL'S OWN FRAME carrying the label
    timestamp. It is not the decision column and it is not the frame's key: the
    registration writes the label's instant as its own arithmetic precisely
    because it is not the generic per-column rule.

    THE DELAY'S ZERO IS PART OF A SUPPLIED DECLARATION, NEVER A DEFAULT FOR A
    MISSING ONE. §2.4: "The publication delay defaults to zero only when the user
    supplies the declaration -- it is part of the user's statement, not something
    a profile fills in." So this field has a default and the ABSENCE of the whole
    object is refused elsewhere; the two states are kept apart on purpose.
    """
    base_column: str
    horizon: pd.Timedelta
    publication_delay: pd.Timedelta = ZERO

    def instants(self, frame: pd.DataFrame) -> pd.Series:
        if self.base_column not in frame.columns:
            raise LabelDeclarationError(
                "`label_availability` names %r as the label's timestamp column "
                "and the label's frame does not carry it. The instant it would "
                "read is not there." % self.base_column)
        base = pd.to_datetime(frame[self.base_column], errors="coerce")
        if base.isna().any():
            raise LabelDeclarationError(
                "%d value(s) of %r do not parse as timestamps. An unparseable "
                "availability instant compares false against every decision "
                "time, which reads as available and hides findings."
                % (int(base.isna().sum()), self.base_column))
        return base + self.horizon + self.publication_delay


@dataclass(frozen=True)
class RawLabel:
    """WHERE THE LABEL LIVES ON THE INPUT SIDE. R260 §5, R261 §4.

    THE SIDE IS IN THE NAME, and the reason is that this package already has a
    `label_column` and it means something else: the BUILT OUTPUT's label, read by
    the model-free checks, classified in the schema as vocabulary this project's
    registration does not declare. L2a perturbs an INPUT cell and rebuilds, so it
    needs the frame and column the label occupies before the builder runs.

    Giving the existing key a second job is the shape `PREREG.md` §2.3 records
    against v9's merge -- one name doing two jobs, set for one and silently
    governing the other -- and extending an unregistered key to carry a
    registered row's declaration would make that worse, not better.
    """
    frame: str
    column: str


@dataclass
class LabelProbeResult:
    side: str
    n_cohorts: int
    detector: str = DETECTOR_ID
    cohorts: list = field(default_factory=list)
    determinism_ok: bool = True
    notes: list = field(default_factory=list)
    #: §8.2's state, attached to an outcome of `none`. Set only where the row
    #: could not run for want of a declaration; never where it ran and was
    #: quiet. The frozen EvidenceOutcome enum is not touched: this is the state
    #: BESIDE an outcome, the way the NOT PROBED block already carries one.
    unsupported: str | None = None
    base_columns: tuple = ()
    #: Rows AFTER a probed cohort that moved. Evidence the perturbation reached
    #: the builder, and NOT an availability claim: those rows may legitimately
    #: read the cells that were corrupted for an earlier cohort.
    read_beyond: int = 0

    @property
    def findings(self):
        return [c for c in self.cohorts if c.finding()]

    @property
    def band_cohorts(self):
        return [c for c in self.cohorts if c.moved_in_band]

    @property
    def cells_perturbed(self) -> int:
        return sum(c.cells_perturbed for c in self.cohorts)

    def verdict(self) -> str:
        if self.unsupported:
            return "unsupported(%s)" % self.unsupported
        if not self.determinism_ok:
            return "could_not_run(determinism)"
        if not self.cohorts:
            return "could_not_run(no_cohorts)"
        if self.findings:
            return "finding"
        if self.band_cohorts:
            return "attribution_ambiguous"
        # THE SILENCE HAS TO BE LICENSED HERE TOO, AND BY A DIFFERENT FACT.
        # R262 §3(b). L3.1 licenses a silence with moved rows: a corrupted cell
        # that changes a later row proves the perturbation reaches the builder.
        # **That class is not available to L2a**, because a clean pipeline need
        # not read labels as features AT ALL -- a run in which no row moves is
        # the expected shape of a correct pipeline, not evidence of a dead
        # probe. So what licenses this row's silence is that cells were
        # PERTURBED: the probe wrote to the label cells the declaration says
        # were unrealized, and the build did not change. With zero perturbed
        # there is nothing to be silent about and the verdict says `none`.
        if self.cells_perturbed == 0:
            return "none(no perturbed cell reached the pipeline)"
        return "observed_silence"


# ---------------------------------------------------------------------------
# THE REFUSAL, AT THE SHARED CONSUMPTION POINT. R260 §6, R261 §4.
# ---------------------------------------------------------------------------

#: The elements a temporal L2a run needs, in the order a user meets them.
_ELEMENTS = ("raw_label", "label_availability")


def resolve_label_declaration(raw_label, label_availability, *, where: str,
                              has_timestamp: bool = True):
    """The one refusal, called from every consumer. Three cases, not two.

    R260 §6 ruled the shape and R261 §4 carried it. The registration says an
    absent declaration returns `unsupported` naming the missing element (§2.7,
    §8.2); every shipped refusal in this package raises. Both are right, for
    different cases, and the case that decides which is whether the user said
    ANYTHING about the label:

      nothing declared      -> ("unsupported", reason). The audit runs and the
                               row reports an outcome of `none` carrying the
                               §8.2 state. Never a pass.
      declared in part      -> REFUSE. A partial declaration is evidence of
                               intent, and running past it makes the rest of the
                               output look like the audit the user asked for.
      declared and malformed-> REFUSE, as every shipped refusal does.

    IF THE REGISTRATION'S "ABSENT" SENTENCE COVERS THE PARTIAL CASE TOO, the
    raise is a tool-level tightening rather than a conflict: §2.7 says "if the
    required declaration is neither supplied nor defaulted", and a declaration
    supplied in part has been supplied. The reading is recorded rather than
    assumed -- see the round report -- and the raise stands either way, because
    a tightening that refuses is not a pass mistaken for one.
    """
    present = [n for n, v in zip(_ELEMENTS, (raw_label, label_availability))
               if v is not None]
    if not present:
        return ("unsupported",
                "missing: %s. L2a perturbs label cells on the INPUT side and "
                "compares their declared availability against each output row's "
                "decision instant, so it needs to be told which frame and column "
                "the label occupies (`raw_label`) and when a label value became "
                "knowable (`label_availability`). Neither was declared, so this "
                "row did not run. That is not a pass and not a silence: nothing "
                "was probed." % ", ".join(_ELEMENTS))

    missing = [n for n in _ELEMENTS if n not in present]
    if missing:
        raise LabelDeclarationError(
            "L2a is declared in part: %s supplied, %s missing. %s\n"
            "REFUSED RATHER THAN REPORTED UNSUPPORTED. Declaring one half is "
            "evidence you meant this row to run, and a run that quietly skips it "
            "returns an audit that looks like the one you asked for and is not. "
            "Supply the rest, or remove both and the row reports `unsupported` "
            "naming what it needed."
            % (", ".join("`%s`" % p for p in present),
               ", ".join("`%s`" % m for m in missing), where))

    if not isinstance(raw_label, RawLabel):
        raise LabelDeclarationError(
            "`raw_label` is %r and a RawLabel(frame=, column=) was expected. %s"
            % (raw_label, where))
    for attr in ("frame", "column"):
        val = getattr(raw_label, attr)
        if not isinstance(val, str) or not val:
            raise LabelDeclarationError(
                "`raw_label.%s` is %r, and a name was expected. %s"
                % (attr, val, where))
    if not isinstance(label_availability, LabelAvailability):
        raise LabelDeclarationError(
            "`label_availability` is %r and a LabelAvailability(base_column=, "
            "horizon=, publication_delay=) was expected. %s"
            % (label_availability, where))
    if not isinstance(label_availability.base_column, str) or \
            not label_availability.base_column:
        raise LabelDeclarationError(
            "`label_availability.base_column` is %r, and a column name was "
            "expected. %s" % (label_availability.base_column, where))
    for attr in ("horizon", "publication_delay"):
        val = getattr(label_availability, attr)
        if not isinstance(val, pd.Timedelta) or val is pd.NaT:
            raise LabelDeclarationError(
                "`label_availability.%s` is %r, and a duration was expected. "
                "All three terms of `a(y_j) = base + horizon + delay` are "
                "declared (PREREG.md section 2.4); none is inferred. %s"
                % (attr, val, where))
        if val < ZERO:
            raise LabelDeclarationError(
                "`label_availability.%s` is negative (%s). A label that becomes "
                "knowable BEFORE its own timestamp is not a horizon or a "
                "publication delay, and this tool declines to guess which term "
                "was meant. %s" % (attr, val, where))

    if not has_timestamp:
        # §4.2's non-temporal mode. Refused with its reason, not silently
        # unavailable: the user is in a real state and it has a real name.
        raise LabelDeclarationError(
            "this task carries no decision timing, so L2a's NON-TEMPORAL mode "
            "would be the applicable one (PREREG.md sections 2.5 and 4.2) and it "
            "is NOT BUILT. %s\n"
            "WHY IT IS REFUSED RATHER THAN APPROXIMATED. The registered scoring "
            "unit is `feature x affected output cohort` and a cohort is the "
            "output rows sharing one decision time. A non-temporal task has no "
            "decision times, so it has no cohorts, and building the mode would "
            "mean inventing a cohort identity the registration does not supply. "
            "That is recorded as a registration finding -- item 7(ii) of "
            "NEXT_REGISTRATION_REQUIREMENTS.md -- and filling it by judgment "
            "here would put a number in a denominator nobody registered." % where)
    return ("ok", None)


# ---------------------------------------------------------------------------
# THE PROBE
# ---------------------------------------------------------------------------

def run_probe_l2a(raw, build, model, *, raw_label=None, label_availability=None,
                  side: str = "user", cohort_stride: int = 97,
                  max_cohorts: int = 25, seed: int = 20260828,
                  has_timestamp: bool = True) -> LabelProbeResult:
    """Corrupt the label cells unavailable at each probed cohort, one at a time.

    Returns a `LabelProbeResult` whose verdict is `unsupported(...)` where no
    L2a element was declared. A partial or malformed declaration raises.
    """
    res = LabelProbeResult(side=side, n_cohorts=0)
    state, reason = resolve_label_declaration(
        raw_label, label_availability,
        where="the label probe (L2a)", has_timestamp=has_timestamp)
    if state == "unsupported":
        res.unsupported = reason
        res.notes.append(
            "NOT PROBED: L2a. %s" % reason)
        return res

    if raw_label.frame not in raw:
        raise LabelDeclarationError(
            "`raw_label` names frame %r, which was not supplied. Supplied: %s. "
            "A declared frame that is absent would make this row silent about "
            "the configuration rather than about the pipeline."
            % (raw_label.frame, ", ".join(sorted(raw)) or "nothing"))
    lf = raw[raw_label.frame]
    if raw_label.column not in lf.columns:
        raise LabelDeclarationError(
            "frame %r has no column %r. Columns: %s"
            % (raw_label.frame, raw_label.column, ", ".join(map(str, lf.columns))))

    base = build(dict(raw))
    res.base_columns = tuple(base.columns)
    base2 = build(dict(raw))
    if not base.equals(base2):
        res.determinism_ok = False
        res.notes.append("the builder is not deterministic across two clean runs; "
                         "no corruption result from it could be attributed")
        return res

    dcol = require_decision_column(model.decision_column, "the label probe (L2a)")
    if dcol not in base.columns:
        raise ProbeError("the decision column %r is not in the built output" % dcol)
    d = pd.to_datetime(base[dcol])

    a_y = label_availability.instants(lf)
    a_y = align_key(a_y, d, frame=raw_label.frame,
                    column=label_availability.base_column)

    seconds = pd.Index(sorted(d.dt.floor("s").unique()))
    picked = seconds[::cohort_stride][:max_cohorts]
    res.n_cohorts = len(picked)
    res.notes.append(
        "label availability: a(y) = %r + horizon %s + publication delay %s. "
        "All three are declared; none is inferred (PREREG.md section 2.4)."
        % (label_availability.base_column,
           label_availability.horizon, label_availability.publication_delay))
    if model.ties_available:
        res.notes.append(
            "comparator: `a(y_j) <= d(i)` -- ties AVAILABLE, the registered "
            "default (PREREG.md section 2.3). A label whose instant equals the "
            "decision instant counts as realized.")
    else:
        res.notes.append(
            "COMPARATOR IS NOT THE DEFAULT: `a(y_j) < d(i)` -- ties UNAVAILABLE. "
            "A label realizing exactly at the decision instant is counted as NOT "
            "realized, so rows stamped exactly there are findings here and are "
            "not under the default.")
    # ONE REBUILD PER COHORT, SO THE STRIDE IS A SAMPLING CHOICE AND NOTHING
    # MORE. R261 §1(b) asks for this to be said where it is true rather than for
    # a derived number that would mean nothing: no two cohorts share a batch, so
    # no moved row can be claimed by two of them.
    res.notes.append(
        "cohorts are probed ONE PER REBUILD, so `cohort_stride`=%d selects which "
        "seconds are looked at and carries no attribution weight: each cohort's "
        "batch is its own and no moved row lies in two of them. That is the "
        "registered cost model's `C x S` term (DESIGN.md section 5.1), not a "
        "slower choice." % cohort_stride)
    if res.n_cohorts == 0:
        return res

    rng = np.random.default_rng(seed)
    a_np = a_y.to_numpy()
    probed_any = False
    read_beyond = 0
    for f_sec in picked:
        # §4.2: at cohort d, corrupt only label cells UNAVAILABLE at d.
        if model.ties_available:
            unavail = a_np > np.datetime64(f_sec)
        else:
            unavail = a_np >= np.datetime64(f_sec)
        if not unavail.any():
            res.cohorts.append(_empty_cohort(f_sec))
            continue
        probed_any = True
        corrupt = {k: v.copy() for k, v in raw.items()}
        cf = corrupt[raw_label.frame]
        _perturb(cf, raw_label.column, unavail, rng)
        after = build(corrupt)
        if len(after) != len(base) or list(after.columns) != list(base.columns):
            raise ProbeError(
                "the corrupted build changed shape (%s -> %s); rows cannot be "
                "compared positionally"
                % ((len(base), len(base.columns)), (len(after), len(after.columns))))
        # ASSERT EVERY CALL, per DESIGN.md §2.7: every non-label column and every
        # AVAILABLE label cell is byte-identical to the aligned baseline.
        _assert_only_unavailable_labels_moved(raw, corrupt, raw_label, unavail)
        moved, moved_col = _diff(base, after)
        lo = pd.Timestamp(a_np[unavail].min())
        hi = pd.Timestamp(a_np[unavail].max())
        # THIS COHORT SPEAKS FOR `d(i) <= F` AND FOR NOTHING ELSE. §2.6 locks
        # both directions: a change at any row with `d(i) <= d` is a valid
        # finding, and silence is informative only for `d(i) = d`. Rows after F
        # read cells that may well have been available to them, so this cohort
        # has no claim about them either way -- they are counted below as
        # evidence the perturbation was READ, which is a fact about the probe
        # and not about availability.
        # CLOSED AT BOTH ENDS: rows deciding AT OR BEFORE this cohort's instant,
        # which is §2.6's `d(i) <= d` written as itself. The row AT `f_sec` is
        # the tie row and it belongs here under the default comparator.
        bounds = {f_sec: (d.min(), f_sec)}
        cohorts, _notes, _ov = classify_cohorts(
            [f_sec], d, moved, moved_col, {f_sec: lo}, {f_sec: hi}, model,
            bounds=bounds, batch_n={f_sec: int(unavail.sum())})
        res.cohorts.extend(cohorts)
        read_beyond += int((moved & (d.to_numpy() > np.datetime64(f_sec))).sum())

    # THE PER-COHORT CELL COUNTS, PRINTED. R262 §3(b). The silence rests on
    # them, so they are in the output rather than inferable from it, and a
    # cohort that perturbed nothing is named rather than averaged into a total.
    empty = [str(c.second) for c in res.cohorts if c.cells_perturbed == 0]
    res.notes.append(
        "cells perturbed per cohort: %s. Total %d cell(s) perturbed across %d "
        "cohort(s)%s."
        % (", ".join("%s=%d" % (c.second, c.cells_perturbed)
                     for c in res.cohorts) or "none",
           res.cells_perturbed, len(res.cohorts),
           "" if not empty else
           "; %d cohort(s) had NO unavailable label to corrupt and are `none` "
           "rather than silent: %s" % (len(empty), ", ".join(empty))))
    # WHICH LICENCE THIS ROW'S SILENCE CARRIES, said in the run rather than left
    # to be inferred from L3.1's. R262 §3(b).
    res.notes.append(
        "WHAT LICENSES A SILENCE HERE, and it is not what licenses L3.1's. That "
        "probe can point at rows that MOVED and were available -- proof its "
        "perturbation reaches the builder. L2a has no such class: a pipeline "
        "that does not read the label as a feature moves no row at all, and "
        "that is the expected shape of a CORRECT pipeline rather than a dead "
        "probe. So this row's silence rests on cells having been PERTURBED -- "
        "the label values the declaration calls unrealized were written to, and "
        "the build did not change. With zero perturbed the verdict is `none`.")
    if not probed_any:
        res.notes.append(
            "no label cell was unavailable at any probed second, so nothing was "
            "perturbed. This row's silence is `none` -- a probe that did not "
            "happen -- rather than `observed_silence`.")
        res.notes.append(silence_note(
            res.cells_perturbed, {}, {}, list(picked),
            extra="For this row that means the declared label availability puts "
                  "every label value at or before every probed decision "
                  "instant, so there was never an unrealized label to corrupt. "
                  "Check the horizon and the base column against what your "
                  "labels actually are."))
    res.read_beyond = read_beyond
    res.notes.append(
        "attribution: %d finding row(s) across %d cohort(s), detector %s. "
        "Each cohort speaks for rows deciding at or before its own instant "
        "(PREREG.md section 2.6) and for no others; %d row(s) after a probed "
        "cohort moved, which is evidence the perturbation was READ and is not "
        "an availability claim about those rows. The BAND is empty here BY "
        "CONSTRUCTION -- this row's mask is the comparator itself, so every "
        "perturbed cell is unavailable to every row the cohort speaks for -- "
        "and a non-zero band would mean the mask and the classifier had come "
        "apart."
        % (sum(c.moved_in_second for c in res.cohorts), len(res.cohorts),
           DETECTOR_ID, read_beyond))
    return res


def _empty_cohort(f_sec):
    return CohortResult(second=f_sec, rows_in_second=0, moved_in_second=0,
                        moved_next_second=0)


def _perturb(frame: pd.DataFrame, column: str, mask, rng) -> None:
    """A large, deterministic, dtype-preserving perturbation of the label cells.

    The same rule `availability.run_probe_a` applies to an aggregate column, for
    the same reason: the question is whether the value is READ, and a
    perturbation that could coincide with the original produces a false silence.
    """
    col = frame[column]
    n = int(np.asarray(mask).sum())
    if pd.api.types.is_bool_dtype(col):
        frame.loc[mask, column] = ~col[mask].to_numpy()
    elif pd.api.types.is_integer_dtype(col):
        info = np.iinfo(col.dtype)
        lo, hi = int(info.min), int(info.max)
        headroom = min(1000, max(1, hi - lo))
        off = 1 + rng.integers(0, headroom, n)
        vals = col[mask].to_numpy()
        up = vals <= (hi - headroom)
        frame.loc[mask, column] = np.where(up, vals + off, vals - off).astype(col.dtype)
    elif pd.api.types.is_numeric_dtype(col):
        vals = col[mask].to_numpy(dtype=float, copy=True)
        frame.loc[mask, column] = vals + 1.0e6 + rng.standard_normal(n)
    else:
        raise LabelDeclarationError(
            "the label column %r has dtype %s, which this probe cannot perturb "
            "without inventing a value for it. Refused rather than coerced: a "
            "dtype change is itself a perturbation and would make the finding "
            "unattributable." % (column, col.dtype))


def _assert_only_unavailable_labels_moved(raw, corrupt, raw_label, mask) -> None:
    """DESIGN.md §2.7's every-call assertion. Without it a finding cannot be
    attributed to the label rather than to something else that moved."""
    for name, before in raw.items():
        after = corrupt[name]
        if name != raw_label.frame:
            if not before.equals(after):
                raise ProbeError(
                    "frame %r changed and only the label column of %r should "
                    "have. A finding from this run could not be attributed."
                    % (name, raw_label.frame))
            continue
        for c in before.columns:
            if c == raw_label.column:
                continue
            if not before[c].equals(after[c]):
                raise ProbeError(
                    "column %r of the label frame changed and only %r should "
                    "have." % (c, raw_label.column))
        keep = ~np.asarray(mask)
        if not before[raw_label.column][keep].equals(after[raw_label.column][keep]):
            raise ProbeError(
                "an AVAILABLE label cell was perturbed. Only cells unavailable "
                "at the cohort may move, or a finding says nothing about "
                "availability.")


def _diff(base: pd.DataFrame, after: pd.DataFrame):
    """(row mask, {column -> row mask}) of what moved. Exact, never tolerant."""
    moved_col = {}
    moved = np.zeros(len(base), dtype=bool)
    for c in base.columns:
        a_ = base[c].astype("string").fillna("<NA>").to_numpy()
        b_ = after[c].astype("string").fillna("<NA>").to_numpy()
        m = a_ != b_
        if m.any():
            moved_col[c] = m
            moved = moved | m
    return moved, moved_col
