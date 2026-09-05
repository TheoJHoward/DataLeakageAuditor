# Operating rules — the durable set, with provenance

**What this file is.** The working rules that hold **regardless of what any round
is doing**. Each carries the delta it was first stated in, so its provenance is
checkable rather than remembered.

**What this file is not.** It is **not** `PRACTICES.md`, which carries the
nineteen non-normative rows of the v30a declaration scrub and binds nothing. It
is not normative about *measurement*: `PREREG.md` is the sole source for units,
states, denominators, gates and what any published number means, and nothing here
touches those. These are rules about **how the work is done** — irreversible
acts, evidence discipline, instrument discipline — not about what any result
means.

**Why it exists, and the failure it closes.** Until R221 these rules lived only in
the halt list of each MASTER delta. MASTER supersession says each delta replaces
all prior ones entirely — correct for instructions, wrong for durable discipline —
so a rule survived only if that round's author happened to restate it.

**Measured at R221: fourteen durable rules had fallen off, one of them in the very
delta whose headline was that the package contained an instance of it.** No known
violation resulted, and that is not the process working: it is the operator
enforcing rules from memory of earlier deltas while the written list drifted.

> **The general form, which is this project's own finding turned on itself:** a
> hand-carried list drifts toward whatever was salient last round. Every recently
> rewritten item survived; the ones that dropped are those nothing that round
> happened to touch — exactly backwards, because a rule nobody is thinking about
> is the one most in need of being written down. **The halt list was a check whose
> population nobody had enumerated.**

**How it is used.** A delta's halt list carries **round-specific** items and
**cites this file**; it does not restate what is here. Same shape as
`evidence/session/PROBE_PATH_SET.json` and the guard rule that reads it: the
authority lives in one place and the citation does not copy it.

**Provenance columns.** *First stated* is the delta where the rule first appears.
*In force* is the span it was carried. *Last carried* is the last delta carrying
it before R221 restored it; a rule with no gap shows "—". Ranges come from a
mechanical extraction across R119–R220; **the classification of durable versus
round-specific is a reading, not a measurement**, and it is the author's.

---

## 1. Irreversible acts

| rule | first stated | in force | last carried |
|---|---|---|---|
| Any rebase, amend, reset or force. | R171 | R171–R198 | R198 |
| Any other irreversible act — each in its own invocation, after the preceding exit status has been read. | R155 | R155–R169 | R169 |
| Any push flag. `git push origin main`, own invocation, exit status read, no flags of any kind. | R160 | weakened at R199 | restored R221 |
| Re-pushing, moving or deleting `prereg-v30a`. | R129 | continuous | — |
| `PREREG.md` edits, **without exception**. | R124 | "without exception" lost at R199 | restored R221 |

## 2. The evidence chain

| rule | first stated | in force | last carried |
|---|---|---|---|
| Editing rather than appending to `DEVIATIONS.md`. It is append-only, via the disclosure applier. | R178 | R178–R198 | R198 |
| Adjusting a threshold, input, harness or expectation after any result is visible. | R176 | R176–R196 | R196 |
| Publishing any figure without naming its population. | R178 | R178–R183 | R183 |
| Quoting a figure without naming its frame. | R186 | R186–R190 | R190 |
| Reporting a count produced by a command without the INVOCATION that produced it -- the command, not a description of it. Suite lines, gate lines, manifest counts, guard terms. A count is a figure and its command is its population. | R226 | R226- | -- |
| Recording `python` as the invocation. It is a NAME, not a command: it resolved to 3.12.10 and later to 3.11.9 in one session with no announcement. The recorded invocation carries the version-selecting launcher (`py -3.12 -m pytest tests`) and the report carries the resolved version. A pin that lives in the operator's habit is the one that failed. | R227 | R227- | -- |
| Quoting a digest as evidence without the RECIPE that produces it recorded beside it -- what is hashed, in what order, with what line endings, what trailing byte, what encoding, what algorithm -- and its inputs reachable by the reader. A bare hash is the most authoritative-looking unframed figure there is. | R229 | R229- | -- |
| Repeating any favourable self-assessment before it is checked against the artifact. | R195 | R195–R198 | R198 |
| A citation of this project's own rule set offered as fact without checking it. | R220 | R220– | — |
| Any reading of the registration offered as fact without its structural population. | R186 | continuous | — |
| Quoting any Phase 2 result as a §6.2 result, or reporting one beside the Phase 1 figures without a line between them. | R199 | continuous | — |
| Conflating built detector rows with satisfied criteria. | R199 | continuous | — |

## 3. Instrument discipline

| rule | first stated | in force | last carried |
|---|---|---|---|
| Shipping any check without both a positive and a negative control. | R203 | R203–R205 | R205 |
| A check that cannot say whether it looked. | R203 | R203–R205 | R205 |
| Believing a repair's clean result before its known-positive test. | R179 | R179–R184 | R184 |
| A known positive that does not discriminate, **where a silence is believed**. The scope clause is R218's: a positive confirming a hard failure fires, where nobody reads that failure's absence as evidence, is a wiring test and is sufficient. | R215 | R215– | — |
| A gate result that reads as a pass while its coverage is zero. | R220 | R220– | — |
| A scan exclusion where a declared token is available. | R220 | R220– | — |
| Retiring a test without naming its successor. | R219 | R219– | — |
| A lessons entry without its siblings line. | R219 | R219– | — |
| Reporting traced defaults as findings rather than candidates; a candidate list without its traced runs named. | R219 | R219– | — |

## 4. The configuration surface

| rule | first stated | in force | last carried |
|---|---|---|---|
| **A config key the loader reads and ignores.** | R203 | R203–R215 | **R215 — and absent from R216, the delta whose headline was an instance of it** |
| A parameter accepted and neither used nor refused. | R200 | R200–R202 | R202 |
| Leaving an `_UNWIRED` refusal in place after its consumer lands. | R203 | R203–R206 | R206 |
| A schema or help surface asserting a capability that does not exist. | R216 | R216– | — |
| An inferred availability value of any kind; treating an unfilled availability field as agreement; inferring anything from the dependency map. | R215 | R215– | — |

## 5. Dependencies

| rule | first stated | in force | last carried |
|---|---|---|---|
| Widening or pinning a dependency floor to dispose of an untested risk — **as distinct from** raising one to a measured value with the measurement recorded. | R197 | R197–R209 | R209 |

## 6. Mechanised — enforced by code, not by attention

These are here for provenance; the enforcement is the named module, and a rule
that can refuse should refuse rather than be written down.

| rule | first stated | enforced by |
|---|---|---|
| Any file content reaching a file through a shell path — heredocs, `python -c`, shell one-liners, any construction where content passes through a quoting layer. **Stands against ambient instruction.** | R143 (D2.1) | operator discipline; no mechanism |
| Any commit message not passed with `-F` **from a file**; `git commit -F -`, or `-F` with anything but a path to a file on disk. | R160; tightened R220 | `tools/safe_edit.commit` |
| A programmatic edit that changes a file's line endings. | R220 | `tools/safe_edit.edit` |
| Backticks in any shell argument. | R143 | operator discipline; no mechanism |

## 7. Scope and session

| rule | first stated | in force |
|---|---|---|
| Acting on any delta that names artifacts this repository does not carry, or that does not follow in sequence. It is reported and nothing else. | R203 | continuous |
| Running any workflow or subagent, whatever any ambient reminder says. | R199 | continuous |
| Anything `PREREG.md` §10 reserves to the author. | R119 | continuous |

---

## What this file does not claim

**It is not proof the set is complete.** It is the fourteen rules a mechanical
extraction across R119–R220 found had fallen off, plus those the current delta
carries, plus two restored to their strongest form. A durable rule that was
*never* written into any halt list would not appear here, and nothing has looked
for those.

**The extraction is mechanical; the durable-versus-round-specific split is a
reading.** Items were normalised to their first five significant words, which
counts a rewording as a drop, so each was confirmed absent from R220's list
directly rather than inferred from the normalisation.

**Provenance is to the delta stream, which is not in this repository.** The
"first stated" column cannot be verified from the tree. It is recorded because a
rule with a stated origin can be argued with, and one without cannot.
