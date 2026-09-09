"""R260 §3(c). Does every cell L3.1 perturbs have a(j) = F + 1 exactly?

F is the picked (corrupted) second; a(j) is the cell's DECLARED availability
instant. The question decides the round, so it is measured rather than argued.

TWO SELECTION PATHS EXIST IN `run_probe_a` and they are different arithmetic:

    frame rule (no column_modes)   mask      = floor(key).isin(picked)
                                   a(j)      = floor(key) + window
                                   so a(j)   = F + window, EXACTLY

    per-column mode (v3)           cell_mask = floor(a - window).isin(picked)
                                   a(j)      = the column's own instant
                                   so a(j) in [F + window, F + window + 1)

This script measures both, on one frame set, and then measures the CONSEQUENCE:
whether a leak the registered comparator calls a finding is reported as one.

Written with the Write tool per D2.1. Read-only against the repository.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "src")

from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402
from leakaudit.modes import ColumnMode  # noqa: E402

T0 = pd.Timestamp("2026-01-01 00:00:00")
SEC = pd.Timedelta(seconds=1)
N = 12
OFFSET = pd.Timedelta(milliseconds=500)


def frames():
    """One aggregate frame whose key sits mid-second, and nothing else.

    Row n carries key `T0 + n s + 0.5 s` and value n. A mid-second key is not
    exotic: the acceptance fixture's `trades.ts_event` is one on 397,408 of its
    397,457 rows, median offset 467.83 ms, measured and recorded in
    `AvailabilityModel`'s own docstring.
    """
    k = [T0 + n * SEC + OFFSET for n in range(N)]
    return {"agg": pd.DataFrame({"k": k, "v": np.arange(N, dtype="float64")})}


def build(raw):
    """Output row m decides at `T0 + m s` and reads the agg row keyed 0.5 s LATER.

    That is a leak under every rule in play: the cell's instant is 0.5 s after
    the decision instant under the per-column declaration, and 1 s after it
    under the frame rule. Both say unavailable; the registered comparator says
    finding.
    """
    agg = raw["agg"]
    d = [T0 + m * SEC for m in range(N)]
    return pd.DataFrame({"d": d, "x": agg["v"].to_numpy()})


def selection(model, column_modes):
    """(f_sec, a(j)) for every cell the probe would perturb, computed the way
    `run_probe_a` computes it -- same expressions, so this reports the shipped
    selection and not a paraphrase of it."""
    raw = frames()
    base = build(raw)
    d = pd.to_datetime(base["d"])
    picked = pd.Index(sorted(d.dt.floor("s").unique()))
    pset = set(picked)
    f = raw["agg"]
    key = pd.to_datetime(f["k"])
    out = []
    if column_modes:
        from leakaudit.modes import availability as _availability
        a = _availability(f, "v", column_modes["v"], timestamp_column="k")
        sel = (a - model.window).dt.floor("s")
        for j in range(len(f)):
            if sel.iloc[j] in pset:
                out.append((sel.iloc[j], a.iloc[j]))
    else:
        kf = key.dt.floor("s")
        for j in range(len(f)):
            if kf.iloc[j] in pset:
                out.append((kf.iloc[j], kf.iloc[j] + model.window))
    return out


def report_identity(label, pairs, window):
    deltas = sorted({(a - fsec) for fsec, a in pairs})
    exact = all((a - fsec) == window for fsec, a in pairs)
    print("  %-28s cells perturbed: %d" % (label, len(pairs)))
    print("  %-28s a(j) - F values : %s"
          % ("", ", ".join(str(x) for x in deltas)))
    print("  %-28s a(j) == F + window for every cell: %s"
          % ("", "YES" if exact else "NO"))
    return exact


def main():
    print("=" * 74)
    print("R260 section 3(c) -- is a(j) = F + window exact on every perturbed cell?")
    print("=" * 74)
    print("frames: 1 aggregate frame, %d rows, key at T0 + n s + %s" % (N, OFFSET))
    print("model : window=%s, ties_available=True (the registered default)" % SEC)
    print()

    model = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")

    print("PATH 1 -- frame rule, no column_modes (every Phase 1 run)")
    exact_frame = report_identity("frame rule", selection(model, None), SEC)
    print()

    modes = {"v": ColumnMode("at_timestamp")}
    print("PATH 2 -- per-column mode `at_timestamp`, a v3 declared config")
    exact_modes = report_identity("column mode", selection(model, modes), SEC)
    print()

    print("-" * 74)
    print("THE CONSEQUENCE -- same frames, same builder, same cohorts.")
    print("The leak: output row m decides at T0 + m s and reads a cell whose")
    print("declared instant is T0 + m s + %s. Unavailable under the comparator" % OFFSET)
    print("on both paths, so the registered rule says FINDING on both.")
    print("-" * 74)

    raw = frames()
    print("  ALL COHORTS AT ONCE (stride 1) -- one rebuild corrupts every")
    print("  selected cell, so every output row moves and each cohort's own row")
    print("  moved for a reason that may belong to a different cohort. The")
    print("  verdict is right here by construction, not by attribution:")
    r1 = run_probe_a(raw, build, model, side="frame-rule",
                     cohort_stride=1, max_cohorts=100)
    print("    frame rule  : verdict=%-18s findings=%d  cohorts=%d"
          % (r1.verdict(), len(r1.findings), r1.n_cohorts))
    r2 = run_probe_a(raw, build, model, side="column-mode",
                     cohort_stride=1, max_cohorts=100, column_modes=modes)
    print("    column mode : verdict=%-18s findings=%d  cohorts=%d"
          % (r2.verdict(), len(r2.findings), r2.n_cohorts))
    print()
    print("  ONE COHORT (max_cohorts=1) -- attribution is now unambiguous:")
    print("  exactly one cell is corrupted and exactly one output row moves.")
    r1s = run_probe_a(raw, build, model, side="frame-rule-1",
                      cohort_stride=1, max_cohorts=1)
    c1 = r1s.cohorts[0]
    print("    frame rule  : cohort F=%s  a(j)=F+%s  moved_in=%d moved_next=%d "
          "-> %s"
          % (c1.second, SEC, c1.moved_in_second, c1.moved_next_second,
             r1s.verdict()))
    r2s = run_probe_a(raw, build, model, side="column-mode-1",
                      cohort_stride=1, max_cohorts=1, column_modes=modes)
    c2 = r2s.cohorts[0]
    print("    column mode : cohort F=%s  a(j)=F+%s  moved_in=%d moved_next=%d "
          "-> %s"
          % (c2.second, pd.Timedelta(seconds=1) + OFFSET,
             c2.moved_in_second, c2.moved_next_second, r2s.verdict()))
    print()
    print("  The moved row decides at F + 1s. The corrupted cell's declared")
    print("  instant is F + 1.5s. The registered comparator is a(j) > d(i),")
    print("  so F + 1.5s > F + 1s is UNAVAILABLE and the row is a FINDING.")
    print("  `moved_in_second` puts it in `nxt` and calls the cohort silent.")
    print()

    print("-" * 74)
    print("SECOND INPUT -- window_seconds != 1, no column_modes.")
    print("`nxt` is `base_floor == f_sec + window`, so with window=2s the rows")
    print("in [F+1s, F+2s) are unavailable (a = F+2s > d) and land in NEITHER")
    print("bucket: not a finding, not a silence, not counted.")
    print("-" * 74)
    m2 = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d",
                           window=pd.Timedelta(seconds=2))
    pairs2 = selection(m2, None)
    report_identity("frame rule, window=2s", pairs2, SEC)
    print("  %-28s a(j) == F + 1s for every cell: %s"
          % ("", "YES" if all((a - f) == SEC for f, a in pairs2) else "NO"))
    r3 = run_probe_a(raw, build, m2, side="window-2s",
                     cohort_stride=1, max_cohorts=100)
    counted = sum(c.rows_in_second for c in r3.cohorts)
    print("  %-28s verdict=%s findings=%d rows counted in-second across cohorts=%d"
          % ("", r3.verdict(), len(r3.findings), counted))
    print("  %-28s moved_next_second total=%d (f_sec + 2s is a boundary, so `nxt` matches)"
          % ("", sum(c.moved_next_second for c in r3.cohorts)))

    m3 = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d",
                           window=pd.Timedelta(milliseconds=1500))
    r4 = run_probe_a(raw, build, m3, side="window-1500ms",
                     cohort_stride=1, max_cohorts=100)
    print("  %-28s window=1.5s: moved_next_second total=%d "
          "(f_sec + 1.5s is never a second boundary, so `nxt` can never match)"
          % ("", sum(c.moved_next_second for c in r4.cohorts)))

    print()
    print("=" * 74)
    print("IDENTITY HOLDS ON PATH 1 (default window): %s" % exact_frame)
    print("IDENTITY HOLDS ON PATH 2 (declared column mode): %s" % exact_modes)
    print("=" * 74)


if __name__ == "__main__":
    main()
