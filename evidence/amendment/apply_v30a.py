#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mechanical applier for the PREREG.md v30a amendment diff.

UNAPPLIED BY DEFAULT. It refuses to touch the live repository: it takes an
explicit --root and asserts that root is NOT the live project directory.

Every hunk is anchor-matched on the full line, and the applier RAISES if an
anchor is absent or matches more than once. Hunk ids match PREREG_v30a_DIFF.md.
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

LIVE = "MBO_2025(4mon)+2026-01"

# --------------------------------------------------------------------------
# ANCHORS - exact full lines as they appear in PREREG.md today (v30, 1099 lines)
# --------------------------------------------------------------------------

A_STATUS = ("**Status:** v30 — supersedes v1–v29. Committed together with "
            "`DESIGN.md` v26 and `HISTORY.md`. **The last version under the "
            "self-imposed cap. Everything after this routes through §0.2.1's "
            "class A/B/C machinery, which is what it was built for.**")

A_REGISTRATION = ("**Registration:** committed unchanged as `PREREG.md` at first "
                  "commit, before any detector code is written. See §11.")

A_AUC = ("- **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 "
         "absolute**. The gate runs in `full` mode.")

A_CONTAM = "- **Contamination availability class** recorded in the manifest."

A_SLICED = ("- **Sliced variant** for CI, from the same padded slicer as "
            "user-facing slice auditing.")

A_CRIT3 = ("3. **No runtime finding of any tier, primary or secondary**, appears "
           "on `fixture_corrected`.")

A_DESCENDANTS = ("Secondary findings on **manifest-listed descendants** of a true "
                 "leaking source remain permitted on `fixture_contaminated`; they "
                 "neither satisfy criterion 1 nor enter criterion 2.")

A_COVERAGE_ROW = ("| **Detector-case coverage** | `passed`, `failed`, "
                  "`not_applicable`, `unsupported`, `could_not_run(reason)`, "
                  "`waived` |")

A_FLOOR = ("   The replacement may be stricter than the floor and may not be "
           "weaker: non-zero proof yield, neither runtime detector waived, "
           "criterion 3's gates in force. Committing it before knowing which "
           "criterion is practically useful is the cost of the ex-ante property "
           "— a criterion chosen because it works after tuning is a criterion "
           "shaped by tuning.")

A_PHASE1 = ("| **1** | Availability model and profiles; **verification of §0.3 "
            "Claims A–C and the §6.10 comparator cases**; fixture harness and "
            "manifest; padded slicer; evaluation generator and conformance suite "
            "frozen; detector protocol; report skeleton; the three controls and "
            "the determinism guard | 2–3 wknds | §10.0 ordering followed; claims "
            "verified or a deviation filed with the measurement; both fixture "
            "AUCs reproduce within ±0.010, full and sliced; **all four "
            "alignment-control cases behave as §6.5 requires**; snapshots hashed |")

A_KILLGATE3 = ("3. Fires on `fixture_contaminated` and is silent on "
               "`fixture_corrected` **under the reconstructed declaration — or, "
               "where the fixture is semantically ambiguous (§6.2), under the "
               "labelled hypothetical declaration**;")

# --------------------------------------------------------------------------
# NEW TEXT
# --------------------------------------------------------------------------

H1a = """**Amendment status:** **v30a — this file is amended.** Six class C changes under §0.2.1, listed in the v30a amendments block below. The v30 text of every amended clause is retained inline, marked superseded; `git show prereg-v30:PREREG.md` recovers the registered text byte-exact."""

H1b = """
---

## v30a amendments (class C under §0.2.1)

**What this block is.** `prereg-v30a` is an **amended registration, not a restart** (§0.2.1, line 95). It carries six class C changes. Each was produced by the element-by-element conformance walk of the acceptance fixture's reconstructed availability declaration against §6.2 — `AVAILABILITY_DECLARATION.md` §A — and each hunk below cites the walk section that justifies it. That file is the reconstructed declaration §6.2 already requires and the carrier of this fixture's evidence. **It is not a normative annex and may not be cited as one.** Measurement semantics live in this file and only in this file (§0.2.1's single-normative-source rule). What lives there is this fixture's *instances*: its identity, its measured ground-truth map, its reference-anchor values, its evidence, its documented-unverifiable assumptions, and the per-column enumeration these rules yield for it.

**The test applied to every sentence below, so the split is checkable rather than asserted:** *would this still be true for a different fixture?* If yes it is a **rule** and it is here. If no it is an **instance** and it is in the declaration.

**How the amendment is written, so nothing is lost.**

1. **The superseded v30 text is retained inline, verbatim, in a block marked `SUPERSEDED BY v30a` and marked NOT operative.** No registered sentence is deleted from this file.
2. **Each amended clause carries an inline supersession marker naming v30a**, and the new normative text sits beside the old.
3. **The registered text is recoverable byte-exact independently of this file: `git show prereg-v30:PREREG.md`.** The retained inline copies are a reading convenience; the signed `prereg-v30` tag is the record.
4. **This amendment inherits §11's integrity chain in full** (§0.2.1, line 97): signed tag, file hashes in the tag message, external timestamp receipt committed, repository publicly reachable at lock.

| # | Clause amended | Class | `AVAILABILITY_DECLARATION.md` §A justification | What it changes |
|---|---|---|---|---|
| 1 | §6.2 — reference AUC anchor | C | §A.1 | Retires the registered anchor pair; an anchor is henceforth **constituted by recomputation** from the fixture's stored per-row predictions, with the ±0.010 interval retained as an upper bound. |
| 2 | §6.2 — contamination availability class | C | §A.3 | Moves the **recording locus** from the manifest to the fixture's availability declaration, which the tag hashes; an evidence artifact may not be the locus of a declaration. |
| 3 | §6.2 — sliced variant for CI | C | §A.4 | Moves the sliced variant **off the Phase 0 acceptance fixture** and re-registers it as a Phase 1 CI obligation with its scoring rule declared ex ante. |
| 4 | §6.2 — criterion 3 | C | §A.8 (working resolution R9) | Replaces "no finding on the corrected side" with **scoring against a declared ground-truth map**; neither side is assumed clean. |
| 5 | §6.2 — criterion 1's denominator, and the scored-set partition rule | C | §A.6, §A.6.0–§A.6.4, §A.10 (working resolution R11) | Adds the rule constituting the denominator — derived from the declared map, three classes, each **enumerated by name**, never a residue or a bare count. Criterion 1's registered text itself stands unchanged. |
| 6 | §10.2 — the word "waived" in the replacement-criterion floor | C | §A.12 | Adds the **missing defining clause** to a floor that used the word without one. Changes no threshold and grants no permission. |

**All six are class C under §0.2.1 line 93** — each changes what a published number means, or what an acceptance criterion requires — **and are carried by this registration under line 95.** None is a `DEVIATIONS.md` entry standing alone.

**What an amendment may not do, restated here because this is the first one.** It may not be weaker than the thing it amends (line 97). It may not convert an unmet element into a satisfied one by re-reading it. Where an element cannot be met as written at the instant the amendment must be committed, it is **amended explicitly, never waived and never left outstanding** — which is what amendment 3 does.
"""

H2 = """- **Reference AUC anchor — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.1). **The anchor is constituted by recomputation, not by transcription.** It is computed from the acceptance fixture's own stored per-row prediction and outcome columns — committed bytes — and is declared in the fixture's availability declaration as an **enumerated set of entries**, one per declared horizon and side, each naming its model family, its row count, and the artifact and rows it was computed from. **Where the fixture is of the re-evaluation class** — the scored artifact carries stored per-row predictions rather than a training procedure — **the recomputation is authoritative over any figure recorded in a prior report**: it is a pure function of bytes already committed, so no rerun, reseeding, or environment change can move it. A lower-precision recorded figure that agrees is a secondary record and is reported as such; one that disagrees is a defect to be resolved before the gate runs, never a competing anchor. **The acceptance interval remains ±0.010 absolute, applied per entry, and may not be widened.** Because the anchor is a pure function of committed bytes, a deviation approaching the interval indicates a defect in the recomputation and is a **stop-and-report, not a pass**. **The gate runs in `full` mode** (carried unchanged from the superseded clause). **A report quoting an anchor entry names its model family and horizon**, and says so explicitly where the family differs from the one the original experiment documented.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode."
  >
  > *Retired because no horizon of the declared fixture reproduces the registered pair, and because the anchor's model family changed — both facts, and the replacement entries themselves, are instances and are recorded in the declaration (§A.1). Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*"""

H3 = """- **Contamination availability class — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.3). **The contamination availability class is recorded in the fixture's reconstructed availability declaration** — the declaration this section already requires — **and that file is hashed in the amended registration's tag message**, so the class is frozen at the tag and moving it afterwards is itself a class C amendment. **The recording locus may not be an evidence artifact.** A manifest is the product of a dated measurement round and records what was measured; writing a declaration into it makes a measurement record carry a decision, and an evidence artifact is never adjusted toward a decision. The class is recorded together with its mechanism, its measured incidence, and its per-column enumeration. **This clause moves the locus of one element and nothing else:** the ground-truth column DAG and the count of independently leaking sources remain manifest content and are satisfied there.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Contamination availability class** recorded in the manifest."
  >
  > *The obligation to record the class is not removed — only its locus moves, and it moves to a file the tag hashes, which binds harder than the manifest did.*"""

H4 = """- **Sliced variant — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.4). **The sliced variant is not part of the Phase 0 acceptance fixture.** It is a **Phase 1 CI obligation, due at the first CI run that exercises the padded slicer and before any user-facing slice auditing is published**, produced by that same padded slicer, with its slice boundaries declared. **Its scoring rule is declared now, ex ante, so it cannot be chosen after a result is seen:** a slice inherits the ground-truth-map cells its rows select and is scored against those cells under criterion 3 as amended — findings the selected cells predict are required, findings they exclude are false positives, cells the map does not cover are unscored. **A slice of a characterized side is never treated as clean, and a slice may not be reported as a pass on the strength of containing only unscored cells.** The obligation is not deletable by a `DEVIATIONS.md` entry or by a decision-log interpretation; dropping it is a further class C amendment. **Why it is amended rather than left outstanding:** the registered clause requires an artifact produced by a component of the tool under development, while §0.2.1 line 95 requires this amendment to be committed before that component exists. An element that cannot be satisfied at the instant it must be committed is amended explicitly — leaving it outstanding invites it to be quietly re-read as satisfied later, which is the failure mode §2.7 exists to stop.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing."
  >
  > *The variant is moved and re-registered, not deleted: slice auditing is not dropped and the slicer is not exempt from CI.*"""

H5 = """3. **Runtime findings on both fixture sides are scored against the fixture's DECLARED GROUND-TRUTH MAP — v30a, operative** (supersedes the registered criterion 3 quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.8, working resolution R9). The map is declared in the fixture's availability declaration and **frozen before any detector runs**. It is stated **per side, per declared violation class, and per declared map cell** — the cell key is the unit the declaration declares the fixture to be partitioned into, and the declaration names it. Three dispositions, mutually exclusive and exhaustive over the map:
   - **A finding the map predicts is REQUIRED.** Its absence is a miss.
   - **A finding the map excludes is a FALSE POSITIVE.** It fails the gate — on either side, at any tier, primary or secondary.
   - **A cell the map does not cover is UNSCORED.** It requires no finding and forbids none, enters no denominator, contributes to no rate, and **is never reported as a pass.**

   **Neither side is assumed clean.** The corrected side of a fixture is **CHARACTERIZED, never clean**, and no report may describe it as clean. This is the tool's own coverage principle — silence and belief never convert into a pass (§2.7, §8.1) — applied to the tool's own exam. **The amendment does not lower the bar:** a finding on a cell the map marks zero is still a false positive and still fails the gate, and the unscored disposition is not an escape hatch — unscored cells are named as unscored, never as clean, and they license no pass.
   > **SUPERSEDED BY v30a — registered v30 criterion 3, retained verbatim, NOT operative:** "3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`."
   >
   > *Retired because measurement falsified its premise: the corrected side of the declared fixture carries real, strictly-post-decision violations, so the registered criterion would fail the gate on a correctly-behaving detector reporting a violation the fixture really contains. The measured incidence is an instance and is recorded in the declaration.*"""

H6 = """
**The criterion-1 denominator, and the partition rule that constitutes it — v30a** (`AVAILABILITY_DECLARATION.md` §A.6, §A.6.0–§A.6.4 and §A.10; working resolution R11). **Criterion 1 above stands exactly as registered.** What follows states how its denominator is constituted, which the registered text left to be inferred.

**The denominator derives from the declared ground-truth map, not from a manifest's construction classes.** A manifest's leak-source classification says how a column was *built*; criterion 1 asks what the map *declares violating* on the scored side under the declared `ties` branch (§2.3). Those are different questions and they do not in general have the same answer. **The count of independently leaking sources is manifest content and provenance context; it carries no gate arithmetic and is not N.** Any report quoting a leaking-source count names the scope it counts under.

**Every column of the fixture's declared scored set is placed in exactly one of three classes.** The classes are mutually exclusive and exhaustive over that set:

| Class | What it is | What a finding on it means |
|---|---|---|
| **REQUIRED** | the map declares a violation on it, on the scored side, under the declared branch | at least one **primary** runtime finding attributed to it is required; absence is a miss |
| **OUT OF JURISDICTION** | declared availability-legal at the boundary instant under the declared branch | an availability-class finding on it is a **false positive** |
| **UNSCORED** | scoring on it is declared impossible | counts **neither for nor against** any criterion; reported as an unscored observation |

**N is the length of the REQUIRED list.** Three constraints on how the partition is published, and they are the point of the rule:

1. **Each class is published as an enumerated list of column names.** A class stated as a bare count is not auditable and does not satisfy this.
2. **No class is defined as a residue.** "Everything else" is not a class definition; each column's membership is derived by the rule below and shown.
3. **The partition check is printed and reproducible by any gate report:** the three class sizes sum to the size of the declared scored set, no column appears in two classes, and no column of the set is missing from all three. A report that cannot reproduce the check has not scored the fixture.

**Reporting, per class, and never folded together** (§8.6): the descriptive proof count of this section is published as **k of N REQUIRED columns**, naming N; **false positives are reported against the OUT OF JURISDICTION class and no other** — that class alone bears the false-positive consequence; and findings on UNSCORED columns are reported as unscored observations, which are **not** false positives.

> **THE PARTITION RULE.** A column's class is **derived, not assigned**. Given the fixture declaration's decision instant, `ties` branch, and join keys:
>
> - **REQUIRED** iff its construction carries a **join whose window completes strictly after the decision instant of the row the aggregate is attached to** — the availability-violating join the declaration names — **and** it is **not degenerate-constant** on the fixture.
> - **OUT OF JURISDICTION** iff its construction reads **only values whose availability times are legal at the boundary instant under the declared `ties` branch** (§2.3) — that is, it carries no such join, and every constituent read is legal at its own timestamp.
> - **UNSCORED** iff it is **degenerate-constant** on the fixture, **or** its gate status is declared **EXCLUDED** because its construction is not verifiable from the fixture's own code.

Three reading rules fix the rule's edges. Each closes a hole measurement actually found, and each is part of the rule rather than a gloss on it:

- **Precedence: UNSCORED wins.** A column satisfying an UNSCORED limb and another class's clause is UNSCORED. (The REQUIRED clause is a conjunction, so a degenerate-constant column is already outside it without appeal to precedence; precedence is load-bearing for a column that is fully availability-legal *and* declared EXCLUDED.)
- **"Reads only same-row values" is read as "reads only within-lattice values", not literally one row.** A lagged read of the same column at another timestamp of the same lattice carries no cross-source join, and each constituent read is legal at its own timestamp; such a column is OUT OF JURISDICTION.
- **"Not constructible" means gate status EXCLUDED on the artifact the gate actually scores** — never "not reconstructible in some other rebuild of the fixture". Reading a rebuild's unconstructibles as gate-unscored silently drops columns out of the arithmetic in both directions.

**A column carries one gate class and one only** — §0.2.1's rule that no field answers two questions, applied to gate classes. Where a column has two grounds, one violating and one legal, **the gate class follows the violating ground**; the legal ground is recorded as a fact and not applied; and **a finding on the legal ground does not satisfy the REQUIRED entry.** Naming the right column on the wrong ground does not satisfy criterion 1.

**Re-derivation is mandatory, and moving a column is an amendment.** If a column's construction changes, or a column declared EXCLUDED becomes constructible, its class is re-derived by this rule. **Moving a column between classes, or changing N, after the tag is a class C amendment.** The declaration's enumeration is the current output of this rule and is never a substitute for it.
"""

H7 = """
   **"Waived", defined — v30a** (`AVAILABILITY_DECLARATION.md` §A.12). The floor above uses the word without a defining clause, and the word appears once more as a detector-case coverage state in §7.7's table, also undefined. An undefined term inside a floor whose purpose is to stop criteria being dropped silently is exactly the term that gets read permissively later. **This adds the defining clause. It changes no threshold, exempts nothing, and grants no permission.** The two runtime detectors the floor governs are **L2a and L3.1**.

   > A runtime detector is **WAIVED** with respect to a criterion when the criterion is written, configured, or reported in any way that makes the detector's own result incapable of changing the criterion's outcome. Concretely, a detector is waived if any of the following holds: **(i)** it is excluded from the criterion's denominator; **(ii)** it is in the denominator but its findings are not required to be non-empty for a pass, so its contribution is optional; **(iii)** the criterion can be satisfied by the other detector's output alone; **(iv)** its threshold is set at a level it meets without executing, or by construction; or **(v)** its cases are reported under §7.7's `waived` coverage state rather than executed to a terminal result.

   **What invoking it requires: nothing, because it may not be invoked.** The floor is a **prohibition, not a permission with conditions**. There is no procedure by which either runtime detector may be waived in a replacement criterion. A replacement criterion that waives one is weaker than the floor and is out of specification on its face; it does not become admissible by being recorded, disclosed, justified, or approved. Changing that requires amending the floor itself — a further class C amendment, committed and timestamped before the affected detector is implemented or evaluated (§0.2.1).

   **What this definition does NOT permit — stated so it cannot be read as a general escape:**

   1. **It is not an escape hatch of any kind.** It creates no exception, no justified waiver, no reviewer-approved waiver, no time-limited waiver. It exists only to make a prohibition checkable.
   2. **It does not reach any other criterion.** It defines the word for this floor and for §7.7's coverage state. It says nothing about §6.2's acceptance criteria and may not be cited to soften them.
   3. **"Experimental" is not "waived", and may not become it.** Criterion 3 below can ship a detector or mode marked experimental and exclude it from `assert_no_proven_leakage()`. That changes how findings are *labelled and asserted on*; it does not remove the detector from a replacement criterion's denominator. A criterion that drops a detector *because* it was marked experimental has waived it.
   4. **"No data" is not "waived".** A cell with no data is **unscored**: ledgered by name, entering no denominator, contributing to no rate, and never reported as a pass. The detector is still scored wherever data exists. Converting an unscored cell into a pass is the failure the amended §6.2 criterion 3 names; doing it at the level of a whole detector is a waiver.
   5. **A working resolution or a `DEVIATIONS.md` entry cannot do it.** The clause above forbids a `DEVIATIONS.md`-only criterion outright, and an interpretation of locked text may resolve only toward the stronger reading.
   6. **Per-combination waiving is still waiving.** Criterion 3 below applies its gates per combination; dropping a detector from one combination's criterion while scoring it in another waives it for that combination, and is class C.
   7. **It licenses nothing after tuning.** The whole floor exists ex ante — as the floor's own closing sentence says, a criterion chosen because it works after tuning is a criterion shaped by tuning.
"""

H8 = """
**`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it appears, including this table. **The conditions under which a detector-case may be reported in this state are not defined by this registration**; defining them is a class C change, and until it is made no case may be reported as `waived` on the strength of the state merely existing in this table.
"""

C1 = ("| **1** | Availability model and profiles; **verification of §0.3 Claims "
      "A–C and the §6.10 comparator cases**; fixture harness and manifest; "
      "padded slicer; evaluation generator and conformance suite frozen; "
      "detector protocol; report skeleton; the three controls and the "
      "determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified "
      "or a deviation filed with the measurement; **every declared "
      "reference-anchor entry reproduces within ±0.010 absolute by recomputation "
      "from the fixture's stored predictions (§6.2 as amended by v30a); the "
      "sliced variant is due under §6.2's amended Phase 1 CI obligation, not "
      "here**; **all four alignment-control cases behave as §6.5 requires**; "
      "snapshots hashed |")

C2 = ("3. Fires on `fixture_contaminated` and, on `fixture_corrected`, reports "
      "findings **consistent with the declared ground-truth map — silent where "
      "the map is silent, firing where the map declares a violation** (§6.2 "
      "criterion 3 as amended by v30a) **under the reconstructed declaration "
      "— or, where the fixture is semantically ambiguous (§6.2), under the "
      "labelled hypothetical declaration**;")

# --------------------------------------------------------------------------

HUNKS = [
    # (id, anchor, mode, payload)
    ("H1a", A_STATUS, "after", H1a),
    ("H1b", A_REGISTRATION, "after", H1b),
    ("H2", A_AUC, "replace", H2),
    ("H3", A_CONTAM, "replace", H3),
    ("H4", A_SLICED, "replace", H4),
    ("H5", A_CRIT3, "replace", H5),
    ("H6", A_DESCENDANTS, "after", H6),
    ("H7", A_FLOOR, "after", H7),
    ("H8", A_COVERAGE_ROW, "after_table", H8),
]

CONSEQUENTIAL = [
    ("C1", A_PHASE1, "replace", C1),
    ("C2", A_KILLGATE3, "replace", C2),
]


def apply(root: Path, include_consequential: bool) -> dict:
    path = root / "PREREG.md"
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    before = len(lines)

    hunks = list(HUNKS) + (list(CONSEQUENTIAL) if include_consequential else [])
    stats = {"replaced": 0, "inserted": 0, "anchor_lines": {}}

    for hid, anchor, mode, payload in hunks:
        idxs = [i for i, ln in enumerate(lines) if ln == anchor]
        if len(idxs) != 1:
            raise SystemExit(f"{hid}: anchor matched {len(idxs)} lines, expected 1")
        i = idxs[0]
        stats["anchor_lines"][hid] = i + 1
        new_lines = payload.split("\n")
        if mode == "replace":
            lines[i:i + 1] = new_lines
            stats["replaced"] += 1
            stats["inserted"] += len(new_lines) - 1
        elif mode == "after":
            lines[i + 1:i + 1] = new_lines
            stats["inserted"] += len(new_lines)
        elif mode == "after_table":
            j = i + 1
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            lines[j:j] = new_lines
            stats["inserted"] += len(new_lines)
        else:
            raise SystemExit(f"{hid}: unknown mode {mode}")

    out = "\n".join(lines)
    path.write_text(out, encoding="utf-8")
    stats["before"] = before
    stats["after"] = len(lines)
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--with-consequential", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if LIVE in str(root):
        raise SystemExit("refusing to run against the live project directory")
    stats = apply(root, args.with_consequential)
    print(stats)
    return 0


if __name__ == "__main__":
    sys.exit(main())
