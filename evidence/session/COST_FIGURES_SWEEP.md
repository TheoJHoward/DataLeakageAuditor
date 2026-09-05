# Every figure quoted as a cost — did the run finish?

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures. Every count carries its command and its resolved
interpreter version where one was recorded.

**The finding this sweeps for.** R230 found that two figures this project quoted
as `sys.setprofile`'s cost — *"no answer in fifteen minutes"* and *"over
thirty-four minutes against a usual eight and a half"* — came from runs that were
**stopped**, not runs that finished. A stopped run licenses *"at least N"* and
nothing more; both were used to license *"prohibitive"*, across four rounds, in a
project whose central discipline is that a figure carries its population
(D-V30A-64).

**The population.** Every duration currently quoted as a cost in
`evidence/session/`, `tools/`, `README.md` and `INSTALL.md`, found by scanning
for time-valued figures and discarding the ones that are not costs — window
lengths, bar durations, flooring boundaries, column names like `buy_volume_10s`.

**Three states, and the third is not a failure of the sweep.** *Completed* — it is
a cost. *Stopped* — it is a lower bound and is rewritten as one wherever quoted.
*Unknown* — say unknown.

---

## The sweep

| figure | where | completed? | disposition |
|---|---|---|---|
| **"no answer in fifteen minutes against an unprofiled 288 seconds"** | `tools/probe_path_guard.py`, `METHOD_VERIFICATIONS.md` MV-16 | **STOPPED** | **Lower bound.** The real ratio on that recorder's workload is ×1.8 (379.5 s against 209.2 s). Rewritten below. |
| **"over thirty-four minutes against a usual eight and a half"** | `tools/probe_path_guard.py`, `GUARD_COST_CRITERION.md` | **STOPPED** — *"killed rather than waited out"*, and the file says so | **Lower bound**, and it is already worded as one at both sites (*"over"*, *"killed rather than waited out"*). It is the upper behavioural anchor of the 20-minute criterion, and for that use a lower bound is the right instrument: it says somebody would not wait this long. |
| unprofiled guard side, **209.2 s** | MV-16, `GUARD_COST_CRITERION.md` | completed | cost |
| `sys.monitoring` guard side, **185.8 s** | MV-16, `GUARD_COST_CRITERION.md` | completed | cost |
| `sys.setprofile` guard side, **379.5 s** | MV-16, `GUARD_COST_CRITERION.md` | completed | cost |
| guard sides **180 / 179, 226 / 224, 266 / 265 s** | round reports R227–R228 | completed | cost |
| fixture capture **38–46.4 s** | guard output, `ROUND_STATE.md` | completed | cost |
| **288.49 s** — the opt-in fixture tests unprofiled | MV, `probe_path_guard.py` | completed (`10 passed in 288.49 s`) | cost |
| **288.41 s** — the same under `sys.monitoring` | `probe_path_guard.py` | completed | cost |
| floor suite **37–45 s** | `INSTALL.md`, `floor_check.py` | completed | cost |
| dev suite **43–56 s** | round reports | completed | cost |
| Pearson **0.097 s**, Spearman **2.819 / 1.409 s**, whole check **1.291 s** | `LABEL_CHECK_NAME.md` | completed, best of three | cost |
| **8 seconds** — the column-only read | MV | completed | cost |
| synthetic benchmark baselines **0.04–0.05 s** | MV-16, TB-24 | completed | cost, **and useless** — TB-24 records why: the baseline did not move, so the measurement contained no per-call cost at all |
| **63 minutes** — between the corner measurement and the commit that broke it | `HAND_TYPED_FIGURES.md`, D-V30A-58 | not a cost | an interval between two commits, read from their timestamps |

**Two stopped, twelve completed, none unknown.** The population is small because
this project quotes few durations, and both stopped figures were already about the
same recorder.

---

## What was rewritten, and what was left alone

**Rewritten:** the fifteen-minute figure in `tools/probe_path_guard.py` and in
MV-16. It was the one being read as a cost — *"it had produced no answer after
fifteen minutes"* sitting beside a real 288-second baseline invites the reader to
compute a ratio, and any ratio computed from it is wrong. It now says what it is.

**Left alone:** the thirty-four-minute figure, at both sites. It is already
written as a bound — *"over"*, *"killed rather than waited out"* — and its use is
as the point at which a run was abandoned, which is precisely what a stopped run
establishes. **A lower bound quoted for what a lower bound licenses is not the
defect**; the defect is a lower bound quoted as a measurement.

**The distinction the sweep turns on**, stated because it is the reusable part: a
stopped run is not a bad measurement, it is a measurement of a different quantity.
It measures *how long somebody was willing to wait*, which is a real and useful
fact — it is the upper anchor of the guard's cost criterion — and it is not the
same quantity as *how long the thing takes*. The error was substituting one for
the other, not recording either.

---

## What this sweep does not cover

**Durations in the delta stream** rather than in the repository. The deltas are
not in this tree and are not scanned.

**Figures in `ROUND_STATE.md`'s superseded sections.** They are dated records of
what was believed on their date, and a dated measurement is not rewritten to carry
a later result — the same rule that left `INSTALL.md`'s environment rows alone
when the digest was retired.

**Anything not currently quoted.** The population is figures in force now, not
every duration ever written down.
