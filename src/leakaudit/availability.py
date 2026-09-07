"""Probe A -- the availability probe. R151 §4/B-6.

WHAT IT ASKS, in one sentence: does the built output depend on cells the declared
availability model says had not yet arrived at the row's decision time?

THE MODEL, from `AVAILABILITY_DECLARATION.md`, not invented here:

  * the comparator is `a(j,c) <= d(i)` -- TIES AVAILABLE, locked at §0.3 Claim A
  * `d(i)` is the output row's decision instant: its `timestamp`
  * for the join families the declared availability instant is the
    **`at_source_timestamp` truth, `ts_floor + 1s`** -- the instant the
    wall-clock-second aggregate COMPLETES. The declaration states in terms that
    the `at_bar_close` role is an APPROXIMATION of that instant and not the
    scored one, "which is why the declaration is made here, in terms": scoring
    `at_bar_close` would find the contaminated side clean.

So an aggregate over `[F, F+1s)` is unavailable to any row stamped inside that
second, and available to rows stamped at or after `F + 1s`.

WHY ONE REBUILD SUFFICES, AND WHY A NAIVE ONE WOULD PROVE NOTHING. Corrupting
every aggregate row moves every output row on BOTH sides -- one reads its own
second, the other reads the previous one, and both were corrupted. The probe
must corrupt a SPARSE SET OF SECONDS and then ask WHICH output rows moved:

    a row stamped in second F moves        -> the build read F's aggregate at a
                                              decision time inside F  -> the cell
                                              was UNAVAILABLE  -> a finding
    only rows stamped in second F+1 move   -> the build read F's aggregate one
                                              second later  -> AVAILABLE  -> no
                                              finding

**The discrimination is in the row indices, not in the fact of movement.** That
is what lets a single rebuild separate the pair, and it is the whole design.

SC-7 COMPLIANCE. The probe receives the pipeline for ONE SIDE and the declared
availability model. It never receives the paired side, and never the R9
ground-truth map -- SC-7(c): under criterion 3 the map is the scoring key, and a
run that received it "has not produced a gate result, whatever it reports."

EXACT COMPARISON, NEVER TOLERANT. A tolerance would silently absorb exactly the
small perturbations a leak of one aggregate produces.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Callable, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

SECOND = pd.Timedelta(seconds=1)


class ProbeError(RuntimeError):
    """The probe cannot answer, and says so rather than returning silence."""


def _window_text(w: pd.Timedelta) -> str:
    """`1s`, not `0 days 00:00:01`.

    The note this feeds is read by someone deciding whether their configuration
    is right. pandas' Timedelta repr is correct and unreadable, and a message
    nobody finishes reading is the failure mode this whole round is about.
    """
    ns = int(w.value)
    if ns > 0:
        for div, unit in ((86_400_000_000_000, "d"), (3_600_000_000_000, "h"),
                          (60_000_000_000, "min"), (1_000_000_000, "s"),
                          (1_000_000, "ms"), (1_000, "us"), (1, "ns")):
            if ns % div == 0:
                return "%d%s" % (ns // div, unit)
    return str(w)


def _inference_frame(info) -> str:
    """WHAT THE INFERRED BAR DURATION RESTS ON, in the note. R225 §2(b), (c).

    THE VALUE IS NAMED ONLY WHERE THERE IS ONE. R224 §2(b) put the number in the
    note so a wrong inference could be seen at a glance, and it worked on its
    first live use -- but the number it printed was one row's gap standing for a
    per-row series, so on a frame whose bars are irregular it was a point
    estimate of a set with no centre. Where the successive differences disagree
    this says so and names no value, which is the refusal R225 §2(c) asks for
    applied to the CLAIM: the registration fixes the computation as per-row gaps
    (`PREREG.md` line 255, `DESIGN.md` §2.1, `AVAILABILITY_MODES.md`), so
    refusing the ROUTE would narrow a registered grant -- `ties_available`'s
    defect -- while refusing to state a bar duration the frame does not have
    costs the user nothing they were entitled to.

    THE SUMMARY HAS NO CENTRE; THE MECHANISM DOES NOT NEED ONE. R226 §1, recorded
    here because it is the question the next reader will ask, and because it was
    asked once already and answered wrongly. Disagreeing gaps are NOT a defect in
    the computation: each row uses the gap to its own next timestamp and is
    correct by construction, so there is no averaging anywhere and nothing to
    make well-conditioned. What has no centre is the one-number SUMMARY somebody
    wanted to print. Raising on disagreement would treat ordinary irregular data
    as an error and remove the granted route in the process.

    AND THE FRAME IS WHAT MAKES THE CONSEQUENCE VISIBLE. "26 differences, 2
    distinct, 1s to 2s" tells a reader that some rows took a 2s gap where the
    true bar was 1s -- a cell reported knowable later than it truly was -- which
    is a statement about their data that no single number could carry.
    """
    if info is None:
        return "The frame is empty, so nothing was inferred from it."
    order = ("The timestamp column was NOT IN TIME ORDER as given, and the "
             "differences were taken in time order rather than row order. "
             ) if info.reordered else ""
    if info.agrees:
        return (
            "%sINFERRED BAR DURATION: %s -- and it is well founded: all %d "
            "successive differences are that same value, so this frame does "
            "have a single bar length. CHECK IT anyway: it is a fact about "
            "your data's sampling, not about what the bar summarises."
            % (order, _window_text(info.smallest), info.n_gaps))
    return (
        "%sTHERE IS NO SINGLE BAR DURATION HERE, so none is named. The %d "
        "successive differences take %d DISTINCT values, from %s to %s "
        "(median %s). The registered inference gives each row the gap to its "
        "own next timestamp, so the availability instant varies row by row and "
        "no one number describes this run -- reporting a representative value "
        "would be a figure without its frame. Differences that disagree mean "
        "either that bars are missing (a gap of two bars is read as a bar "
        "twice as long, which puts that cell's availability later than it "
        "truly was) or that the column is not bar-shaped at all, in which case "
        "`at_bar_close` is the wrong mode. Declare `bar_duration_seconds` to "
        "settle it."
        % (order, info.n_gaps, info.n_distinct, _window_text(info.smallest),
           _window_text(info.largest), _window_text(info.median)))


# The decision clock nobody has declared. A sentinel rather than `None` so the
# field keeps its type, and rather than `"timestamp"` so the absence is visible.
NOT_SET = "<decision column not declared>"

# The slice padding nobody has declared, as distinct from a declared zero.
# `slicing.py` owns the rule and this constant is DEFINED HERE because a
# signature default must be importable without a cycle -- `slicing` imports this
# module, so this module cannot import `slicing` at the top to get it. One
# definition, imported by `slicing`, so the two cannot drift apart. R255 §5.
NOT_DECLARED = "<padding not declared>"


def require_column_name(dcol, where: str) -> None:
    """A value that is not a non-empty string is not a column name.

    SEPARATE FROM THE UNSET QUESTION, because the two are asked in different
    scopes. "Nobody declared a clock" matters only where a clock is consumed; "a
    clock was declared as the integer 0" is malformed wherever it appears, so
    the loader asks this one of every file and the other only of files that
    declare an availability model.

    IT LIVES HERE RATHER THAN IN THE LOADER, and R238 §1 is why. The loader
    refused `None`, `''` and `0`; the consolidated refusal at the consumption
    point did not, so the consolidation made the check WEAKER than the boundary
    it replaced. Measured: with the membership test that sits on the next line
    of each probe removed, those three values reach pandas as `KeyError: None`
    -- a detection arriving as somebody else's exception, which is the failure
    mode `modes.availability` was hardened against twice.

    So the completeness of the refusal had been resting on a NEIGHBOURING LINE'S
    POSITION. That is not a property a refusal can have: `cli.py` reads the
    clock with no membership test beside it at all and was covered only because
    `run_probe_a` runs first.
    """
    if isinstance(dcol, str) and dcol == NOT_SET:
        return                      # a different question, asked elsewhere
    if not isinstance(dcol, str) or not dcol:
        raise ProbeError(
            "`decision_column` is %r, and a column name was expected. %s\n"
            "REFUSED HERE RATHER THAN DOWNSTREAM. Until R238 a value like this "
            "passed through the shared refusal and was stopped by a membership "
            "test on the next line of each probe -- so whether it was caught "
            "depended on that line's position, and a consumer without one "
            "handed it to pandas." % (dcol, where))


def require_decision_column(dcol, where: str) -> str:
    """The clock, or a refusal. ONE refusal, called from every consumer.

    R236 §3(c). There were nearly two: a file-boundary check added at R235 and a
    consumption-point check added here. Two refusals for one condition is the
    two-lists hazard in another costume -- they drift, and the one a user meets
    depends on which path they took. This is the single implementation; the
    loader calls it early so a file gets its refusal before any work, and the
    probe calls it so a library caller gets the same words.

    IT TAKES THE VALUE, NOT A MODEL, and the reason is measured. The first
    version took a model, so the loader had to build a throwaway one to ask the
    question -- and the defaults instrument immediately reported two newly-taken
    default sites, `window=` and `ties_available=`, because that throwaway
    omitted them. A helper that makes its callers construct an object to ask a
    question about one field is asking for the wrong thing.
    """
    # `isinstance` FIRST. `dcol == NOT_SET` alone asks an arbitrary object's
    # `__eq__` a question about a string, and an array-like answers with an
    # array, which is not a truth value. NOT_SET is a str, so only a str can be
    # equal to it.
    if isinstance(dcol, str) and dcol == NOT_SET:
        raise ProbeError(
            "no decision column is declared, and there is no default for it. %s\n"
            "`decision_column` names the column of your BUILT OUTPUT holding "
            "each row's decision instant -- the moment that row's prediction was "
            "made, against which every availability instant is compared.\n"
            "IT DEFAULTED TO `timestamp` UNTIL R236, and that default was "
            "measured producing `observed_silence` -- this tool's affirmative "
            "'I looked and found nothing, this is evidence' -- on a frame set "
            "whose declared clock produced three findings. A real leak reported "
            "as evidence of absence, because a column happened to be named "
            "`timestamp` and sat two seconds from the true instant.\n"
            "If your output genuinely calls it `timestamp`, declare that. The "
            "declaration and the coincidence are different things and only one "
            "of them is checkable." % where)
    require_column_name(dcol, where)
    return dcol


@dataclass(frozen=True)
class AvailabilityModel:
    """The declared model. Supplied to the probe; never inferred by it.

    `aggregate_frames` are the frames whose rows are wall-clock-second
    aggregates keyed by `key_column`; their declared availability instant is
    **`floor(key) + window`** -- the end of the wall-clock second the key falls
    in. `decision_column` is the output's decision instant.

    THE FLOOR IS NOT DECORATION, AND THIS SENTENCE USED TO BE WRONG. It read
    `key + window` for two rounds, which is the same number only where the key
    is already a wall-clock second. On the acceptance fixture that holds for
    `magg.ts_floor` (464,199 of 464,199 rows) and fails for `trades.ts_event`
    (49 of 397,457, median offset 467.83 ms), so the documented instant was
    later than the computed one on 99.9877% of that frame's rows. The computed
    one is correct -- `AVAILABILITY_DECLARATION.md` §3 and §C.1 declare the join
    family's instant to be `floor(T) + 1s`, and the pipeline reaches every
    trade-derived feature through `groupby("ts_floor")` -- so the description was
    the defect, and it is recorded as D-V30A-43 rather than quietly amended. A
    non-boundary key is floored AND REPORTED; see `run_probe_a`.
    """
    aggregate_frames: Mapping[str, str]          # frame name -> key column
    # NOT_SET, NEVER "timestamp". R236 §3.
    #
    # This read `= "timestamp"` for the project's whole history, and the default
    # was measured producing the worst answer the tool can give. Same frames,
    # same pipeline, the field the only difference:
    #
    #     no decision_column  -> observed_silence, 0 findings
    #     the true clock      -> 3 findings
    #
    # `observed_silence` is the affirmative "I looked over a stated population
    # and found nothing. This is evidence." A real leak, reported as evidence of
    # absence, because a column was called `timestamp` and sat two seconds from
    # the decision instant.
    #
    # R235 refused this AT THE FILE BOUNDARY and that covered one of two entry
    # points. Measured at the other: `AvailabilityModel(aggregate_frames=...)`
    # in Python, no decision column, silently picked and returned the same
    # false silence. **A fix at one entry point does not cover the other** --
    # P0 at `audit()` and not the CLI, three config keys reaching the library
    # and not the command, `_is_datetimeish` on frames and not on files.
    #
    # SO THE SENTINEL SITS ON THE FIELD AND THE REFUSAL SITS WHERE THE CLOCK IS
    # CONSUMED, which both entry points reach. And it makes two states
    # distinguishable that a string default merges: "explicitly timestamp" is a
    # declaration this tool cannot check, and "never chose" is a question nobody
    # answered. Only the second is refusable.
    decision_column: str = NOT_SET
    window: pd.Timedelta = SECOND
    ties_available: bool = True                  # §0.3 Claim A, locked

    def available(self, a: pd.Series, d: pd.Series) -> pd.Series:
        """`a(j,c) <= d(i)` under the locked tie rule."""
        return a <= d if self.ties_available else a < d


@dataclass
class CohortResult:
    second: pd.Timestamp
    rows_in_second: int
    moved_in_second: int          # rows whose decision time is INSIDE F
    moved_next_second: int        # rows stamped in F+1
    # WHICH COLUMNS MOVED, not merely that a row did. The frozen output contract
    # requires a FindingRecord to name a `feature`; a probe that reports only row
    # movement cannot fill that field without inventing one, and a placeholder
    # there would be a fabricated fact inside a registered trace.
    features_in_second: tuple = ()
    def finding(self) -> bool:
        return self.moved_in_second > 0


@dataclass
class ProbeAResult:
    side: str
    n_cohorts: int
    cohorts: list = field(default_factory=list)
    determinism_ok: bool = True
    notes: list = field(default_factory=list)
    # THE COLUMNS OF THE FRAME THE PROBE ACTUALLY COMPARED. R192 §1.
    #
    # A caller that needs the output's column set was building the frame a
    # second time to get it, which costs a build per side and -- worse -- takes
    # the column set from a DIFFERENT build than the one the findings came from.
    # The probe has the baseline in hand; carrying its columns out is free and
    # removes the possibility of the two disagreeing.
    base_columns: tuple = ()
    # FRAMES THE CALLER SUPPLIED AND THE MODEL DOES NOT DESCRIBE. R200 P0.
    #
    # Such a frame is not perturbed, so nothing it feeds can move, so every
    # column downstream of it is silent -- and that silence is `none`, a probe
    # that did not happen, NOT `observed_silence`, a probe that happened and
    # found nothing. The registration fixes that distinction and the package
    # was collapsing it: an undeclared frame produced no note at all, so a
    # caller who forgot to declare one received a silence about their own
    # configuration and could not tell it from a silence about their pipeline.
    unmodelled_frames: tuple = ()
    # THE SLICE, IF ONE WAS ASKED FOR. `DESIGN.md` §5.3, R255 §3.
    #
    # `context_seconds` are seconds the builder READ and the probe did NOT
    # perturb. They are carried separately from `cohorts` rather than appended
    # to it with a flag, because anything inside `cohorts` is a probed subject
    # and `verdict()` reads that list: a padding second admitted there would
    # count toward `observed_silence`, which is exactly the claim -- a probe
    # happened and found nothing -- that never ran over them. Their outcome is
    # `not_applicable`. `DESIGN.md` §8 locks the same distinction for the
    # report: not-run states are never displayed as passed.
    slice_plan: object = None
    context_seconds: tuple = ()

    @property
    def findings(self):
        return [c for c in self.cohorts if c.finding()]

    def context_outcome(self) -> str:
        """The padding seconds' outcome. Never `observed_silence`, never clean."""
        return "not_applicable" if self.context_seconds else "no_slice"

    def verdict(self) -> str:
        if not self.determinism_ok:
            return "could_not_run(determinism)"
        if not self.cohorts:
            return "could_not_run(no_cohorts)"
        return "finding" if self.findings else "observed_silence"


@dataclass
class EligibleCohorts:
    """Which selected seconds an aggregate frame actually carries a row in."""
    eligible: tuple = ()
    ineligible: tuple = ()
    per_frame: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)


def align_key(key: pd.Series, decision: pd.Series, *, frame: str,
              column: str) -> pd.Series:
    """Put an aggregate frame's key into the decision stamps' frame of reference.

    THIS IS THE FUNCTION THAT USED TO LIVE IN A TEST HARNESS, AND IT IS A
    SILENT-WRONG-ANSWER GENERATOR IF IT IS WRONG. `trades.ts_event` is
    tz-aware UTC while the snapshot stamps are naive. `isin` between aware and
    naive NEVER matches, so the trades frame was silently never corrupted -- an
    all-False mask that looks exactly like "no cells were unavailable". It was
    found by measurement, not by review, and the harness copy of it dropped
    every key to naive UTC unconditionally, which is a DIFFERENT rule from the
    one the probe uses and produces an empty intersection whenever the decision
    stamps are the aware ones.

    So the two cases are separated and neither is silent:

      * both sides carry a timezone, or neither does -> convert into the
        decision stamps' zone and return;
      * exactly one side carries one -> the two are not comparable and no
        conversion is derivable from the data. RAISE. Returning an empty match
        here is the failure this function exists to prevent.

    UNRESOLVED, AND RECORDED RATHER THAN QUIETLY RECONCILED (D-V30A-42). This
    function REFUSES the mixed case. `run_probe_a` below, and the population
    harness, both CONVERT it -- assuming the aware column is universal time --
    and that converting rule produced every number in this project's Phase 1
    evidence. The two contradict, and the acceptance fixture contains the case:
    its trade frame carries an aware key against naive decision stamps. Which
    rule is right is a question about the probe, so it is not settled here in
    passing. NOTHING CALLS THIS FUNCTION IN THE PATH THAT PRODUCED ANY RECORDED
    RESULT, which is exactly how the two were able to diverge unnoticed.
    """
    k_tz = getattr(key.dt, "tz", None)
    d_tz = getattr(decision.dt, "tz", None)
    if (k_tz is None) != (d_tz is None):
        raise ProbeError(
            "frame %r column %r is %s and the decision stamps are %s. A "
            "comparison between them matches NOTHING, which is indistinguishable "
            "from a frame that carries no row in any selected second -- and that "
            "silence would be reported as though the pipeline had been probed. "
            "Localise one of them and say which is right; this cannot be "
            "guessed from the data."
            % (frame, column,
               "timezone-aware (%s)" % k_tz if k_tz is not None else "naive",
               "timezone-aware (%s)" % d_tz if d_tz is not None else "naive"))
    if k_tz is not None and str(k_tz) != str(d_tz):
        return key.dt.tz_convert(d_tz)
    return key


def eligible_cohorts(frames: Mapping[str, pd.DataFrame],
                     model: AvailabilityModel,
                     picked: Iterable,
                     decision: pd.Series) -> EligibleCohorts:
    """The selected seconds some declared aggregate frame carries a row in.

    A second with no aggregate row has nothing to corrupt, so nothing can be
    scheduled there. Emitting a record for it anyway would resolve to a missing
    schedule slot with no recorded failure -- reporting a dead process where the
    truth is an empty probe surface.

    Extracted from two test harnesses at R201 P2. It was duplicated there and
    reimplemented in a third form inside the identity control, which is three
    chances for the timezone rule above to be got wrong in three places.
    """
    picked = list(picked)
    pset = set(picked)
    have: set = set()
    res = EligibleCohorts()
    for fname, keycol in model.aggregate_frames.items():
        f = frames.get(fname)
        if f is None:
            res.notes.append(
                "aggregate frame %r is declared and absent from the supplied "
                "frames; it contributed no eligible second" % fname)
            res.per_frame[fname] = 0
            continue
        if keycol not in f.columns:
            raise ProbeError("frame %r has no key column %r" % (fname, keycol))
        key = align_key(pd.to_datetime(f[keycol]), decision,
                        frame=fname, column=keycol)
        matched = set(key.dt.floor("s").unique()) & pset
        res.per_frame[fname] = len(matched)
        have |= matched
    res.eligible = tuple(s for s in picked if s in have)
    res.ineligible = tuple(s for s in picked if s not in have)
    if picked and not res.eligible:
        res.notes.append(
            "NO selected second is carried by any declared aggregate frame. "
            "Every cohort is ineligible, so this run would probe nothing and "
            "its silence would be `none` rather than `observed_silence`.")
    return res


def _fingerprint(df: pd.DataFrame) -> np.ndarray:
    """A per-row fingerprint, exact. Row order is the identity here."""
    cols = [df[c].to_numpy() for c in sorted(df.columns)]
    out = np.empty(len(df), dtype=object)
    for i in range(len(df)):
        h = hashlib.sha256()
        for col in cols:
            h.update(repr(col[i]).encode("utf-8"))
        out[i] = h.hexdigest()
    return out


def _fast_fingerprint(df: pd.DataFrame) -> pd.Series:
    """Vectorised row fingerprint. Falls back to the exact per-row hash only if
    the vectorised form cannot represent a column."""
    parts = []
    for c in sorted(df.columns):
        s = df[c]
        parts.append(s.astype("string").fillna("<NA>"))
    joined = parts[0]
    for p in parts[1:]:
        joined = joined.str.cat(p, sep="\x1f")
    return joined


def run_probe_a(raw: Mapping[str, pd.DataFrame],
                build: Callable[[Mapping[str, pd.DataFrame]], pd.DataFrame],
                model: AvailabilityModel,
                side: str,
                bar_duration=None,
                cohort_stride: int = 97,
                max_cohorts: int = 400,
                seed: int = 20260828,
                column_modes: Mapping[str, object] | None = None,
                slice_from=None,
                padding=NOT_DECLARED) -> ProbeAResult:
    """Corrupt a sparse set of seconds, rebuild once, and read WHICH rows moved.

    `cohort_stride` keeps corrupted seconds far apart so a moved row can be
    attributed to exactly one corrupted second. A stride of 1 would corrupt
    adjacent seconds and make "own second" and "previous second"
    indistinguishable -- which is the entire discrimination.
    """
    res = ProbeAResult(side=side, n_cohorts=0)

    base = build(dict(raw))
    res.base_columns = tuple(base.columns)
    base2 = build(dict(raw))
    if not base.equals(base2):
        res.determinism_ok = False
        res.notes.append("the builder is not deterministic across two clean runs; "
                         "no corruption result from it could be attributed")
        return res

    dcol = require_decision_column(model.decision_column,
                                   "the availability probe")
    if dcol not in base.columns:
        raise ProbeError("the decision column %r is not in the built output" % dcol)
    d = pd.to_datetime(base[dcol])
    base_floor = d.dt.floor("s")

    # The corrupted seconds: sparse, deterministic, derived from the data's own
    # range rather than chosen.
    seconds = pd.Index(sorted(base_floor.unique()))

    # THE SLICE REFUSAL SITS HERE, AND HERE IS WHY. R255 §5.
    #
    # Two paths reach the availability probe -- `leakaudit.run_probe_a`, which
    # `__init__.py` exports, and `cli._run_availability` behind `leakaudit run`
    # -- and the second calls the first. They JOIN at this function, so one
    # refusal covers both and there is no second copy to fall out of step with
    # this one. The alternative shape, a check in the CLI, would leave the
    # exported library entry unguarded, which is the larger of the two surfaces
    # for a tool whose point is being embedded.
    #
    # It sits AFTER `seconds` and BEFORE `picked` for a reason that is not
    # arrangement: the padding seconds must be removed from the candidate set
    # before the stride samples it, or the stride would spend cohorts on rows
    # that are context, and `n_cohorts` would count subjects that were never
    # probed as subjects.
    if slice_from is not None:
        from . import slicing
        plan = slicing.plan_slice(raw=raw, model=model, slice_from=slice_from,
                                  padding=padding,
                                  declared_bar_duration=bar_duration)
        probed, context = slicing.split_seconds(seconds, plan)
        res.slice_plan = plan
        res.context_seconds = tuple(context)
        res.notes.append(slicing.context_note(plan, len(context)))
        seconds = pd.Index(probed)
    elif not isinstance(padding, str) or padding != NOT_DECLARED:
        # A padding with no slice is a declaration about nothing. Refusing is
        # cheap and the alternative is silently ignoring an argument the caller
        # believed was protecting them.
        raise ProbeError(
            "`padding=` was declared without `slice_from=`. Padding describes "
            "the data before a slice's first probed cohort; with no slice "
            "there is no such boundary and nothing was excluded from probing.")

    picked = seconds[::cohort_stride][:max_cohorts]
    res.n_cohorts = len(picked)
    if res.n_cohorts == 0:
        return res

    # THE COMPARATOR TRAVELS WITH THE RESULT. R216 §2(b).
    #
    # Two runs under different tie branches must not be distinguishable only by
    # a config file nobody kept. The non-default branch is stated loudly because
    # a result produced under it is not the same object as one produced under the
    # default; the default is stated quietly because a reader still has to be
    # able to tell which they are holding.
    if model.ties_available:
        res.notes.append(
            "comparator: `a(j,c) <= d(i)` -- ties AVAILABLE, the registered "
            "default (PREREG.md section 2.3). A cell whose instant equals the "
            "decision instant counts as arrived.")
    else:
        res.notes.append(
            "COMPARATOR IS NOT THE DEFAULT: `a(j,c) < d(i)` -- ties "
            "UNAVAILABLE. A cell whose instant equals the decision instant is "
            "counted as NOT arrived, so rows stamped exactly at an aggregate's "
            "completion instant are findings here and are not under the default. "
            "Every finding below was computed under that branch.")

    picked_set = set(picked)
    corrupt = {k: v.copy() for k, v in raw.items()}
    rng = np.random.default_rng(seed)

    res.unmodelled_frames = tuple(
        sorted(k for k in raw if k not in model.aggregate_frames))
    if res.unmodelled_frames:
        res.notes.append(
            "NOT PROBED: %s. %s in `raw` and absent from the model's aggregate "
            "frames, so nothing in %s was perturbed and any silence downstream "
            "of %s is `none` -- a probe that did not happen -- rather than "
            "`observed_silence`. Declare %s, or read that silence as the absence "
            "it is."
            % ((", ".join(res.unmodelled_frames),)
               + (("They are", "them", "them", "them")
                  if len(res.unmodelled_frames) > 1
                  else ("It is", "it", "it", "it"))))

    touched = 0
    for fname, keycol in model.aggregate_frames.items():
        if fname not in corrupt or corrupt[fname] is None:
            res.notes.append("aggregate frame %r absent from raw; not corrupted" % fname)
            continue
        f = corrupt[fname]
        if keycol not in f.columns:
            raise ProbeError("frame %r has no key column %r" % (fname, keycol))
        # TIMEZONE ALIGNMENT, AND IT IS NOT A DETAIL.
        #
        # `trades.ts_event` is datetime64[ns, UTC] while `snap.timestamp` and
        # `magg.ts_floor` are naive. `isin` between aware and naive NEVER
        # matches, so the trades frame was silently never corrupted -- an
        # all-False mask that looks exactly like "no cells were unavailable".
        # The decision stamps define the frame of reference; a key in another
        # frame is converted into it, never compared across.
        key = pd.to_datetime(f[keycol])
        if getattr(key.dt, "tz", None) is not None:
            key = key.dt.tz_convert("UTC").dt.tz_localize(None) if d.dt.tz is None \
                else key.dt.tz_convert(d.dt.tz)
        elif d.dt.tz is not None:
            key = key.dt.tz_localize(d.dt.tz)
        key_floor = key.dt.floor("s")
        # FLOORING IS APPLIED AND REPORTED, NEVER APPLIED SILENTLY. R207 Q1.
        #
        # A key that is already a wall-clock second floors to itself and there is
        # nothing to say. A key that is a raw event stamp -- `trades.ts_event` is
        # one -- does not, and the instant this probe uses is then
        # `floor(key) + window`, NOT `key + window`. Applying the aggregate
        # contract to a declared aggregate frame is not inference: it is the rule
        # the declaration states. But it is a rule the caller did not write down,
        # and the invisible half of exactly this arithmetic is what let a
        # docstring diverge from the behaviour for weeks (D-V30A-43). So it is
        # named, with the measured fraction, in the run's own output.
        n_key = len(key_floor)
        if n_key:
            on_boundary = int((key == key_floor).sum())
            if on_boundary < n_key:
                res.notes.append(
                    "key %r of frame %r is not on second boundaries (%.4f%% "
                    "are); flooring to `floor(%s) + %s` per the aggregate "
                    "contract. The declared availability instant of every cell "
                    "of this frame is the end of the wall-clock second its key "
                    "falls in, not one window after the key itself."
                    % (keycol, fname, 100.0 * on_boundary / n_key,
                       keycol, _window_text(model.window)))
        mask = key_floor.isin(picked_set)
        # PER-FRAME, NOT IN TOTAL. The original guard summed `touched` across
        # frames and raised only if EVERY frame matched nothing -- so magg's 250
        # masked trades' zero. An aggregate guard hides a per-member failure.
        if not mask.any():
            raise ProbeError(
                "frame %r matched NO corrupted second. Its key %r may be in a "
                "different timezone or resolution from the decision stamps; a "
                "frame that is never corrupted reports a silence about the "
                "harness, not about the pipeline." % (fname, keycol))
        num = [c for c in f.columns
               if c != keycol and pd.api.types.is_numeric_dtype(f[c])]
        if column_modes:
            # THE CONFLICT IS SURFACED, NOT RESOLVED SILENTLY. R205 §3.3.
            #
            # `aggregate_frames` selects frames and supplies a key; `column_modes`
            # refines which cells of a column are perturbed. A column of a
            # selected frame with NO declared mode falls back to the frame's rule
            # -- and whether that is a declaration the user made at frame level or
            # a default the tool applied is a question neither the registration
            # nor AVAILABILITY_MODES.md settles, because `aggregate_frames` is
            # this tool's own coarse mechanism and not registered vocabulary.
            #
            # So the code does one thing and SAYS it did, naming the columns. A
            # reader who thinks the other reading is right can see exactly which
            # columns the answer depends on.
            fell_back = sorted(c for c in num if c not in column_modes)
            if fell_back:
                res.notes.append(
                    "frame %r: %s took the FRAME rule (key + window) because no "
                    "per-column mode was declared for %s. Whether a frame-level "
                    "declaration covers its columns, or a column without its own "
                    "mode is undeclared, is not settled by the registration or by "
                    "the modes document -- this run took the first reading, and "
                    "names the columns so the choice is visible."
                    % (fname, ", ".join(fell_back),
                       "them" if len(fell_back) > 1 else "it"))
        for c in num:
            # PER-COLUMN SELECTION, AND THE WHOLE-FRAME PATH IS THE SPECIAL CASE.
            # R205 §3. Without modes the mask is the frame's, unchanged. With a
            # mode for this column, the cell's own availability instant decides:
            # a cell is corrupted when the instant it BECOMES knowable falls in a
            # selected second, which for the frame rule is key + window and
            # reduces to exactly the mask above.
            cell_mask = mask
            spec = None if not column_modes else column_modes.get(c)
            if spec is not None:
                from .modes import ROUTE_TAKEN as _routes
                from .modes import availability as _availability
                _before = len(_routes)
                a = _availability(f, c, spec, timestamp_column=keycol,
                                  declared_bar_duration=bar_duration)
                # THE ROUTE IS NAMED WHERE THE USER MEETS IT. R223 §2(b).
                # `PREREG.md` line 255 offers two routes for `bar_duration` --
                # a fixed value or inference -- and names no default between
                # them, while the config file carries no key for the first. So
                # a user declaring `at_bar_close` gets one of two registered
                # options chosen for them, and the least this run can do is say
                # which. Selecting between two registered routes without the
                # output naming which is the tie comparator's defect again.
                for _r, _v, _info in _routes[_before:]:
                    if _r == "inferred":
                        res.notes.append(
                            "column %r of frame %r declares `at_bar_close`, and "
                            "its bar duration was INFERRED from successive "
                            "timestamps because none was declared. PREREG.md "
                            "line 255 names two routes -- a fixed value or "
                            "inference -- and names no default between them, "
                            "so the route was chosen for you and is named "
                            "here rather than left to be deduced. Declare "
                            "`bar_duration_seconds` to take the fixed-value "
                            "route instead. %s"
                            % (c, fname, _inference_frame(_info)))
                a = align_key(pd.to_datetime(a), d, frame=fname, column=c)
                cell_mask = (a - model.window).dt.floor("s").isin(picked_set).to_numpy()
                if not cell_mask.any():
                    res.notes.append(
                        "column %r of frame %r declares mode %r and no cell of it "
                        "becomes knowable in any selected second, so it was not "
                        "perturbed. Its silence is `none`, not `observed_silence`."
                        % (c, fname, getattr(spec, "mode", spec)))
            # A LARGE, DETERMINISTIC PERTURBATION. Not noise: the question is
            # whether the value is READ, and a perturbation that could coincide
            # with the original would produce a false silence.
            #
            # THE COLUMN'S DTYPE IS PRESERVED. A first version wrote floats into
            # every numeric column and pandas refused on the int64 ones -- and
            # casting them to float instead would have been worse than the error:
            # a dtype change is itself a perturbation, and the builder's
            # behaviour on a promoted column is a different question from whether
            # it reads the value. Integers get an integer offset.
            n = int(cell_mask.sum())
            if pd.api.types.is_integer_dtype(f[c]):
                # THE PERTURBATION WRAPS INSIDE THE DTYPE'S RANGE.
                #
                # A flat +1_000_000 overflowed `uint8` and pandas refused --
                # after the same offset had already been rejected on int64 as a
                # float. Widening the column would be a SECOND perturbation
                # (R152 §2.2), so the offset is made to fit instead: modular
                # within [iinfo.min, iinfo.max], with a non-zero offset so the
                # new value is GUARANTEED to differ from the original. A
                # perturbation that could coincide produces a false silence.
                info = np.iinfo(f[c].dtype)
                lo, hi = int(info.min), int(info.max)
                headroom = min(1000, max(1, hi - lo))
                off = 1 + rng.integers(0, headroom, n)
                # `cell_mask`, NOT `mask`. R224. When per-column modes are
                # declared these differ, and this line read the frame-level mask
                # while `off` was sized from `cell_mask` and the write below
                # targets `cell_mask` -- so an integer column under a per-column
                # mode raised a broadcast error. A partial conversion left from
                # R205, invisible because that round's discriminating positive
                # used a FLOAT column and never entered this branch.
                #
                # No published figure moves, and that was checked: with no
                # column_modes `cell_mask is mask`, which is every Phase 1 run,
                # and the whole-frame guard re-measures it.
                vals = f.loc[cell_mask, c].to_numpy()
                # ADD, OR SUBTRACT WHERE ADDING WOULD LEAVE THE RANGE. A modular
                # wrap was tried and overflowed: int64's span is 2**64 and does
                # not fit in int64. Choosing the DIRECTION per element needs no
                # arithmetic wider than the column itself, works at every width,
                # and still guarantees new != old because the offset is >= 1.
                up = vals <= (hi - headroom)
                new = np.where(up, vals + off, vals - off)
                f.loc[cell_mask, c] = new.astype(f[c].dtype)
            elif pd.api.types.is_bool_dtype(f[c]):
                f.loc[cell_mask, c] = ~f.loc[cell_mask, c].to_numpy()
            else:
                vals = f.loc[cell_mask, c].to_numpy(dtype=float, copy=True)
                f.loc[cell_mask, c] = vals + 1.0e6 + rng.standard_normal(n)
        touched += int(mask.sum())
        corrupt[fname] = f
    if touched == 0:
        # NAME THE CAUSE, NOT THE SYMPTOM. R210 item 4.
        #
        # "no aggregate cells matched" is true and is a CONSEQUENCE. The walk
        # hit this with one declared frame misspelled -- `scan` for `scans` --
        # and the message sent the reader looking at seconds and keys when the
        # fact that fixes it is that a declared name matches nothing supplied.
        # The standard applied here is the one this package already sets in the
        # v2-model refusal: say what is wrong, then say the routes out.
        declared = sorted(model.aggregate_frames)
        supplied = sorted(raw)
        absent = [f for f in declared if f not in raw]
        if absent:
            raise ProbeError(
                "declared aggregate frame(s) %s were not supplied, so nothing "
                "was corrupted and the probe would report silence about itself. "
                "Declared: %s. Supplied: %s. Correct the name in the model file, "
                "or supply the frame, or drop it from `aggregate_frames` -- in "
                "which case anything downstream of it is `none`, not "
                "`observed_silence`."
                % (", ".join(repr(a) for a in absent),
                   ", ".join(repr(d) for d in declared),
                   ", ".join(repr(s) for s in supplied)))
        raise ProbeError(
            "no aggregate cells matched the corrupted seconds, so the probe "
            "would report silence about itself. Every declared frame (%s) was "
            "supplied, so the mismatch is in the KEYS rather than the names: no "
            "row of them falls in any selected second. Check that the key "
            "column holds the window key, and that its seconds overlap the "
            "decision column's."
            % ", ".join(repr(d) for d in declared))
    res.notes.append("corrupted %d aggregate row(s) across %d second(s)" % (touched, res.n_cohorts))

    after = build(corrupt)
    if len(after) != len(base) or list(after.columns) != list(base.columns):
        raise ProbeError("the corrupted build changed shape (%s -> %s); rows cannot "
                         "be compared positionally"
                         % ((len(base), len(base.columns)), (len(after), len(after.columns))))

    fb = _fast_fingerprint(base)
    fa_ = _fast_fingerprint(after)
    moved = (fb.to_numpy() != fa_.to_numpy())

    # PER-COLUMN ATTRIBUTION, computed once for every column rather than per
    # cohort: `moved_col[c]` is a boolean row mask for column c.
    moved_col = {}
    for c in base.columns:
        a_ = base[c].astype("string").fillna("<NA>").to_numpy()
        b_ = after[c].astype("string").fillna("<NA>").to_numpy()
        m = a_ != b_
        if m.any():
            moved_col[c] = m

    # THE TIE BRANCH, WIRED. R216 §2, and it was inert before this.
    #
    # A cell of second F becomes knowable at a = F + window. A decision row at
    # instant d is fed it illegally when the model says it had not arrived:
    #
    #   d inside [F, F+window)   a > d   unavailable under BOTH branches
    #   d == F + window exactly  a == d  THE TIE. `available` admits it;
    #                                    `unavailable` refuses it.
    #   d after  F + window      a < d   available under both
    #
    # Attribution is by floored second, so the tie rows -- those stamped exactly
    # at the aggregate's completion instant -- sit in the `nxt` bucket together
    # with rows merely somewhere in the following second. Under the default they
    # belong there. Under `ties_available=False` they are findings, and they are
    # the ONLY rows the two branches disagree about.
    #
    # PREREG.md §2.3 registers both branches and states that `unavailable`
    # "remains selectable"; §4.3 writes the inequalities for both. So this is a
    # registered capability being completed, not a tool-level extra -- the
    # structural read is recorded at MV-12. No published figure moves: every
    # recorded result was produced under the default, whose behaviour is
    # unchanged, and that was measured rather than assumed.
    # A row is AT THE TIE when its own stamp sits exactly on a second boundary:
    # it then belongs to the `nxt` bucket of cohort F = base_floor - window,
    # whose instant is F + window = base_floor = d. Written `d == base_floor`
    # rather than `d == f_sec + window` because the first is a property of the
    # row and the second was got wrong by exactly one window on the first
    # attempt -- caught by the discriminating positive, which is what it is for.
    at_tie = (d == base_floor).to_numpy()

    for f_sec in picked:
        in_sec = (base_floor == f_sec).to_numpy()
        nxt = (base_floor == f_sec + model.window).to_numpy()
        if not model.ties_available:
            tie_here = nxt & at_tie
            in_sec = in_sec | tie_here
            nxt = nxt & ~tie_here
        feats = tuple(sorted(c for c, m in moved_col.items() if (m & in_sec).any()))
        res.cohorts.append(CohortResult(
            second=f_sec,
            rows_in_second=int(in_sec.sum()),
            moved_in_second=int((moved & in_sec).sum()),
            moved_next_second=int((moved & nxt).sum()),
            features_in_second=feats,
        ))
    return res
