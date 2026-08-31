# QUARANTINE — output of a run under a VOID pre-commitment. NOT READ.

**Do not read the files in this directory when writing an expectation, a
threshold, or a harness.** They are retained as the record that a run occurred
and was halted, and as a comparison artifact **after** a real result is
committed — never before.

## What happened

Commit `b065264` committed a pre-commitment for the §6.2 acceptance run and the
harness it names. Its stated premise was that the criteria are scored from a
finding's `feature` field alone, and that `affected_output_cohort` is an input to
none of them.

**That premise was refuted.** `EvidenceEvent.pair` is
`(feature, affected_output_cohort)`, and every metric in the scoring machinery is
gated by a pair match against the labels. The field the pre-commitment called
inert is load-bearing.

The refutation was established by reading the machinery, not by reading any
output. The run was stopped first and verified second, which is the order that
preserved the pre-commitment property: nothing here was seen, so a pre-commitment
written later is still genuinely pre-result.

## What these files are

The run reached the end of its first side and checkpointed. It was stopped during
the second.

| file | bytes | sha256, recorded before the files were moved |
|---|---|---|
| `acceptance_run.json` | 135,000 | `6d5928bc72fc77b82916100b4323fdd3dc765725fd6fcd12a753f75d3503c2bf` |
| `acceptance_stdout.txt` | 387 | `b0b4d13785a8c0c8e00ec690953d71d16e3cb7caf93ab9694ec42a3845b54354` |
| `acceptance_stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The stderr digest is the empty-file digest, which is what makes "it is empty"
checkable rather than asserted. There is no exit-status file: the run was stopped
externally, so the shell never wrote one.

**The hashes were taken before anything moved the files.** That is what makes
"never read, never altered" a checkable claim instead of a promise. Anyone can
recompute them.

## Why it is kept

Deleting it would take with it the record of what was believed and what was run.
`b065264` is likewise not edited, amended or deleted: a pre-commitment that is
edited stops being one, and one that is deleted removes the evidence of the
premise it froze. It stands as what it is.

## What is void, and what is not

Void: the pre-commitment as a pre-commitment, and any comparison of these numbers
against its expectations.

Not void: that the probe ran, that it completed one side, and that these are its
bytes. Whatever is in this JSON is what the tool emitted on that day under that
code, and it remains true of that code.
