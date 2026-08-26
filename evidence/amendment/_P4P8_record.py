#!/usr/bin/env python3
"""DELTA R47 - record P4's and P8's answers durably.

Every substitution asserts match count 1. Nothing is forced.
"""
import pathlib

SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")

p = SCR / "ROUND_STATE.md"
t = p.read_text(encoding="utf-8")

subs = [
 ("| **P4** | \u00a79.2 timeline from artifacts; finding-and-stop if cases postdate the runs | **RUNNING** \u2014 workflow `wz5gj3g04` |",
  "| **P4** | \u00a79.2 timeline from artifacts | **ANSWERED \u2014 ordering HELD by 29.261 s. The set EXISTS; four agents wrongly proved it absent. See \u00a72.6.** |"),
 ("| **P8** | every declared entry has an originating counterpart? | **RUNNING** \u2014 same workflow |",
  "| **P8** | every declared entry has an originating counterpart? | **ANSWERED \u2014 3 of 6.** Pre-fix trio yes (Phase 6); post-fix trio none. See \u00a72.7. |"),
 ("| **P3** | H-34 correction note appended below the entry, never as an edit | **DRAFT HELD** \u2014 one sentence depends on P4 |",
  "| **P3** | H-34 correction note appended below the entry, never as an edit | **UNBLOCKED, NOT YET WRITTEN** \u2014 wording turns on the K6-admission decision |"),
 ("| 3 | criterion 3 never evaluated; \u00a79.2 never ran under its registered form | **WAITS ON P4** |",
  "| 3 | criterion 3 never evaluated; \u00a79.2's comparison surface RAN (14 Aug, uncommitted), fixture surface did not | **REWRITTEN \u2014 my earlier \u201c\u00a79.2 never ran\u201d was WRONG** |"),
]
for old, new in subs:
    assert t.count(old) == 1, "ROUND_STATE match %d for %.55s" % (t.count(old), old)
    t = t.replace(old, new, 1)

NEW = """
### 2.6 THE \u00a79.2 COMPARISON SET EXISTS AND RAN (P4) \u2014 CORRECTION

**I reported at R46/J4c and again at R47 that "\u00a79.2 never ran". That was WRONG.** The set exists at
`.../8b1d67a4-.../scratchpad/killgate/k6/` \u2014 inside the root \u00a70 of this file declares active under
R37. **Four agents proved its absence at `confidence: PROVEN`; every one declared a population that
excluded that directory.** H-L15's shape, four times, in the round convened to check the claim.

**Verified first-hand this round, not taken from the report:**

```
newest case-data file   2026-08-14 18:06:06.640  (excluding cases/_scripts adapters, written 18:19)
first tool output       2026-08-14 18:06:35.901  raw/leak-detect.json
GAP                     29.261 s, cases FIRST
hash chain              112 declared hashes recomputed, 0 mismatches, 0 unresolved
tagged tree             20 paths, ZERO killgate/k6/case paths; "killgate" absent from all git history
K6 verdict              11 tools, 8 cases + 8 clean controls, 88 cells; kill gate does NOT fire
```

| \u00a79.2 clause | status |
|---|---|
| "one per leakage type" | **AUTHORED** \u2014 8 cases + 8 paired clean controls |
| "**before any tool is run**" | **HELD** \u2014 29.261 s, hash-corroborated (Tier 1) |
| "**committed with this protocol**" | **BREACHED, UNCURABLE for `prereg-v30`** \u2014 in no commit; tag tree fixed |
| "Phase 0 runs on the acceptance fixture" | **NOT DONE** \u2014 so **\u00a710.1 criterion 3 stays unevaluated** |

**A conflict inside the locked file.** \u00a79.2 (line 973) requires the case set in the first commit;
\u00a711 item 1 (line 1048) enumerates that commit's contents as a **closed list omitting it**. Both are
inside the signed hash. **They could not both have been satisfied.**

**THREE STATEMENTS IN CURRENT DOCUMENTS ARE FALSE AS WRITTEN**, each written after 14 Aug:
`AVAILABILITY_DECLARATION.md`:1041 and :1586, and `evidence/ceremony/CEREMONY_COMMANDS.md`:28
(which cites the declaration line as its authority). **NOTHING HAS BEEN EDITED.** Wording is the
author's. Drafted at `ceremony/DEVIATIONS_D003_DRAFT.md`. **K6 is currently on NO staging list.**

### 2.7 P8 \u2014 3 OF 6 DECLARED ENTRIES HAVE AN ORIGINATING COUNTERPART

The originating record is **Phase 6**, which no P8 agent had opened:
`.../MBO_2025/results/pc2_all_phases/phase6/second_pc/phase6_main_summary.csv` (dated 10 Apr,
external to the fixture). **Verified first-hand:** ZC / LightGBM / L2 -> **0.9662 / 0.94 / 0.8564**
at 5/10/30 s.

| entry | declared | originating | match |
|---|---|---|---|
| 5s pre | 0.966244 | 0.9662 | **YES** (4.4e-5) |
| 10s pre | 0.939968 | 0.9400 | **YES** (3.2e-5) |
| 30s pre | 0.856419 | 0.8564 | **YES** (1.9e-5) |
| 5s / 10s / 30s **post** | 0.931536 / 0.756504 / 0.679288 | **none** | **NO** |

The post-fix side was **first produced by Phase 7 itself** \u2014 there is no prior experiment to agree
with. So **limb (i)'s re-scoping trigger does NOT fire**: the exception branch governs 3 of 6, not
all 6. Three consequences for the author, recorded at \u00a75(b) of the J3 redraft:

1. The three post-fix entries must be registered **ex ante** as having no originating counterpart,
   with the real ground, or the gate row fails on them for a record-keeping reason.
2. **One open determination flips 3/6 to 0/6:** whether Phase 7's pre-side L2 meta is an
   independent re-derivation of Phase 6's or a transcription. All 32 Phase 6 L2 cells appear in
   Phase 7 byte-identical **including the stochastic `shuffle_mean`** \u2014 equally consistent with a
   seed-deterministic re-run and with a copy. **NOT ESTABLISHED, and decidable.**
3. **Limb (i) names the wrong key.** "The same horizon and side" is one-to-many: (5s, pre) selects
   16 rows across 8 instruments and 2 families, spanning 0.5420-0.9662 \u2014 **42x the \u00b10.010
   tolerance**. The operative key is **(side, instrument = ZC, model = LightGBM, horizon)**.

### 2.8 \u00a7A.1 ITEM 2's MODEL-FAMILY RATIONALE IS NOT SUPPORTED BY ITS OWN SOURCE

\u00a7A.1 item 2 says *"The model family changes: XGBoost -> LightGBM,"* citing
`MASTER_FINDINGS\\preregistration_v4.txt` line 273. **Read first-hand:** that file names **six
architectures**, `1. LightGBM` immediately **above** `2. XGBoost`, with hyperparameters for both.
**LightGBM was in the registered protocol from the start; no family changed.**

**Load-bearing where it appears:** H2's justification (*"the anchor's model family changed"*) and
J3's failure-mode table row 1. Both need re-grounding.

**\u00a7A.1's CORE claim survives and is unaffected** \u2014 no horizon reproduces the registered pair
(0.957 / 0.675) on both sides within \u00b10.010: 5s misses post by 0.2565, 10s misses both, 30s misses
pre by 0.1006. Separations 0.034708 / 0.183464 / 0.177131 against the implied 0.282.
"""

anchor = "\n---\n\n## 3. THE FIVE ESTABLISHED DISCLOSURES (P9)"
assert t.count(anchor) == 1, t.count(anchor)
t = t.replace(anchor, NEW + anchor, 1)
p.write_text(t, encoding="utf-8")
print("ROUND_STATE.md updated: %d lines" % len(t.split("\n")))

# ---------------------------------------------------------------- X4
x = SCR / "ceremony" / "X4_REGENERATION_REQUIREMENTS.md"
tx = x.read_text(encoding="utf-8")

A = "7. **`LICENSE` and `PRACTICES.md` on the staging list.**"
assert tx.count(A) == 1, tx.count(A)
ADD = """

7a. **`killgate/` \u2014 THE \u00a79.2 COMPARISON SET \u2014 IF THE AUTHOR ADMITS IT (R47/P4, D-003).** It is
   currently on **no staging list and in no commit**, and X4 regenerates from current state, so an
   unlisted tree silently does not ship. If admitted: it joins the staging list,
   `evidence/MANIFEST.sha256` gains its files with COUNTS **re-derived**, and the Phase 0 work-item
   row for "Cross-tool comparison per \u00a79.2" flips from **NOT RUN** \u2014 whose current authority is a
   declaration line that is itself false. **\u00a79.2's "committed with this protocol" is breached and
   uncurable for `prereg-v30`; committing it now does not cure that, it records it.**"""
tx = tx.replace(A, A + ADD, 1)

B = "- `HISTORY.md` **H-35, H-36, H-37**; `DEVIATIONS.md` **D-001** and **D-002**."
assert tx.count(B) == 1, tx.count(B)
NEWB = ("- `HISTORY.md` **H-35, H-36, H-37**, plus **H-38** (\u00a710.1 registers no third state \u2014 R47/P10)\n"
        "  and **H-39** (the deferred contaminated-side tightening \u2014 R47/P2), and the **H-34 correction\n"
        "  note** (R47/P3 \u2014 appended below the entry, never as an edit); `DEVIATIONS.md` **D-001**,\n"
        "  **D-002** and **D-003** (the \u00a79.2 comparison set \u2014 R47/P4).")
tx = tx.replace(B, NEWB, 1)
x.write_text(tx, encoding="utf-8")
print("X4_REGENERATION_REQUIREMENTS.md updated: %d lines" % len(tx.split("\n")))
