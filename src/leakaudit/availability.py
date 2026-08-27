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
from typing import Callable, Mapping, Sequence

import numpy as np
import pandas as pd

SECOND = pd.Timedelta(seconds=1)


class ProbeError(RuntimeError):
    """The probe cannot answer, and says so rather than returning silence."""


@dataclass(frozen=True)
class AvailabilityModel:
    """The declared model. Supplied to the probe; never inferred by it.

    `aggregate_frames` are the frames whose rows are wall-clock-second
    aggregates keyed by `key_column`; their declared availability instant is
    `key + window`. `decision_column` is the output's decision instant.
    """
    aggregate_frames: Mapping[str, str]          # frame name -> key column
    decision_column: str = "timestamp"
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
    def finding(self) -> bool:
        return self.moved_in_second > 0


@dataclass
class ProbeAResult:
    side: str
    n_cohorts: int
    cohorts: list = field(default_factory=list)
    determinism_ok: bool = True
    notes: list = field(default_factory=list)

    @property
    def findings(self):
        return [c for c in self.cohorts if c.finding()]

    def verdict(self) -> str:
        if not self.determinism_ok:
            return "could_not_run(determinism)"
        if not self.cohorts:
            return "could_not_run(no_cohorts)"
        return "finding" if self.findings else "observed_silence"


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
                cohort_stride: int = 97,
                max_cohorts: int = 400,
                seed: int = 20260828) -> ProbeAResult:
    """Corrupt a sparse set of seconds, rebuild once, and read WHICH rows moved.

    `cohort_stride` keeps corrupted seconds far apart so a moved row can be
    attributed to exactly one corrupted second. A stride of 1 would corrupt
    adjacent seconds and make "own second" and "previous second"
    indistinguishable -- which is the entire discrimination.
    """
    res = ProbeAResult(side=side, n_cohorts=0)

    base = build(dict(raw))
    base2 = build(dict(raw))
    if not base.equals(base2):
        res.determinism_ok = False
        res.notes.append("the builder is not deterministic across two clean runs; "
                         "no corruption result from it could be attributed")
        return res

    dcol = model.decision_column
    if dcol not in base.columns:
        raise ProbeError("the decision column %r is not in the built output" % dcol)
    d = pd.to_datetime(base[dcol])
    base_floor = d.dt.floor("s")

    # The corrupted seconds: sparse, deterministic, derived from the data's own
    # range rather than chosen.
    seconds = pd.Index(sorted(base_floor.unique()))
    picked = seconds[::cohort_stride][:max_cohorts]
    res.n_cohorts = len(picked)
    if res.n_cohorts == 0:
        return res

    picked_set = set(picked)
    corrupt = {k: v.copy() for k, v in raw.items()}
    rng = np.random.default_rng(seed)

    touched = 0
    for fname, keycol in model.aggregate_frames.items():
        if fname not in corrupt or corrupt[fname] is None:
            res.notes.append("aggregate frame %r absent from raw; not corrupted" % fname)
            continue
        f = corrupt[fname]
        if keycol not in f.columns:
            raise ProbeError("frame %r has no key column %r" % (fname, keycol))
        key_floor = pd.to_datetime(f[keycol]).dt.floor("s")
        mask = key_floor.isin(picked_set)
        if not mask.any():
            continue
        num = [c for c in f.columns
               if c != keycol and pd.api.types.is_numeric_dtype(f[c])]
        for c in num:
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
            n = int(mask.sum())
            if pd.api.types.is_integer_dtype(f[c]):
                bump = 1_000_000 + rng.integers(0, 1000, n)
                f.loc[mask, c] = f.loc[mask, c].to_numpy() + bump
            elif pd.api.types.is_bool_dtype(f[c]):
                f.loc[mask, c] = ~f.loc[mask, c].to_numpy()
            else:
                vals = f.loc[mask, c].to_numpy(dtype=float, copy=True)
                f.loc[mask, c] = vals + 1.0e6 + rng.standard_normal(n)
        touched += int(mask.sum())
        corrupt[fname] = f
    if touched == 0:
        raise ProbeError("no aggregate cells matched the corrupted seconds; the "
                         "probe would report silence about itself")
    res.notes.append("corrupted %d aggregate row(s) across %d second(s)" % (touched, res.n_cohorts))

    after = build(corrupt)
    if len(after) != len(base) or list(after.columns) != list(base.columns):
        raise ProbeError("the corrupted build changed shape (%s -> %s); rows cannot "
                         "be compared positionally"
                         % ((len(base), len(base.columns)), (len(after), len(after.columns))))

    fb = _fast_fingerprint(base)
    fa_ = _fast_fingerprint(after)
    moved = (fb.to_numpy() != fa_.to_numpy())

    for f_sec in picked:
        in_sec = (base_floor == f_sec).to_numpy()
        nxt = (base_floor == f_sec + model.window).to_numpy()
        res.cohorts.append(CohortResult(
            second=f_sec,
            rows_in_second=int(in_sec.sum()),
            moved_in_second=int((moved & in_sec).sum()),
            moved_next_second=int((moved & nxt).sum()),
        ))
    return res
