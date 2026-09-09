"""R261 §3. R205's 25-against-0, re-measured under the repaired attribution rule.

    PYTHONPATH=. py -3.12 evidence/session/r261_remeasure_r205.py

WHAT WAS READ AND WHY THE READING WAS SUSPENDED. D-V30A-49 records that the
whole-frame and per-column paths gave different answers on the same data -- 25
cohorts with a finding against 0 -- on a frame carrying a figure published half
an hour before the row using it, and reads the 0 as a false positive that the
per-column declaration correctly suppressed. D-V30A-98 then measured the
per-column bucket geometry producing a 0 on a leak the registered comparator
flags, so a 0 there is consistent with both explanations and the measurement as
taken does not separate them. R261 §3 suspends the reading until the pair is
re-measured under the repaired rule.

THE FIXTURE IS R205'S OWN, not a reconstruction: `tests/phase1/test_modes_wiring.py`
carries it, and this script imports it rather than restating it, so the inputs
are the inputs and not a copy that could drift from them.

WHAT SEPARATES THE TWO EXPLANATIONS. Under the repaired rule a cohort reports
three counts instead of two, and the third -- BAND -- is the state the old
geometry had nowhere to put. If the per-column path still reports no findings and
no band rows, the 0 is a real silence and R205's reading stands. If findings
appear, the 0 was the geometry. If band rows appear, the run cannot attribute
the movement and neither reading is supported by it.

Written with the Write tool per D2.1. Read-only against the repository.
"""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path.cwd()
for p in (str(REPO), str(REPO / "src"), str(REPO / "tests" / "phase1")):
    if p not in sys.path:
        sys.path.insert(0, p)

import test_modes_wiring as fx                                # noqa: E402
from leakaudit.modes import AT_SOURCE_TIMESTAMP, ColumnMode   # noqa: E402


def counts(res):
    return (sum(c.moved_in_second for c in res.cohorts),
            sum(c.moved_in_band for c in res.cohorts),
            sum(c.moved_next_second for c in res.cohorts))


def main() -> int:
    modes = {"released": ColumnMode(AT_SOURCE_TIMESTAMP, "released_at")}
    whole = fx._run(modes=None)
    per = fx._run(modes=modes)

    print("=" * 74)
    print("R261 section 3 -- R205's pair under the repaired attribution rule")
    print("=" * 74)
    print("fixture: tests/phase1/test_modes_wiring.py, imported not copied")
    print("         %d rows, release lag %s, stride 13, max_cohorts 25, seed 7"
          % (fx.N, fx.LAG))
    print()
    hdr = "%-14s %-22s %8s %8s %8s %10s"
    print(hdr % ("path", "verdict", "finding", "band", "liveness", "cohorts"))
    for label, res in (("whole-frame", whole), ("per-column", per)):
        f, b, l = counts(res)
        print(hdr % (label, res.verdict(), f, b, l, len(res.cohorts)))
    print()

    fp, bp, _ = counts(per)
    print("cohorts with a finding: whole-frame %d, per-column %d"
          % (len(whole.findings), len(per.findings)))
    print()

    # WAS THE COLUMN THE BUILDER READS ACTUALLY PERTURBED? Asked before the
    # counts are read, because a 0 from a column nothing touched is not a
    # silence at all, and the first version of this script did not ask -- it
    # read the 0 as a surviving silence and would have reported R205's reading
    # as supported. The run says so in its own notes; nothing was reading them.
    read_col = "released"
    unperturbed = [n for n in per.notes
                   if ("column %r" % read_col) in n and "not perturbed" in n]
    print("was %r perturbed under the per-column declaration? %s"
          % (read_col, "NO" if unperturbed else "yes"))
    for n in unperturbed:
        print("    run note: %s" % n)
    print()

    print("READS AS:")
    if unperturbed:
        print("  NEITHER READING. The builder reads only %r, and under the" % read_col)
        print("  per-column declaration that column's instants are half an hour")
        print("  before the probed range, so NO cell of it was perturbed. The 0")
        print("  is `none` -- a probe that did not happen -- and not a silence.")
        print("  It is not evidence that the coarse path over-reported, and not")
        print("  evidence that it did not. R205's reading is UNSUPPORTED by")
        print("  this fixture, and so is its negation.")
        print()
        print("  AND THE RUN-LEVEL VERDICT OVERSTATES IT: `observed_silence` is")
        print("  reported while the only column the builder reads was never")
        print("  perturbed. The note carries the truth and the verdict does not.")
    elif fp > 0:
        print("  the per-column path now reports %d finding row(s) where it" % fp)
        print("  reported none. The 0 was the geometry, not the declaration,")
        print("  and R205's reading is REFUTED by its own inputs.")
    elif bp:
        print("  the per-column path reports %d BAND row(s) and no findings." % bp)
        print("  The movement cannot be attributed, so this run supports")
        print("  NEITHER reading and the question stays open.")
    else:
        print("  the per-column silence SURVIVES the repair on a column that WAS")
        print("  perturbed. The 0 is a real silence under the comparator and")
        print("  R205's reading is supported.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
