#!/usr/bin/env python3
"""DELTA R48 - Q2 (three false statements), Q4 (model-family claim), Q7 (ex-ante
no-counterpart registration).

R18: ONE declaration copy, at the repo root, edited IN PLACE. Never copied over.
Every substitution asserts match count 1. Nothing is forced.
"""
import pathlib

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
decl = REPO / "AVAILABILITY_DECLARATION.md"
cer = REPO / "evidence" / "ceremony" / "CEREMONY_COMMANDS.md"

t = decl.read_text(encoding="utf-8")
before_lines = len(t.split("\n"))

# ---------------------------------------------------------------- Q2-A: §A.5
OLD_A = "**SATISFIED.** This whole file is a Phase 0 product; no cross-tool comparison has been run."
NEW_A = """**SATISFIED AS TO ORDERING. THE COMPARISON THAT RAN DOES NOT SATISFY \u00a79.2.**

*(Corrected 21 August 2026, R48/Q2. This paragraph previously read: "**SATISFIED.** This whole file
is a Phase 0 product; no cross-tool comparison has been run." The second clause was false when
written. The correction is recorded here rather than by silent replacement.)*

**Line 448's ordering holds.** This whole file is a Phase 0 product, and the reconstruction it
records preceded the cross-tool comparison.

**A cross-tool comparison WAS executed on 14 August 2026** \u2014 eleven tools over eight hand-written
cases and their eight clean paired controls, 88 tool \u00d7 case cells \u2014 with the case set authored,
materialised and hashed **before the first tool ran** (29.261 s, corroborated independently of the
clock by a hash chain: 112 declared case hashes recomputed, 0 mismatches, 0 unresolved).

**It does not satisfy \u00a79.2, and \u00a79.2 remains un-run in its registered form.** \u00a79.2 requires the
comparison set "committed with this protocol"; the set is in no commit, appears nowhere in git
history, and the tagged tree of `prereg-v30` is fixed at 20 paths \u2014 so that clause is **breached and
uncurable for this tag**. **The acceptance-fixture half of \u00a79.2 was not run.** **\u00a710.1 criterion 3
therefore remains unevaluated for every rostered tool**, and the kill-gate verdict rests on
criterion 1. The run is **unverified by any party that did not perform it**; no result of it is
cited load-bearing anywhere in this declaration.

Recorded in full at `DEVIATIONS.md` **D-003**."""
assert t.count(OLD_A) == 1, "Q2-A match %d" % t.count(OLD_A)
t = t.replace(OLD_A, NEW_A, 1)

# ---------------------------------------------------------------- Q2-B: walk summary
OLD_B = "| Reconstruction in Phase 0, before cross-tool | 448 | SATISFIED |"
NEW_B = ("| Reconstruction in Phase 0, before cross-tool | 448 | SATISFIED **as to ordering** \u2014 but see "
         "\u00a7A.5: a cross-tool comparison ran 14 Aug 2026 and does **not** satisfy \u00a79.2 (commitment clause "
         "breached and uncurable; acceptance-fixture half not run; criterion 3 unevaluated). D-003. |")
assert t.count(OLD_B) == 1, "Q2-B match %d" % t.count(OLD_B)
t = t.replace(OLD_B, NEW_B, 1)

# ---------------------------------------------------------------- Q4: §A.1 item 2
OLD_C = """2. **The model family changes: XGBoost \u2192 LightGBM.** The original documented protocol names
   XGBoost (`MASTER_FINDINGS\\preregistration_v4.txt` line 273 "2. XGBoost (gradient boosted
   trees)"; line 284 records its hyperparameters). The declared trio above is LightGBM.
   `f1\\f1_results.csv` carries both families across 128 rows (32 rows each for
   pre/LightGBM, pre/XGBoost, post/LightGBM, post/XGBoost); the declaration names LightGBM and
   states so rather than leaving the family implicit."""
NEW_C = """2. **The registered anchor names no model family; this declaration names one.** *(Corrected 21
   August 2026, R48/Q4. This item previously read "**The model family changes: XGBoost \u2192
   LightGBM**", asserting that the original documented protocol named XGBoost. **That claim is
   false against its own cited source.** `MASTER_FINDINGS\\preregistration_v4.txt` names **six
   fixed architectures**, with line 272 "1. LightGBM (gradient boosted trees)" immediately
   **above** line 273 "2. XGBoost (gradient boosted trees)", and records hyperparameters for
   both. **LightGBM was in the registered protocol from the start. No family changed.** The
   error was a justification citing a source that does not say what was claimed.)* Registered
   `PREREG.md` line 445 states the pair 0.957/0.675 and **names no architecture, horizon or
   instrument**, so the configuration it was computed under is **not recoverable from the
   registered text**. The declared trio above is ZC / LightGBM and says so rather than leaving
   the configuration implicit. `f1\\f1_results.csv` carries both families across 128 rows (32
   rows each for pre/LightGBM, pre/XGBoost, post/LightGBM, post/XGBoost). **This item is a
   disclosure about under-specification in the registered text, not a discrepancy in the
   fixture**; the ground for the amendment is item 1, which does not depend on it."""
assert t.count(OLD_C) == 1, "Q4 match %d" % t.count(OLD_C)
t = t.replace(OLD_C, NEW_C, 1)

# ---------------------------------------------------------------- Q7: ex-ante registration
OLD_D = "The `full` mode clause of line 445 is unaffected and stands."
NEW_D = """4. **REGISTERED EX ANTE \u2014 the post-fix trio has no originating counterpart, and none can
   exist.** *(Registered 21 August 2026, R48/Q7: **before any Phase 1 measurement**, and stated as
   a ground, never as a tolerance discovered after a miss (\u00a77.0).)* The **pre-fix** entries have an
   originating counterpart in **Phase 6** \u2014
   `results\\pc2_all_phases\\phase6\\second_pc\\phase6_main_summary.csv`, keyed
   (`instrument`, `architecture`, `horizon_s`, `tier`), rows ZC / LightGBM / L2: **0.9662 /
   0.9400 / 0.8564** at 5s / 10s / 30s. The declared trio reproduces them to **|\u0394| \u2264 4.4e-5**.
   The **post-fix** entries have **no originating counterpart anywhere in the archive, and none
   can exist**: the universal-lag correction that *defines* the post-fix side was first applied in
   **Phase 7 itself**, so no prior experiment ever measured that side. The absence is a property
   of the experimental record, not of this declaration's diligence. **Where a gate limb compares a
   declared entry against a figure an originating experiment recorded, the three post-fix entries
   take that limb's no-counterpart branch on this registered ground, and on no other.**

**Phase 7 re-derived; it did not transcribe.** *(Determined 21 August 2026, R48/Q5.)* All 32 Phase 6
L2 cells appear in `results\\phase7\\l2_model_meta.csv` byte-identical, **including `shuffle_mean`**.
That is not evidence of copying: `phase7_l2_sim.py` trains its own models, reads no Phase 6 output
(its eight `phase6` references are all to a rerun mode that **writes**), Phase 6 stored **no
prediction files at all** so Phase 7's 64 parquets cannot be copies, and the shuffle mean is
computed over **fixed seeds [42, 123, 456]** via `RandomState(seed).permutation` \u2014 deterministic by
construction, so identity across a seeded re-run is expected. Recomputing AUC from Phase 7's own
`zc_LightGBM_5s_predictions.parquet` gives **0.966244**, matching the declared entry to 2.5e-7.
**Not established:** no Phase 6 script survives on disk, so whether the two runs shared seeds and
parameters \u2014 and hence whether the agreement is deterministic identity or independent convergence
\u2014 cannot be settled from the artifacts.

The `full` mode clause of line 445 is unaffected and stands."""
assert t.count(OLD_D) == 1, "Q7 match %d" % t.count(OLD_D)
t = t.replace(OLD_D, NEW_D, 1)

decl.write_text(t, encoding="utf-8")
print("AVAILABILITY_DECLARATION.md: 4 substitutions, %d -> %d lines"
      % (before_lines, len(t.split("\n"))))

# ---------------------------------------------------------------- Q2-D: ceremony
c = cer.read_text(encoding="utf-8")
OLD_E = ("| **Cross-tool comparison per \u00a79.2** | **NOT RUN** | `AVAILABILITY_DECLARATION.md` \u00a7A.5, "
         "verbatim: \"This whole file is a Phase 0 product; **no cross-tool comparison has been run.**\" |")
NEW_E = ("| **Cross-tool comparison per \u00a79.2** | **RAN 14 Aug 2026, but does NOT satisfy \u00a79.2** | "
         "Executed: 11 tools, 8 hand-written cases + 8 clean paired controls, 88 cells "
         "(`killgate/k6/K6_RESULTS.md`); case set authored before the first run (29.261 s, hash chain "
         "112/112). **Not \u00a79.2-compliant:** the set is in no commit, so \"committed with this protocol\" "
         "is breached and uncurable for `prereg-v30`; the acceptance-fixture half was not run; "
         "**\u00a710.1 criterion 3 remains unevaluated**. Unverified by any party that did not perform it. "
         "`DEVIATIONS.md` D-003. *(Row corrected 21 Aug 2026, R48/Q2 \u2014 it previously read **NOT RUN**, "
         "citing a declaration line that was itself false.)* |")
assert c.count(OLD_E) == 1, "Q2-D match %d" % c.count(OLD_E)
c = c.replace(OLD_E, NEW_E, 1)
cer.write_text(c, encoding="utf-8")
print("evidence/ceremony/CEREMONY_COMMANDS.md: 1 substitution")
