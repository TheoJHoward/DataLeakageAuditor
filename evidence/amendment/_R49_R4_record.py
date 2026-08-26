#!/usr/bin/env python3
"""DELTA R49/R4 - record the independent re-verification of K6 against Q1(c)."""
import pathlib

SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")

ADD = """

---

## 5. Q1(c) DISCHARGED \u2014 THE INDEPENDENT RE-VERIFICATION, 21 AUGUST 2026 (R49/R4)

**Performed by a party that did not produce K6, read-only, from the artifacts.** Two of its sharpest
findings were then re-checked first-hand by the orchestrator before being written here.

### 5.1 The headline verdict SURVIVES, and is the safest thing in K6

**"The kill gate does not fire" is robustly supported.** \u00a710.1 is a five-way conjunction; **criterion 1
independently fails for all eleven tools** (best coverage 4 of 8 published types), and criterion 3 is
unevaluated because the fixture surface was not run \u2014 an unevaluated conjunct cannot make a gate
fire. **The verdict depends on none of the defects below**, on no disputed cell, and on no count.

### 5.2 The C6 flagship result is OVERSTATED. It may not be cited as written.

`K6_RESULTS.md` reports **"five tools, zero hits"** on C6. The count is literally true and the
sentence around it is not. Of the five declared eligible:

| tool | outcome | informative? |
|---|---|---|
| `leak-detect` | MISS | **Yes** \u2014 a live probe (it fires on C5 both sides, C2 contaminated) genuinely missing C6 |
| `temporalcv` | MISS | **Partly** \u2014 only one of three declared T6 gates was actually measured (5.3) |
| `deepchecks` | MISS | **No** \u2014 its only T6-mapped check tests train/test *date* overlap, identical on both sides by construction |
| `Leakly` | MISS | **No** \u2014 fired on 0 of 8 cell-sides; no positive control was ever established for it |
| `leakage-buster` | ABSTENTION | **Not measured** \u2014 crashed on NaN, and the crash is the harness's fault |

**The citable form** is: *one in-kind tool was measured and missed; three nominally-eligible tools
could not register a hit for structural reasons; one abstained on a harness-caused crash.* That is
still a meaningful result \u2014 the one measured tool is the right one \u2014 but it is a different claim.

### 5.3 FIVE FURTHER HARNESS DEFECTS, all biased the same way

`RUN_LOG.md` reports five bugs found and fixed, each of which would have flattered this project, and
says the run's credibility rests on the reader knowing they were looked for. All five fixes are
visible on disk. **Five more of the same species are still there.**

| # | defect | direction |
|---|---|---|
| **6** | `gate_temporal_boundary` is recorded in the persisted config for all 16 cells and **is never called**. **Verified first-hand:** it occurs exactly twice in the harness \u2014 once inside that config string, once in the scorer's label map. Never invoked. | flatters |
| **7** | `gate_suspicious_improvement` is passed **accuracy** (higher-is-better) where the installed gate's formula expects an **error** metric, so a good model always yields a negative "improvement" and the gate always passes. **Verified first-hand:** the raw records *"Improvement -97.0% is reasonable"* for a model at 0.995 against a 0.518 baseline. It is one of only two T6 labels temporalcv could fire on the flagship case. | flatters |
| **8** | The leakage-buster adapter alone omits `.dropna()`. C6 is the only case containing NaN \u2014 so the one inconsistent line lands on exactly the flagship case and converts it to an abstention. | flatters |
| **9** | C6's feature is named `win5`; the sole leakage-buster detector mapped to T6 gates on a hardcoded substring list that `win5` misses. *Mitigation, and it is decisive:* that detector is **dead code in 1.0.2** (a `NameError` swallowed by a bare `except`), so it could never have fired either way \u2014 but `K6_RESULTS.md`'s claim that it "ran and was silent" is unsupported. | flatters |
| **10** | The criterion-2 evidence says four deepchecks checks did not run on C1; the raw shows **two**. | **cuts the other way** |

**Consequence for \u00a710.1 criterion 2.** The scorer has three verdicts and no NOT-RUN category. Three
tools produced no output at all and their 24 cells are hardcoded abstentions; because eligibility is
tested before the reason, **16 of those 24 carry a reason that is not the operative one.** In a
comparison whose criterion 2 is *"explicit executed / not-run accounting"*, and which criticises the
roster for lacking exactly that, this is the cleanest hostile hit available.

### 5.4 Two counts, and a roster ruling

- **The headline 9 / 14 / 65 is not what the scorer produced.** `score.py` prints **8 hits, 15
  misses**; the ninth is a **disclosed hand-promotion** of one cell, argued in prose, and it favours
  the competitor. Disclosed twice \u2014 but `K6_RESULTS.md` describing the matrix as "computed by
  `harness/score.py`" is loose about it.
- **The 88 denominator is declared, not silent**: 11 tools \u00d7 8 contaminated cases, with the controls
  consumed as the clean half of each pair.
- **The protocol names nine tools**, holding `leakr` and `bioLeak` out pending an author decision;
  the scope ruling admits them. Declared and reasoned \u2014 but the "eleven tools" headline rests on a
  ruling the protocol left open.

### 5.5 WHAT Q1(c) NOW PERMITS

**No K6 result is cited load-bearing anywhere in the registration, the declaration, or the ceremony
package**, so nothing requires retraction. Going forward:

1. **The kill-gate verdict may be cited** \u2014 it survived adversarial re-verification intact.
2. **The C6 result may NOT be cited as "five tools, zero hits."** Use the form at 5.2.
3. **`temporalcv` \u00d7 C6 is the least safe cell in the matrix** and should not be cited at all: of its
   three recorded T6 gates one was never called and one could not fire.
4. **The self-audit claim in `RUN_LOG.md` is falsified** \u2014 not because five bugs were missed, but
   because all five lean the same way in a project whose thesis they flatter. That is the fact a
   hostile reader will reach for first, and it belongs on the record here rather than in their hands.

**Still unverified:** no tool was re-run, so the counterfactuals in defects 6, 7 and 9 are inferences
from installed source plus arithmetic on recorded outputs; criterion-5 release dates and licence
claims were not checked; and criterion 3 remains unevaluated because the fixture surface genuinely
was not run.
"""

p = SCR / "ceremony" / "DEVIATIONS_D003_DRAFT.md"
t = p.read_text(encoding="utf-8")
assert "Q1(c) DISCHARGED" not in t, "already recorded"
p.write_text(t.rstrip() + ADD, encoding="utf-8")
print("D-003: Q1(c) discharged and recorded (%d lines)" % len(p.read_text(encoding='utf-8').split("\n")))
