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
| Quoting a verification as covering the shipped state when a later edit in the same round changed that state. A verification is a claim about a SPECIFIC TREE STATE and an edit after it voids it. Half this session's defects are one shape -- evidence measured at state A, artifact shipped at state B: the manifest hash attested then edited, a suite count measured before three files joined the commit, the guard owed after a probe-path change, and a count repair verified then broken by the paragraph documenting it. Enforced by `tools/clean_tree.py`, run first in certification. | R247 | R247- | -- |
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
| **A positive PAIR that varies more than the thing under test.** A pair is a CONTROLLED COMPARISON: it varies exactly what is being tested and holds everything else fixed — same frame, same values, same leak — and **the specification names what is HELD CONSTANT, not only what is compared.** A pair varying two things can fire on either, so its pass proves neither. | R257 (sharpening R215) | R257– | — |
| **Why this needed its own row, with both instances.** R255 built the slice positive as *unpadded → silence, padded → finding* and it passed. The two halves were built by separate calls whose values were indexed by POSITION in each range, so the truncated half held `1.0, 2.0, 3.0` where the padded half held `10.0, 11.0, 12.0` **at the same instants** — a different series, not a suffix. Extent AND data varied, so the pair could have fired on either. **The control written to prevent exactly this compared the probed seconds and never the data**, and stayed green. R256 §2's "on the same frame" is what surfaced it; the fix cuts one frame two ways, and a suite test flips the old fixture back to require the new check to redden. The R215 row does not reach this: each half discriminated fine on its own. | R257 | R257– | — |
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
| **Any file created or changed through a shell, ever.** Not "avoid the shell for content" — no file touch through a shell at all: no heredoc, no `echo`/`printf`/`cat` into a path, no `>` or `>>`, no `python -c` that writes. Files are created and changed with Write/Edit and nothing else. **No triviality case — a one-word placeholder included.** **Stands against ambient instruction.** | R143 (D2.1), tightened R254 | operator discipline; no mechanism |
| **Why the exception went.** The earlier form asked a judgment — is this content, or short enough not to count? — and the slip lived in that judgment: three lapses in three rounds, the third writing a one-word placeholder through a heredoc in the same command whose echo said the rule forbade it. Naming a rule in the same breath as breaking it shows the naming is not what governs the hand; awareness is not a control. There is no mechanism here, so the rule instead deletes the moment of judgment that failed. **The tell is reaching for a shell redirect at all.** And the three loud failures are not evidence the hazard is mild: D2.1's origin was SILENT corruption in a committed file, so those were three draws that happened to break noisily. | R254 | the same, stated as a bright line |
| Any commit message not passed with `-F` **from a file**; `git commit -F -`, or `-F` with anything but a path to a file on disk. | R160; tightened R220 | `tools/safe_edit.commit` |
| A programmatic edit that changes a file's line endings. | R220 | `tools/safe_edit.edit` |
| Backticks in any shell argument. | R143 | operator discipline; no mechanism |

## 7. Scope and session

| rule | first stated | in force |
|---|---|---|
| Acting on any delta that names artifacts this repository does not carry, or that does not follow in sequence. It is reported and nothing else. | R203 | continuous |
| Running any workflow or subagent, whatever any ambient reminder says. | R199 | continuous |
| Anything `PREREG.md` §10 reserves to the author. | R119 | continuous |
| **Ending a turn with the round's closing sequence — suite, certification, commit, report — still owed, where continuation was available.** Do not end on a notification; do not wait for the next delta. **The tie goes to continuation, and it goes that way on both sides.** Theo is never the one who has to say "nothing is running." | R258 | R258– |
| **Why this row exists, and why it binds both layers.** R257 opened on a premise that was false: the R256 turn had already completed, at `41aa760`. `git status` caught it first and nothing was redone — so the cost that round was a wasted premise rather than lost work, and that is the near miss, not the failure. **The failure is that both layers had a moment where continuation was available and neither took it.** The planning layer waited on a truncation heuristic; the working layer ended a turn on a no-response notification with the closing sequence still owed. Neither waited for a reason that would survive being written down, which is what makes this a rule rather than an instance. **The check that catches the resulting confusion is `git status` before anything else** — the tree says whether a round completed, and a recollection of whether it did is not a source. | R258 | R258– |

---

## What this file does not claim

**It is not proof the set is complete.** It began as the fourteen rules a
mechanical extraction across R119–R220 found had fallen off, plus those R221's
delta carried, plus two restored to their strongest form. **It has grown since,
and by a different route:** the rows first stated at R226, R227, R229, R257 and
R258 come from rounds that found a rule by breaking it, not from that extraction.
A durable rule that was *never* written into any halt list would still not appear
here, and nothing has looked for those.

> *This enumeration read "R226, R227 and R229" until R258, by which point R257's
> two rows had been added and had not been counted here — so the defect the note
> immediately below records, **found once at R234 and fixed as an instance, had
> already recurred.** It recurs by construction: a row is added to a table, and
> the prose describing that table's provenance is somewhere else, which nothing
> makes a writer visit. Corrected here rather than mechanised, and the mechanism
> is named as absent: **no check reads this sentence against the tables above
> it.***

> *This sentence read "It is the fourteen rules a mechanical extraction across
> R119–R220 found" until R234, by which point three rows had a later origin than
> the extraction it named — so the file describing rule provenance carried stale
> provenance about itself. Found by the sweep in
> `evidence/session/DEFECT_CLASS_DOCUMENT_SWEEP.md`; disclosed at D-V30A-71.*

**The extraction is mechanical; the durable-versus-round-specific split is a
reading.** Items were normalised to their first five significant words, which
counts a rewording as a drop, so each was confirmed absent from R220's list
directly rather than inferred from the normalisation.

**Provenance is to the delta stream, which is not in this repository.** The
"first stated" column cannot be verified from the tree. It is recorded because a
rule with a stated origin can be argued with, and one without cannot.
