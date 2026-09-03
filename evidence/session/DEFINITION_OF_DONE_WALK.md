# The definition-of-done walk — a literal transcript

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures.

**The sentence under test** (DELTA R199 §3, extended R200 §0):

> A stranger with their own pandas pipeline can install the package, run one
> command against it, and get a list of findings naming the columns involved —
> without reading the source, with any configuration they got wrong reported as
> an error rather than as a silence, and with anything not checked reported as
> not checked, distinct from checked and clean.

**The measurement is the count of steps that required reading source, guessing a
name, or opening a file the documentation did not send me to.** The transcript is
the evidence. Friction is recorded, not judged.

**THIS IS A CHEAP APPROXIMATION AND SAYS SO.** I wrote the tool. I cannot be a
stranger, and every guess I made was an informed one. The count below is
therefore a **lower bound**: a real stranger hits at least these and probably
more. The author's second-machine install remains the only version of this test
run by someone the code was not written in front of.

---

## Result: NOT MET. Four steps required guessing or would require reading source.

Under R208's DECISION 3, that list is the remaining work, and it is short and
specific. It is at the bottom of this file.

---

## The environment

```
python -m venv dod_env
dod_env/Scripts/python.exe -c "import sys; print(sys.version)"
  3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025) [MSC v.1943 64 bit (AMD64)]
dod_env/Scripts/python.exe -m pip list
  pip 25.0.1
```

Clean: pip and nothing else.

## Step 1 — README.md

The conventional entry point, opened without being sent there. It states the
command name (`leakaudit`), that the API is unstable before 1.0, an `## Install`
section, and a pointer to `INSTALL.md`. **No friction.**

## Step 2 — install

Documented at `README.md` § Install, verbatim:

```
python -m pip install .
```

Result: `Successfully installed leakaudit-0.1.0.dev0 numpy-2.5.2 pandas-3.0.5
pyarrow-25.0.1 python-dateutil-2.9.0.post0 six-1.17.0 tzdata-2026.3`, exit 0.

**Worth recording: the floors resolved ABOVE the development machine.** The
declared floors are `numpy>=1.26`, `pandas>=2.1`, `pyarrow>=14`; the dev machine
runs 2.4.2 / 3.0.1 / 23.0.1; this environment resolved 2.5.2 / 3.0.5 / 25.0.1 and
the package built and ran. That is one more datum on the untested-ceiling
question and it is not a substitute for the untested floors. **No friction.**

## Step 3 — `leakaudit --help`

The README names the command; `--help` is the standard next move. Prints the
three subcommands with one-line descriptions. **No friction.**

## Step 4 — `leakaudit run --help` and `leakaudit check --help`

Both self-sufficient. `run --help` explains that `--model` switches the run
between the availability probe and the column dependency probe, and points at
`leakaudit schema` for the format. **No friction.**

## Step 5 — `leakaudit schema`

Prints a worked example, a per-key reference, which keys correspond to registered
vocabulary and which do not, and the statement that a frame not named in
`aggregate_frames` is not perturbed and its silence is `none`. **No friction.**

## Step 6 — write a pipeline that is not the fixture

A warehouse picking line. `stations.csv`, 600 rows, one decision row per second
stamped 300 ms **inside** its second. `scans.csv`, 1,764 rows, several scans per
second at random moments within it. The build floors both to the second,
aggregates the scans, and joins them onto the station rows — so a row deciding at
`08:00:00.300` is fed a count over the whole of `08:00:00`, including scans that
had not happened yet. An ordinary, deliberate overhang leak.

> ### FRICTION 1 — the build function's signature is not stated
> `--pipeline module:function` says the function takes "the frames and returns
> the built output". Whether "the frames" is a dict keyed by the `--frame` names,
> a list, or keyword arguments is nowhere stated. I guessed a name-keyed dict
> from the shape of `--frame name=path`, and I was right. **A guess that happened
> to land.** A wrong one produces a `TypeError` traceback, not a message.

## Step 7 — `leakaudit run`, no model

```
leakaudit run --pipeline mypipe:build --frame stations=stations.csv --frame scans=scans.csv
  could not import 'mypipe': ModuleNotFoundError: No module named 'mypipe'
  exit 1
```

> ### FRICTION 2 — the module is in the working directory and is not importable
> The console script does not put the working directory on `sys.path`. The error
> says correctly what failed and does not say what to do about it. Nothing in the
> README, `INSTALL.md`, `--help` or `schema` mentions it.
>
> Two recovery attempts, in the order a stranger would try them:
> - `python -m leakaudit run ...` → `No module named leakaudit.__main__;
>   'leakaudit' is a package and cannot be directly executed`. Fails.
> - `PYTHONPATH=. leakaudit run ...` → works.
>
> I reached `PYTHONPATH` from general Python knowledge, not from anything the
> tool said. **This is the first hard stop on the path and it is at the very
> first command.**

With `PYTHONPATH=.` set, the column dependency probe returns **15 findings over 9
features**, each naming the source columns whose perturbation moved it — e.g.
`items_total moved when col:scans.items, col:scans.scanned_at,
col:stations.timestamp was perturbed`. It prints a `DOMAIN:` paragraph saying
what was *not* probed and why, and `CHECKS: 1 of 4 ran, 0 with findings. The 3
that did not run are reported as not-looked rather than counted as clean.`

**The definition of done's "list of findings naming the columns involved" is
delivered here, and so is its not-checked clause.**

## Step 8 — write the model file

Written from `leakaudit schema` alone, following its worked example. The example's
own key for the trades frame is `ts_event`, a raw event stamp, which is exactly
the shape of my `scans: scanned_at`. **No friction.**

## Step 9 — `leakaudit run --model model.json`

**26 findings over 4 features**: `items_per_scan`, `items_total`, `target`,
`weight_total` — the four that read the second-aggregate, and not `queue_depth`,
`belt_speed` or `load_index`, which do not. The seven probed seconds are named
individually. Exit 1.

It also prints `NOT PROBED: stations -- supplied and not described by the model
... Any silence about it is 'none', not 'observed_silence'.`

**The tool found the leak I planted, named the right four columns, and excluded
the three that were clean.**

## Step 10 — `leakaudit check`, without and with the model

Without: three of four checks report `NOT CHECKED`, each naming the key to
declare and each ending *"This is not a clean result; it is the absence of one."*
One runs and reports `observed_silence` over a stated population. With the model:
all four run, each stating its population, two adding a note about what the
result does **not** establish.

**This is the strongest part of the path.** The `none` / `observed_silence`
distinction is delivered plainly, in the tool's own output, without the reader
needing the vocabulary.

Minor, recorded and not judged: with a complete model the tally reads *"The other
0 did not look"*.

## Step 11 — three deliberately wrong configurations

| file | mistake | what the tool did |
|---|---|---|
| `bad_misc.json` | `"version": 9`, plus a misspelled `decision_colunm` | **A clean message.** `` `version` is 9 and this build understands [1, 2, 3]. REFUSED, not read best-effort. Upgrade the tool, or write a model at a version it knows.`` exit 1. |
| `bad_key.json` | key column named `scan_time`; the column is `scanned_at` | **A 12-line Python traceback**, ending `ProbeError: frame 'scans' has no key column 'scan_time'` |
| `bad_frame.json` | frame named `scan`; the frame supplied is `scans` | **A 12-line Python traceback**, ending `ProbeError: no aggregate cells matched the corrupted seconds; the probe would report silence about itself` |

> ### FRICTION 3 — a wrong name arrives as a traceback, not as a message
> All three are errors rather than silences, so that limb of the definition
> holds. But two of three put twelve lines of Python stack — through
> `cli.py` line 211 and `availability.py` line 353 — in front of the one useful
> sentence. **The traceback puts the tool's source paths in front of a reader
> who was promised they would not need them.**

> ### FRICTION 4 — a misspelled frame name reports a symptom, not the cause
> `bad_frame.json` declares `scan`; the supplied frames are `scans` and
> `stations`. The tool says *"no aggregate cells matched the corrupted
> seconds"* — true, and a consequence. It never says *"you declared frame 'scan'
> and the frames supplied are 'scans', 'stations'"*, which is the fact that fixes
> it. The probe already has a note for a declared-and-absent frame; this path
> raises before reaching it.

## Step 12 — what the walk found in the tool

Two defects were found by walking rather than by any test, and both are
corrections of things claimed in earlier commit messages.

**(a) Every note the probe wrote was invisible to every user of the command.**
`AuditResult.explain()` rendered the unprobed frames, the domain and the check
tally, and never rendered `source.notes`. So the flooring report R207 made a halt
of shipping silently — *"key 'scanned_at' of frame 'scans' is not on second
boundaries (0.0567% are); flooring to `floor(scanned_at) + 1s`"* — reached
nobody. Nor did the per-column-modes fallback conflict note, whose R205 commit
message said it appears "in the run's own output". Recorded as **D-V30A-44**,
fixed, and covered by `tests/phase1/test_notes_reach_the_user.py`.

**(b) `leakaudit schema` still stated the superseded formula.** It read *"The
declared availability instant is that key plus the window"* — the exact sentence
corrected in `AvailabilityModel`'s docstring one round earlier, left standing in
the one place a stranger actually reads it, above a worked example whose own key
is a raw event stamp. Corrected, and the behaviour-versus-description check is
widened from the docstring to both statements.

Both were fixed and the walk re-run from the same clean environment: the flooring
report now appears under `ABOUT THIS RUN:`, once, and `NOT PROBED` is stated
once rather than twice.

---

## The remaining work, which is the answer

1. **The working directory is not importable and nothing says so.** First hard
   stop, at the first command. Either put the pipeline module's directory on
   `sys.path`, or catch the import failure and say what to do.
2. **The build function's contract is not stated.** One sentence in
   `run --help`, or a line in `schema`.
3. **`ProbeError` reaches the user as a traceback.** Catch it at the CLI boundary
   and print the message, as the version refusal already does.
4. **A declared frame that matches no supplied frame reports a symptom.** Name
   the declared frames and the supplied ones.

None of the four is in the tool's arithmetic. All four are on the path between a
stranger and the arithmetic, which is what this test was for.

### One more, recorded and not counted

`python -m pip install .` — the command `README.md` gives — leaves `build/` and
`leakaudit.egg-info/` untracked in the tree it was run from, and `.gitignore`
covered neither. **Not counted among the four**, because that is how pip behaves
in every Python project and is not a fact about this tool. Recorded because this
repository's gate reports unattested files, so its own documented install command
dirtied the tree it attests. Both are now ignored.
