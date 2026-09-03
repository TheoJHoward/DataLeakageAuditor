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

> **STATE AS OF PART III: all six are fixed and the fixed path re-walks at zero.**
> The result below is Part I and Part II's measurement and is left standing — it
> is what the unfixed path measured, and Part III's zero is only meaningful
> against it. **A zero walked by the person who wrote the fixes is not evidence
> that a stranger finds none**; see Part III's closing section.

## Result: NOT MET. **Six** steps required guessing or would require reading source.

Part I of this file recorded four. **Part II resumed the walk over the documented
surface Part I had not touched and found two more**, plus one place where Part I
had skipped a file the README explicitly links. The list of six is at the bottom.

That list is the remaining work. **Nothing on it has been fixed.** Two defects
the walk found *in the tool* — separate from the friction list — were fixed after
Part I's walk completed, and are recorded at Step 12.

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

---

# PART II — the walk resumed, and the count is 6, not 4

**DELTA R209 held that the walk was incomplete and two friction points recorded.
Four were recorded, and the core path was complete: nothing was fixed
mid-transcript, and none of the four was fixed at all.** What Part I fixed were
two defects the walk exposed *in the tool* — notes that reached no reader, and a
schema doc stating a superseded formula — neither of which is on the friction
list.

**But the instinct was right in substance and the count was wrong.** Part I
walked the path a stranger takes to a result. It did not walk the documented
surface around that path: a file the README explicitly links, the library entry
point the README advertises, two of the three frame formats the help names, and
every way a user's own pipeline can misbehave. Finishing it found **two more
friction points and one omission in the walk itself**. That is the decay argument
in R209 §0 arriving as a measured fact rather than a caution: the walker who
knows the answers stops looking.

## Step 13 — `INSTALL.md`, which the README sends you to and I did not open

**This is an omission in Part I's walk, recorded as one.** `README.md` § The tool
says *"Install instructions, verified by execution rather than by reading, are in
`INSTALL.md`"*, and Part I went from the README's own `## Install` block straight
to `pip install .` without opening it.

Checked, because it bears on FRICTION 2's count: **`INSTALL.md` does not mention
`PYTHONPATH`, `sys.path`, or the user's own pipeline module.** Its import section
is about the *package's* importability — `protocol/` missing from the first
distribution, the lazy fixture import — not about the caller's module.
**FRICTION 2 stands.** Had it answered the question, that friction point would
have been mine, not the tool's.

## Step 14 — the library entry point

`README.md` advertises `audit()` by name — *"`audit()`'s return type already
has"* changed. Nothing states its signature.

- **Attempt 1**, `audit(frames, build)`, the order the CLI implies: **works**,
  returns `AuditResult`, prints the same 15 findings over 9 features as the CLI.
- **Attempt 2**, `audit(build, frames)`, the other order: `ContractError: raw
  must be a DataFrame or a mapping of name -> DataFrame, got function`. **A clean
  message that names both what was expected and what arrived.**
- `audit.__doc__` is substantial and explains why two arguments is the entry
  point, why `availability=None` does not mean no result, and that the other five
  parameters raise so the refusal can name them.

> ### FRICTION 1, CONFIRMED AND SHARPENED
> `audit.__doc__` documents what **`audit`** receives. Nothing documents what
> **`build`** receives. `inspect.signature(audit)` renders
> `build: 'Callable[[Any], pd.DataFrame]'` — the return type is stated and the
> **argument is `Any`**. So the package annotates the half I did not need and
> leaves `Any` on the half I had to guess. My guess of a name-keyed dict was
> right on both the CLI and library paths, and it was still a guess.

Minor, recorded and not counted: `dir(leakaudit)` returns 50 public names with no
"start here" among them.

## Step 15 — the other two frame formats

`run --help` says `.parquet, .csv or .json`; Part I used only CSV. Both others
were written from the same data and run with the same model.

**All three produce identical output** — 26 findings over the same four features,
the same flooring fraction of 0.0567%, the same 20 rows across 7 seconds.

> ### FRICTION 5 — the JSON orientation is not stated
> `--frame name=x.json` does not say which pandas `orient` is expected. I guessed
> `records` and it worked. A stranger writing `orient="split"` or `"index"` finds
> out by failing.

## Step 16 — the CLI's own error surface, exhaustively

| what | what the tool printed | lines |
|---|---|---|
| no `--frame` at all | `no --frame given; there is nothing to probe` | 1 |
| frame file absent | `nope.csv: no such file (for frame 'stations')` | 1 |
| function name misspelled | `'mypipe' has no attribute 'buld'` | 1 |
| a v2 model given to `run` | `v2_model.json declares no `aggregate_frames`, so there is no availability model to probe with. Declare one, or drop --model and run the column dependency probe, or use `leakaudit check` for the checks that need no model.` | 1 |
| malformed JSON | `broken.json: not valid JSON (Expecting property name … char 59). The model is refused rather than guessed at: a partially-read model probes less than you declared and says nothing about the difference.` | 1 |
| unknown `version` | `REFUSED, not read best-effort. Upgrade the tool, or write a model at a version it knows.` | 1 |

**Six of six are one clean line.** The v2 case names the problem and *three routes
out*; the malformed-JSON case names the error, its character offset, and why
refusing beats guessing. **This is the standard the rest of the surface fails to
meet, and it is set inside this same package.**

`--stride 200 --max-cohorts 2` reduced the probe to 2 seconds and 8 findings, as
documented.

## Step 17 — a user's own pipeline misbehaving

| what | what the tool printed | lines |
|---|---|---|
| `build` raises | 13-line traceback ending `ValueError: my own pipeline is broken, and this is my exception`, naming **the user's own file and line** | 13 |
| `build` returns a `dict` | 20-line traceback ending `AttributeError: 'dict' object has no attribute 'columns'`, inside **`leakaudit/determinism.py` line 65** | 20 |
| `build` returns `None` | 17-line traceback ending `AttributeError: 'NoneType' object has no attribute 'columns'`, inside **`leakaudit/checks.py` line 205** | 17 |

The first is acceptable and is **not counted**: it is the user's own bug, their
own file is named, and a traceback is the right answer.

> ### FRICTION 6 — a build function returning the wrong type crashes inside the tool
> The other two are the tool's contract being violated and reported as an
> internal `AttributeError` in a module the user has never heard of. The
> signature already annotates `Callable[[Any], pd.DataFrame]`, so **the contract
> is written down and never checked.** This is a configuration the user got
> wrong, and it is reported neither as a silence nor as a usable error.

## Step 18 — where the tracebacks actually come from

Sharper than Part I's reading. The CLI's own argument and config handling is
uniformly excellent — six of six one-line messages. Every traceback observed,
across both parts, comes from an exception escaping **inside** `run_probe_a`,
`determinism` or `checks` rather than being caught at the CLI boundary:
`ProbeError` twice in Part I, `AttributeError` twice here.

**It is one missing boundary, not a diffuse quality problem.** That matters for
the fix, and it is why R209 §1 is right that a fix designed from two examples
would fit two examples.

---

# The remaining work — the answer, at six

1. **The `build` contract is not stated, and is annotated `Any`.** Both paths.
2. **The working directory is not importable and nothing says so.** First hard
   stop, first command; `python -m leakaudit` also fails.
3. **`ProbeError` reaches the user as a traceback** — bad key column, bad frame
   name.
4. **A declared frame matching no supplied frame reports a symptom**, never
   naming the declared frames against the supplied ones.
5. **The JSON `orient` for `--frame x.json` is not stated.**
6. **A `build` returning a non-DataFrame crashes inside `determinism` or
   `checks`** — a contract the package annotates and does not check.

**1, 4 and 5 are the class R209 §1 names:** the message says what went wrong and
not what to do next. **3 and 6 are one thing:** no exception boundary between the
probe internals and the CLI. **2 is its own.**

None is in the tool's arithmetic. All six are on the path between a stranger and
the arithmetic, which is what this test was for. **Nothing on this list has been
fixed.** *(Superseded by Part III, which fixes all six. The sentence stands
because a reader of Part II needs to know what was true when it was written.)*

---

# PART III — the six fixed, and the fixed path re-walked

**The diagnosis was the design.** R210 §1: six defects were one architectural gap
plus documentation. Every traceback came from an exception escaping out of
`run_probe_a`, `determinism` or `checks` with nothing between it and the
terminal, while the CLI's own surface was already six-for-six on one clean line.
So the work was *apply the standard this package already sets, at the boundary
where it is missing* — not invent a message convention.

**Each fix's test is the wrong turn that found it.** The transcript is the
acceptance suite: `tests/phase1/test_the_walks_wrong_turns.py`, 12 tests, one per
step a stranger actually took.

## The six, with the wrong turn re-run

### Item 2 — the working directory is not importable

*Wrong turn re-run:* `leakaudit run --pipeline mypipe:build …` from the
directory holding `mypipe.py`, no `PYTHONPATH`.

```
could not import 'mypipe': no module of that name is on the import path.
A file 'mypipe.py' exists in the working directory, which is almost certainly the one you meant.
A console script does not add the working directory to `sys.path`, so a module beside you
is not importable by default. Any one of these fixes it:
  set PYTHONPATH to its directory   PYTHONPATH=<cwd> leakaudit ...
  install your project              python -m pip install -e .
  name it by its package path       --pipeline mypkg.features:build
The module is imported rather than exec'd on purpose: your pipeline is code this command
runs, and running a path would hide which copy it ran.
```

It detects the file sitting there and says so. **Route 1 was then followed
verbatim and worked.** Routes 2 and 3 were not each exercised, and both assume
the user has a project or package — which is why the route that works for a lone
script is listed first.

A module that is *found* and raises is no longer offered a path fix: it gets
*"The module was found and raised while importing, so this is an error inside
your own code rather than a path problem."*

### Item 3 — `ProbeError` as a traceback

*Wrong turn re-run:* key column `scan_time` where the column is `scanned_at`.

```
leakaudit: frame 'scans' has no key column 'scan_time'
```

**One line, was twelve.** The boundary catches `ProbeError`, `ContractError`,
`ModelFileError` and `ModeError` — the errors this package raises *on purpose* —
listed explicitly. A bare `except Exception` would print a bug in this tool as
though the user had made a mistake, which is the mirror image of the defect the
boundary was added to fix, and a test asserts the catch list is not `Exception`.

### Item 4 — a symptom instead of a cause

*Wrong turn re-run:* frame declared `scan`; frames supplied `scans`, `stations`.

```
leakaudit: declared aggregate frame(s) 'scan' were not supplied, so nothing was corrupted
and the probe would report silence about itself. Declared: 'scan'. Supplied: 'scans',
'stations'. Correct the name in the model file, or supply the frame, or drop it from
`aggregate_frames` -- in which case anything downstream of it is `none`, not
`observed_silence`.
```

The remaining case — every declared frame supplied, but no key overlapping any
selected second — now says the mismatch is in the **keys rather than the names**,
so the two are no longer one message.

### Item 6 — the contract checked

*Wrong turns re-run:* a `build` returning a `dict`, and one returning `None`.

```
leakaudit: your build function returned dict; it must return a pandas DataFrame. The probe
compares the built output row by row and column by column, which dict does not support. If
you are building a dict of columns, return `pd.DataFrame(that_dict)`.

leakaudit: your build function returned None. It must RETURN the built frame -- a function
that assigns it and falls off the end returns None, which is the usual cause. Nothing
downstream can be probed without it.
```

Was 20 and 17 lines, inside `determinism.py:65` and `checks.py:205`. The guard
wraps the callable once at the boundary, so no consumer can be forgotten.

**And re-running the wrong turn found a defect the fix had introduced.** The CLI
wrapped and `audit()` wrapped again, so a user's own exception came back with
`contract.py, in checked` in the stack **twice** — two frames of this tool's
plumbing added to a traceback whose entire value is that it points at the user's
file. The guard is now idempotent, with a test. Nothing but re-running the wrong
turn would have shown it.

> ### THE ACCEPTANCE TEST CAUGHT A BUG IN THE FIX IT WAS ACCEPTING
>
> **Written down at the moment it happened, because this reads as luck later
> unless it is.** R210 §2's claim was that every fix already has its test: re-run
> the exact wrong turn that found the friction. That was proposed as a way to
> confirm fixes. On its **first execution**, before anything was committed, it
> caught a defect in the implementation of the very fix it was checking.
>
> The three cases the fix was written to change all returned one clean line. The
> suite was green. The guard's own behaviour was correct in every respect. The
> defect was visible **only in the stack of a case that is supposed to fail** —
> the user's own pipeline raising — and only by reading that stack rather than
> its last line. No test then existing looked there, and no test that asserts on
> a message would ever have looked there.
>
> The general form: **a fix is checked against the cases it changes, and the
> damage lands on a case it was holding constant.** The wrong-turn re-run covers
> the held-constant cases for free, because they are wrong turns too.

### The idempotency fix has its own two positives

Making a guard idempotent means detecting that it is already applied. Both halves
of that were shown rather than assumed, in
`tests/phase1/test_guard_idempotency.py` — and **both were fired against the real
defect** by temporarily reverting the fix.

**Positive 1 — the doubling is actually prevented.** The test counts `checked`
frames in a real traceback rather than asserting object identity, because
identity would pass even if the frames were still there for another reason. With
the idempotency check disabled, it fires with exactly what was observed:

```
AssertionError: 2 `checked` frames in the user's traceback, not 1.
Stack: ['_frames_in_traceback', 'checked', 'checked', '_raising_build']
```

A triple wrap gives three. A control asserts an unwrapped callable shows **zero**
`checked` frames, so counting them measures something. And a fourth test asserts
idempotent does not mean inert: a double-wrapped build returning a dict still
raises.

**Positive 2 — the marker does not suppress a different guard.** The first
marker was `__leakaudit_guarded__` — generic, meaning "some guard is applied".
That is the discarded-parameter defect wearing a decorator: a second guard added
later for a different job would find the flag set, decline to apply, and leave
its own check unperformed with nothing said.

The marker is now keyed on **the job**: `GUARD_BUILD_RETURN = "build_return_type"`,
carried in a set through `guards_applied()`. The two-guard case is **constructed**
rather than argued — a second guard with its own job name is written in the test
file, and four tests assert both apply, in either order, that each stays
idempotent in the other's presence, and that both actually fire. Reverting the
marker to the generic boolean fires all four.

**Which of the two answers R211 §1.2 asked for:** the marker is now *specific
enough that two guards cannot collide*, and the collision case is constructed to
prove it rather than left as a property of the naming.

### Items 1 and 5 — documentation, asserted separately from the check

`run --help` and `check --help` now state the contract: *"called with ONE
argument — a dict keyed by the --frame names, whose values are DataFrames — and
must RETURN the built output as a DataFrame"*, and *"JSON is read with pandas
defaults, so a list of row objects (orient=records) is what works"*.

The annotation moved from `Callable[[Any], pd.DataFrame]` to
`Callable[[Mapping[str, pd.DataFrame] | pd.DataFrame], pd.DataFrame]`.

**These are two items and the annotation closes only one of them.** Python
enforces no annotation; item 1 is what a reader finds, item 6 is what happens
when they get it wrong, and they have separate tests for that reason.

## What must NOT regress, and is tested

A user's own pipeline raising still produces a traceback naming **their** file
and line. That was never friction: it is their bug, and a traceback is the right
answer. The boundary catches only what this package raises deliberately.

## The re-walk: **0 guess or source-reading steps** — and what that does not mean

Re-walked on the fixed path, in the same clean environment: `--help` → pipeline →
first run → follow the message's own route → model file → availability run →
both `check` runs → every wrong configuration. **Nothing required guessing,
reading source, or opening an undocumented file.**

**A zero from me is not a zero.** I now know every answer, so this walk could not
have discovered new friction — that is the decay argument at its limit, not
evidence of its absence. What the zero establishes is that **the six are closed**
and that the fixed path runs end to end. **The author's second-machine install
remains the only walk by someone the code was not written in front of, and this
does not substitute for it.**

## One more, fixed and deliberately not counted among the six

With a complete model the check tally read *"The other 0 did not look"*. Recorded
in Part I as minor and not judged; fixed now to *"Every check had what it needed,
so no result above is a silence standing in for one."* **Reported as outside the
list of six rather than folded into it**, so the list stays the thing that was
measured.

---

# PART IV — CLOSED. The permanent recorded state, 3 September 2026

**This is not pending work. It is the final state of this measurement**, ruled by
the author on 3 September 2026: nobody other than the author will walk this. What
follows is written so that it cannot be quoted without its limit, because the
limit is the half that decides what the result means.

## The definition of done, as stated

> A stranger with their own pandas pipeline can install the package, run one
> command against it, and get a list of findings naming the columns involved —
> without reading the source, with any configuration they got wrong reported as
> an error rather than as a silence, and with anything not checked reported as
> not checked, distinct from checked and clean.

## The measurement

**The re-walk of the fixed path returned ZERO steps requiring source-reading or
guessing.** Clean environment, install from the repository by the README's own
command, a pandas pipeline that is not the fixture, a model file written from
`leakaudit schema` alone, both commands, and every wrong configuration. Every one
of the six frictions the unfixed path produced is closed, each with the wrong
turn that found it re-run as its acceptance test.

## MET — and the clause that travels with it, in the same sentence

**The definition of done is met on the measurement available, and the walker
authored the code and knew every answer, so this establishes that the six
identified frictions are closed and NOT that a newcomer finds none.**

That sentence is the result. Either half quoted alone misrepresents it.

## What was controlled, and what was not

**Uncontrolled: foreknowledge.** The single variable that matters for this
question, and the one this measurement cannot touch. The walker wrote the tool.
Every guess made during Part I was an informed guess, and Part II demonstrated
the cost concretely — a walk that felt complete was missing a third of its own
findings until the documented surface around the path was walked deliberately.

**Controlled separately: environment.** Four dependency sets and three Python
versions, with the suite and a canonical pipeline digest identical across all of
them (MV-6, MV-7). Environment is therefore not a confound in this result; it was
measured, and it is not the variable in question.

## Why it closes here

Two substitutes were available in principle and neither is: no second machine,
and no second person. The author's ruling is that nobody else walks it.

**A written limitation is a limitation. A pending task quietly becomes a claim**
on the day someone stops reading the task list — which is why this is recorded as
the permanent state rather than left open, and why the item is removed from every
open-items list that carried it rather than left in both places saying two
different things.

## What would change it, if anyone ever does walk it

One person who did not watch this being written, following `README.md` from a
clean environment, recording every wrong turn at the moment it is hit rather than
the corrected path. That is the measurement this one approximates. If it is ever
run, its count replaces this one and this section is superseded rather than
edited, with both standing.
