# STAGED — `HISTORY.md` review-lesson line (Grep-undercount method lesson)

**Item Q2. STAGING ONLY.** Nothing in this file has been applied. `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` was **read only** and is unmodified.

---

## 0. Register determination — this is a review lesson, not an erratum, not a firing

`HISTORY.md` keeps four distinct registers and the file's conventions do separate them. The drafted line belongs in the **third** one.

| Register | Section | What goes in it | Fits? |
|---|---|---|---|
| Ledger notes `H-01`…`H-33` | `## Ledger notes, by ID` (l.11 onward) | **Errata against a specific locked clause.** Every entry is headed `### H-NN — from \`PREREG.md\` §X` / `` — from `DESIGN.md` §X `` and records a defect *in the specification text*, in an italic parenthetical. | **No.** There is no defective clause in `PREREG.md` or `DESIGN.md` here. The undercount was a survey-method error in a Phase 0 verification round, not a spec defect. |
| Version ledger | `## Version ledger (from \`PREREG.md\` §0.4)` (l.181) | What a **numbered version** got wrong. Every bullet opens `- **vNN**`. | **No.** No version is implicated; nothing in the registration changed or was reversed. |
| **Review lessons** | `## Review lessons (from \`DESIGN.md\` §9)` (l.203), list at l.207–217 | **Process/method lessons**, dated, generalizable. Existing members include tool-behaviour lessons — H-L11 (l.215) is about a silent `str.replace` no-match, H-L1 (l.207) about prior-art search being a search task. | **YES.** Same register: a method that silently under-reports, plus the practice now in force. |
| Firings | `## H-B — the firing enumeration` (l.226) and `### H-B addendum` (l.262) | **Stopping-rule firings** under `PREREG.md` §0.2, enumerated per version. The addendum explicitly marks non-firings (l.264: "**Two entries are marked *not a firing*:**" — v19, v23). | **No.** The stopping rule did not fire. Nothing needs a `not a firing` marker because the entry does not enter this section at all. |

**Register verdict: review lesson.** State this explicitly at the ceremony so the entry is not mistaken for a firing when the v30 → v30a firing count is reconciled — the addendum at l.264 already warns that entry-counting and firing-counting diverge, and adding a lesson must not move the count of twenty-one firings / twenty-three entries.

---

## 1. Format exemplars, quoted verbatim with line numbers

From `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md`.

**Section header and list preamble — l.203 and l.205:**

```
203:## Review lessons (from `DESIGN.md` §9)
205:**Review lessons, dated.**
```

**Exemplar A — l.207 (H-L1), the shortest form:**

```
207:1. *(28 Jul 2026)* v3 claimed no existing tool probed at runtime. The claim survived several review rounds and was false; `leak-detect` had been on PyPI for six years. **Models are poor at telling you something already exists.** Prior-art verification is a search task, done by the author, written down.
```

**Exemplar B — l.209 (H-L3), incident-pair form:**

```
209:3. *(29 Jul 2026)* v6 added an environment-matching requirement that would have degraded nearly every real user, to handle a case the determinism guard already covered. v12 then locked an alignment comparator that failed every dtype-promoting strategy by construction. **A safeguard can make the tool worse, and it has happened twice.**
```

**Exemplar C — l.215 (H-L11), the closest structural match — a tool-behaviour lesson with a remediation clause:**

```
215:11. *(1 Aug 2026)* Three of v20's announced fixes were never in the file. They were applied as silent string substitutions that did not match, and spot-checking a few of them passed. **An edit that reports nothing when it fails is indistinguishable from an edit that worked**, and a change log written from intent rather than from the file will confidently describe fixes that do not exist. Every edit now asserts its match count, and the change log is written from a diff of the file.
```

**Exemplar D — l.217 (H-L8), the current last line in the file** (this is the insertion anchor):

```
217:8. *(31 Jul 2026)* §0.2.1 was written to justify stopping the revision loop, and its first draft granted a permission no pre-registration can carry: rewrite any locked rule that a measurement contradicts, transparently, and call it registered. **The section arguing that it is time to stop is exactly where a self-serving rule will appear**, and it took a reviewer to say so. The rewrite splits mechanical facts and locked-procedure parameters, which Phase 1 may resolve, from semantic changes, which need an amended registration tag before the affected detector exists.
```

### Conventions these establish

1. **Shape:** `N. *(D Mon YYYY)* <concrete incident, past tense, named artefacts and numbers> **<one bolded generalizable sentence>** <the practice now in force, or why the class is structurally hard to catch>.`
2. **Date:** italic parenthetical, `D Mon YYYY`, no leading zero (`1 Aug 2026`, l.215–216). One entry carries an audit stamp: `*(31 Jul 2026, audited 1 Aug)*` (l.214).
3. **Exactly one bolded sentence per entry**, carrying the generalizable claim. It sits mid-entry (A, C, D) or leads (l.211, l.216); it is never the incident narrative.
4. **Backticks** for filenames, paths and identifiers (`` `leak-detect` ``, `` `str.replace` ``, `` `DEVIATIONS.md` ``). Section references are bare (`§0.2.1`).
5. **Length:** 48–110 words. Median ≈ 60.
6. **Em dashes** for asides; entries end with a period.
7. **Numbering is an ID, not a position.** Source order of the list is `1, 2, 3, 4, 5, 6, 7, 9, 11, 10, 8` — deliberately not sequential in the file. `DESIGN.md` l.546 names the set "**H-L1** through **H-L11**", so the list number *N* is the ID `H-L`*N*. **The next free ID is 12.**
8. **No entry cites an evidence path.** Provenance for this entry stays in this staging file and in the ceremony record, not in the line.

---

## 2. The drafted line

Insert as list item **12** (= `H-L12`).

```
12. *(12 Aug 2026)* An archive-wide survey for the two aggressor columns reported 37 files; a filesystem walk over the same root found 119. The search tool honours the archive's `.gitignore`, which excludes `/PC2_TRANSFER_v4/scripts/` and `/results/` so that parquet stays out of git — and with them two mirrored code trees, including the archive's only copy of the Phase 7 simulator, where a confirmed aggregation defect was later found. **A survey that inherits a search tool's default exclusions measures the ignore list, not the archive.** Archive-wide counts now come from a filesystem walk that reports how many files it scanned.
```

83 words — inside the observed 48–110 band. One bolded sentence, mid-entry. Backticked paths. Closing clause states the practice now in force, matching Exemplars A and C.

### Variant B — corpus-free, if the author prefers no archive paths in `HISTORY.md`

`HISTORY.md` is otherwise entirely about the specification's own history and names no corpus file. If that is a convention rather than an accident, use:

```
12. *(12 Aug 2026)* An archive-wide survey of the audit corpus reported 37 files; a filesystem walk over the same root found 119. The search tool honours the corpus's own `.gitignore`, written to keep bulk data out of git, which also excluded two mirrored code trees — one of them holding the sole copy of a file a later item found a defect in. **A survey that inherits a search tool's default exclusions measures the ignore list, not the archive.** Archive-wide counts now come from a filesystem walk that reports how many files it scanned.
```

### Variant C — if the author wants the bolded sentence to state the rule rather than the diagnosis

Replace the bolded sentence in either variant with:

```
**An archive-wide survey must walk the filesystem; a default-excluded search answers a different question than the one asked.**
```

Recommendation: **Variant A with the diagnosis-form bold**, because every existing bolded sentence in the list is a diagnosis or a generalization, never an instruction — consistent with l.3's "**Not a normative file.** Nothing here instructs an implementer."

---

## 3. Exact insertion point

| | |
|---|---|
| **File** | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` |
| **Insert** | as a **new line 218**, i.e. immediately **after** current line 217 and **before** the existing blank line 218 |
| **Anchor — the text it follows** | end of l.217: `…from semantic changes, which need an amended registration tag before the affected detector exists.` |
| **Anchor — the text it precedes** | current l.218 (blank), then l.219: `### H-30 — from \`PREREG.md\` §6.6` |
| **Net effect** | file grows 280 → 281 lines; l.218 onward shift down by one |

No other line in `HISTORY.md` changes. The list is appended to, not renumbered — per convention 7, `12` is an ID and the existing out-of-order numbering `…9, 11, 10, 8` is left exactly as it is.

---

## 4. Required companion edit — `DESIGN.md` l.546

Adding a twelfth lesson makes the pair inconsistent unless `DESIGN.md` is updated in the same ceremony. Current text, verbatim:

```
546:**Review lessons are recorded in `HISTORY.md`** (**H-L1** through **H-L11**). They are process history, not implementation guidance, and an implementer needs none of them to build the tool correctly.
```

`H-L11` must become `H-L12`. `DESIGN.md` carries its own SHA-256 in the tag message (verified below), so this is a second hashed file in the ceremony, not a free edit. **Flagging, not drafting** — `DESIGN.md` was outside item Q2's scope.

---

## 5. Why this is staged rather than applied

`HISTORY.md` is hashed in the signed tag message, so any edit outside the amendment ceremony invalidates the v30 registration hash. Verified read-only from `git tag -l -n50 prereg-v30`:

```
f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6  PREREG.md
039240e3c57497cc8eda65fbfcdc3d1120f1d7a12ad0f41b48d71c98ef063428  DESIGN.md
e8cf5bbbc42762838318e2ffc8cf85b6f44ed701c3ee88f8e93a6e734fc43e0d  HISTORY.md
```

The ceremony already opens `HISTORY.md` — `evidence/fixture_spike/f5/v30a_ceremony_CHECKLIST.md` step **A4** (l.76): "[AUTHOR decides] HISTORY.md ledger entry (next H-ID) for the amendment", next free ledger ID being `H-34` (last present is `H-33`, l.257). **This lesson line rides that same open, in a different section of the file** — the lesson list at l.207–217, not the `H-NN` ledger. Two independent additions to one file in one ceremony; the checklist's `git add` line (l.95) already contemplates `HISTORY.md`.

---

## 6. Evidence and verification status

Everything below was reproduced in this session unless marked otherwise.

| Claim | Status | Source |
|---|---|---|
| Filesystem walk found **119** files | **VERIFIED** | `…\fixture_spike\c1\tagger_survey_capture.txt`, header: `files with >=1 mention: 119` (also `total *.py scanned: 460`). Traversal is `for root, dirs, files in os.walk(ARCHIVE):` — `c1\tagger_survey.py` l.60. |
| Default-excluded search found **37** files | **VERIFIED (reproduced this session)** | Grep tool over `C:\Users\ttbea\OneDrive\Desktop\MBO_2025`, glob `*.py`, pattern `aggressor_side\|is_buy_aggressor` → "Found 154 total occurrences across 37 files." All 37 sit under `MBO_2025\scripts\`. |
| `PC2_TRANSFER_v4\scripts\` was missed | **VERIFIED** | Absent from the 37. Targeted search at that subtree returns 6 files / 29 occurrences — present, therefore excluded rather than absent. |
| `results\pc2_all_phases\_scripts\scripts\` was missed | **VERIFIED** | Absent from the 37. Targeted search at `MBO_2025\results` returns 37 files / 128 occurrences. *(Coincidentally also 37 — do not conflate with the root-survey figure.)* |
| **Mechanism** is the archive's own `.gitignore` | **VERIFIED** | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\.gitignore` l.8 `/results/` and l.89 `/PC2_TRANSFER_v4/scripts/`. Its stated purpose (l.1–2, l.85–86) is keeping bulk parquet out of git; excluding the mirrored **code** trees is a side effect. The Grep tool's ripgrep engine honours `.gitignore` by default. |
| Materiality: an excluded tree held a defect-bearing file | **VERIFIED** | `phase7_l2_sim.py` resolves to exactly one path archive-wide — `results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py` (`find` over the archive; corroborated by `c2\aggregation_comparison.md`: "exists at exactly ONE path in the archive"). It is inside the excluded `/results/` tree, and item C2 statically confirmed the aggregation defect in it. The default-excluded search could not have reached it. |
| "the M1 finding" as a cited source | **UNVERIFIED — could not locate** | There is no `m1` subdirectory in the spike tree (`m3`, `m4`, `m5` only) and no M1 finding document under the scratchpad or `evidence/fixture_spike\`. M1 is referenced second-hand in `n2\provenance_notes.md` l.81 and l.283 (its ZC 2025-01 row count of 338,159). The drafted line does not depend on M1; if the author wants M1 cited in the ceremony record, the primary M1 artefact must be located first. |
| Date `12 Aug 2026` | **CONVENTION AMBIGUOUS — author to confirm** | The survey's own stamp is `run_utc: 2026-08-12T00:12:55.741793+00:00`; local file mtimes are `Aug 11 17:11–17:16`, i.e. the same run. Whether the list's existing dates are local or UTC cannot be determined from the file. `12 Aug 2026` is used as the date the lesson is *recorded*; substitute `11 Aug 2026` if the convention is local date-of-work. |

### Ceremony checklist additions proposed

- [ ] Insert the drafted line as new l.218 of `HISTORY.md` (after l.217).
- [ ] Update `DESIGN.md` l.546: `H-L11` → `H-L12`.
- [ ] Confirm the date convention (§6, last row) before insertion.
- [ ] Record in the ceremony note that this is a **review lesson**, not a firing — the firing count stays at twenty-one, the H-B addendum entry count at twenty-three.
- [ ] Re-hash `HISTORY.md` **and** `DESIGN.md` for the v30a tag message.
