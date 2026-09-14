"""`leakaudit` — the one command. R201 P3.

WHAT IT DOES. Loads your frames, imports your build function, runs the column
probe, and prints what moved. No availability model is needed for that, which is
why it is the first command: a tool whose first useful result requires a declared
availability model has no first useful result.

    leakaudit run --pipeline mymodule:build --frame raw=data.parquet

WHAT IT REFUSES. Everything it does not consume, by name, with what would consume
it -- the same rule as the library entry point. An argument accepted and then
discarded returns a result that looks clean and is not, and for a leakage tool
that is the one failure that must never ship.

WHAT AN EMPTY RESULT SAYS. Which kind of empty it is. `observed_silence` is
evidence; `none` is the absence of evidence; a frame the model does not describe
is named. The exit status distinguishes them too, because a script reading only
the status is exactly the reader who cannot see the prose.
"""
from __future__ import annotations

import argparse
import importlib
import sys

import pandas as pd
from pathlib import Path

EXIT_OK_SILENT = 0          # probes ran, nothing moved
EXIT_FINDINGS = 1           # something moved
EXIT_NOTHING_PROBED = 3     # `none` -- not evidence of absence
EXIT_USAGE = 2
# R267 §3(d). A subsample was probed and nothing moved in it. NOT the clean
# exit: "nothing moved in the part I looked at" is a different claim from
# "nothing moved", and collapsing them is the `none`-as-`observed_silence`
# mistake one level up. It maps to EXIT_OK_SILENT only when the user has
# DECLARED that partial coverage is acceptable, and the acceptance is printed.
EXIT_INCOMPLETE_SILENT = 4
# R272 §2(e). The run discovered its own stride was wrong: `--confirm` found a
# finding that returns only beside EARLIER cohorts, whose cells are available to
# the row. That is not a usage error and it is not a finding about the pipeline;
# it is a fact about this run's stride, and every silence in the run is `none`.
EXIT_INTERFERENCE = 5

#: The exit precedence, printed in `leakaudit run --help`. R272 §2(e).
EXIT_PRECEDENCE = (
    "exit codes, highest precedence first: 2 refused (a usage error or a probe "
    "refusal) > 5 interference (the run's own stride let one cohort's corruption "
    "into another's window; confirmed findings are still listed, and the run is "
    "to be re-done at the stride the message names) > 1 findings > 3 nothing "
    "probed > 4 incomplete and silent > 0 clean.")


def _expected_errors() -> tuple:
    """The exceptions this package raises ON PURPOSE, as a tuple to catch.

    Imported lazily and listed explicitly rather than caught as `Exception`. A
    bare except at the boundary would swallow genuine bugs in this tool and
    print them as though they were the user's mistake, which is the failure mode
    the boundary exists to prevent the mirror image of.
    """
    from .availability import ProbeError
    from .contract import ContractError
    from .model_file import ModelFileError
    from .modes import ModeError
    return (ProbeError, ContractError, ModelFileError, ModeError)


def _load_callable(spec: str):
    if ":" not in spec:
        raise SystemExit(
            "--pipeline takes module:function, e.g. mypkg.features:build. "
            "Got %r, which names no function." % spec)
    mod_name, func_name = spec.rsplit(":", 1)
    try:
        mod = importlib.import_module(mod_name)
    except ModuleNotFoundError as e:
        # THE FIRST HARD STOP ON THE STRANGER PATH, and it was at the first
        # command. R210 item 2. A console script does not put the working
        # directory on `sys.path`, so a pipeline module sitting right there is
        # not importable, and the old message named the failure without naming
        # the route out. Nothing in README.md, INSTALL.md, --help or schema
        # mentioned it.
        missing = getattr(e, "name", None)
        if missing and missing.split(".")[0] == mod_name.split(".")[0]:
            here = Path.cwd()
            local = here / (mod_name.split(".")[0] + ".py")
            raise SystemExit(
                "could not import %r: no module of that name is on the import "
                "path.%s\n"
                "A console script does not add the working directory to "
                "`sys.path`, so a module beside you is not importable by "
                "default. Any one of these fixes it:\n"
                "  set PYTHONPATH to its directory   PYTHONPATH=%s leakaudit ...\n"
                "  install your project              python -m pip install -e .\n"
                "  name it by its package path       --pipeline mypkg.features:%s\n"
                "The module is imported rather than exec'd on purpose: your "
                "pipeline is code this command runs, and running a path would "
                "hide which copy it ran."
                % (mod_name,
                   ("\nA file %r exists in the working directory, which is "
                    "almost certainly the one you meant." % local.name)
                   if local.is_file() else "",
                   here, func_name))
        raise SystemExit(
            "could not import %r: %s: %s\nThe module was found and failed while "
            "importing, so this is an error inside your own code rather than a "
            "path problem." % (mod_name, type(e).__name__, e))
    except Exception as e:                                  # noqa: BLE001
        raise SystemExit(
            "could not import %r: %s: %s\nThe module was found and raised while "
            "importing, so this is an error inside your own code rather than a "
            "path problem." % (mod_name, type(e).__name__, e))
    fn = getattr(mod, func_name, None)
    if fn is None:
        raise SystemExit("%r has no attribute %r" % (mod_name, func_name))
    if not callable(fn):
        raise SystemExit("%s:%s is not callable" % (mod_name, func_name))
    return fn


def _head_commit() -> str:
    """The commit a draft was generated at, or an honest unknown.

    PROVENANCE, and the unknown is a real state rather than a blank. A draft
    written outside a checkout has no commit, and saying "unknown" is different
    from omitting the field -- one says nobody could tell, the other says nobody
    looked.
    """
    import subprocess
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                           text=True, cwd=str(Path(__file__).resolve().parent),
                           timeout=15)
        return r.stdout.strip() if r.returncode == 0 else "unknown"
    except Exception:                                        # noqa: BLE001
        return "unknown"


def _load_frame(path: Path):
    import pandas as pd
    suffix = path.suffix.lower()
    if suffix in (".parquet", ".pq"):
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in (".json",):
        return pd.read_json(path)
    raise SystemExit(
        "%s: unsupported extension %r. Readable: .parquet, .csv, .json. "
        "A frame this command cannot read is refused rather than skipped -- "
        "skipping it would probe less than you asked and say nothing about it."
        % (path, suffix))


def _parse_frames(pairs) -> dict:
    frames = {}
    for pair in pairs or ():
        if "=" not in pair:
            raise SystemExit(
                "--frame takes name=path, e.g. raw=data.parquet. Got %r." % pair)
        name, path = pair.split("=", 1)
        p = Path(path)
        if not p.exists():
            raise SystemExit("%s: no such file (for frame %r)" % (p, name))
        frames[name] = _load_frame(p)
    if not frames:
        raise SystemExit("no --frame given; there is nothing to probe")
    return frames


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="leakaudit",
        description="Runtime leakage auditing by intervention. "
                    "An empty result always says which kind of empty it is.")
    sub = ap.add_subparsers(dest="command")

    run = sub.add_parser(
        "run", help="probe which source columns your pipeline's output reads",
        epilog=EXIT_PRECEDENCE)
    run.add_argument("--pipeline", required=True, metavar="module:function",
                     help="your build function. It is called with ONE argument "
                          "-- a dict keyed by the --frame names, whose values "
                          "are DataFrames -- and must RETURN the built output "
                          "as a DataFrame")
    run.add_argument("--frame", action="append", metavar="name=path",
                     help="an input frame; repeat for several. .parquet, .csv "
                          "or .json. The name is the key your build function "
                          "receives. JSON is read with pandas defaults, so a "
                          "list of row objects (orient=records) is what works")
    run.add_argument("--model", metavar="path.json",
                     help="an availability model FILE. With it, the run is the "
                          "availability probe: which cells the output read "
                          "before the model says they had arrived. Without it, "
                          "the run is the column dependency probe, which needs "
                          "no model. `leakaudit schema` prints the format")
    # THE SENTINEL, NOT 97, SO BOTH ENTRY POINTS RESOLVE THROUGH ONE RULE.
    # R265 §2. The value is still 97 when the flag is omitted -- the rule lives
    # in `run_probe_a` and applies the floor to it -- but omitting the flag and
    # typing `--stride 97` are now different states, and the run says which it
    # was in. A default duplicated at the boundary is the shape R255 §5 and
    # R238 §1 both closed for other keys.
    run.add_argument("--stride", type=int, default=None, metavar="N",
                     help="probe every Nth second (availability runs only). "
                          "Corrupted seconds are kept far apart so a moved row "
                          "is attributable to exactly one of them. Omitted, the "
                          "shipped default of 97 is used where it clears the "
                          "derived floor, and the floor where it does not; "
                          "either way the run says which. A stride below the "
                          "floor is refused.")
    run.add_argument("--max-cohorts", type=int, default=400, metavar="N",
                     help="cap on probed seconds (availability runs only)")
    run.add_argument("--slice-from", default=None, metavar="TIMESTAMP",
                     help="audit only cohorts at or after this instant. The "
                          "data before it is still read by your pipeline and is "
                          "NOT probed, so --padding is REQUIRED with this "
                          "(DESIGN.md section 5.3)")
    run.add_argument("--padding", default=None, metavar="DURATION",
                     help="how far back your builder reads, e.g. 30D or 1h. "
                          "Required with --slice-from and refused without it. "
                          "This tool cannot derive it: the availability model "
                          "says when a cell became knowable, not how far back "
                          "your build function reaches")
    run.add_argument("--label-cohorts", type=int, default=None, metavar="N",
                     help="L2a cohort budget. L2a rebuilds ONCE PER COHORT, so "
                          "this is the run's cost. Defaults to a number derived "
                          "from a measured build time against a ten-minute "
                          "target, printed with its arithmetic. L3.1 has no "
                          "such budget: its cohorts are near-free and it always "
                          "probes every eligible one")
    run.add_argument("--complete", action="store_true",
                     help="probe EVERY eligible cohort. L3.1 batches, so one "
                          "pass can only probe seconds further apart than the "
                          "builder's measured reach; a complete run is that "
                          "many passes at different offsets, each its own "
                          "rebuild, and L2a probes every eligible cohort at a "
                          "build each. The pass count and its cost are printed "
                          "before the verdict. Named --complete rather than "
                          "DESIGN.md's `full`, because `full` was a MODE that "
                          "also switched reach refinement on, and R267 ruled "
                          "there are no modes")
    run.add_argument("--confirm", action="store_true",
                     help="re-probe every batched finding ALONE -- that "
                          "cohort's cells corrupted and nothing else, one "
                          "rebuild each -- and class it CONFIRMED or BATCHED "
                          "ONLY -- NOT CONFIRMED. A batched pass's stride sits "
                          "one second above a reach that is a lower bound, so a "
                          "finding there may be a neighbour's; alone, it "
                          "cannot be. Nothing is dropped. Needs --model")
    run.add_argument("--confirm-cap", type=int, default=None, metavar="N",
                     help="how many finding cohorts --confirm re-probes; above "
                          "it they are chosen by rank and the rest are printed "
                          "as not re-probed. Each costs a rebuild. Default %d "
                          "(%d s target at ~%.1f s a re-probe, measured on the "
                          "acceptance fixture), a cost choice"
                          % (DEFAULT_CONFIRM_CAP, BUDGET_TARGET_SECONDS,
                             FIXTURE_CONFIRM_SECONDS))
    run.add_argument("--accept-partial-coverage", action="store_true",
                     help="treat an INCOMPLETE-and-silent run as clean. Without "
                          "this, a run that probed a subsample and found "
                          "nothing exits %d rather than 0, because that is a "
                          "silence about the subsample and not about the "
                          "pipeline. The acceptance is printed beside the "
                          "verdict" % EXIT_INCOMPLETE_SILENT)
    run.add_argument("--quiet", action="store_true",
                     help="print the findings only, without the explanation")

    chk = sub.add_parser(
        "check", help="the checks that need no availability model")
    chk.add_argument("--pipeline", required=True, metavar="module:function",
                     help="your build function. Called with ONE argument -- a "
                          "dict keyed by the --frame names -- and must RETURN a "
                          "DataFrame")
    chk.add_argument("--frame", action="append", metavar="name=path",
                     help="an input frame; repeat for several. .parquet, .csv "
                          "or .json. The name is the key your build function "
                          "receives")
    chk.add_argument("--model", metavar="path.json",
                     help="the config file. Without it, every check that needs "
                          "a declared label or split reports that it DID NOT "
                          "LOOK, which is not a clean result")

    dft = sub.add_parser(
        "draft", help="draft a model file from your frames -- structure filled, "
                      "availability left blank for you")
    dft.add_argument("--frame", action="append", metavar="name=path",
                     help="an input frame; repeat for several. .parquet, .csv "
                          "or .json")
    dft.add_argument("--out", metavar="path.json",
                     help="write the draft here instead of printing it. REFUSES "
                          "if the file exists: a hand-written model's "
                          "availability fields are the ones nothing can "
                          "reconstruct, because they were never in your data")

    sub.add_parser("schema", help="print the config file format")
    return ap


def _run_checks(frames, build, model_path):
    """The checks of `leakaudit.checks`, each saying whether it looked."""
    from .checks import render, run_all
    from .model_file import ModelFileError, load_model

    label = train = test = None
    if model_path:
        try:
            config = load_model(model_path)
        except ModelFileError as e:
            raise SystemExit(str(e))
        label, train, test = config.label_column, config.train_idx, config.test_idx

    built = build(dict(frames))
    results = run_all(built, label=label, train_idx=train, test_idx=test)
    print(render(results))
    if any(r.outcome == "finding" for r in results):
        return EXIT_FINDINGS
    if all(not r.looked for r in results):
        return EXIT_NOTHING_PROBED
    return EXIT_OK_SILENT


def _probe_complete(frames, build, model, config, stride, slice_from, padding,
                    max_passes=None):
    """A COMPLETE L3.1 run: every eligible cohort, in passes. R268 §3(d).

    WHY PASSES. L3.1 is cheap per cohort because one rebuild serves a whole
    batch -- and a batch can only hold seconds further apart than the builder's
    reach, or one cohort's corruption contaminates the next one's finding
    region. So one pass probes one second in `stride`, and probing every second
    takes `stride` passes at offsets 0..stride-1, each its own rebuild.

    THE STRIDE COMES FROM THE MEASUREMENT when none is declared: since R272
    §2(c) the largest of the model's floor, the single-second reach in rows plus
    one, and the block reach in rows plus one, in positions. On the acceptance
    fixture that is 61 -- 61 passes, pass one 175.1 s, ~198.7 min predicted
    (R271). SUPERSEDED, 2026-09-14: the R268 figure once given here -- 14 s ->
    stride 15 -> 15 passes, 202.0 s a pass, 54.7 min -- was produced by a reach
    that corrupted one frame of two.

    ONE REACH MEASUREMENT. The first call corrupts nothing -- `max_cohorts=0`
    returns after the baseline, the determinism check and the reach control,
    which is exactly what a stride needs -- and every pass then shares that
    measurement, so the separation refusal still checks each pass against it.

    Returns (combined result, the pass-budget note). The combined result is pass
    0 with every later pass's cohorts appended: `verdict()`, `findings` and
    `liveness` all read the cohort list, so aggregation needs no second
    implementation of any of them.
    """
    from .availability import (DEFAULT_STRIDE, NOT_DECLARED,
                               STRIDE_NOT_DECLARED, run_probe_a, stride_floor)
    import math

    from .reach import COMPLETE_SAMPLES
    import time
    t_start = time.time()
    common = dict(column_modes=config.column_modes or None,
                  bar_duration=config.bar_duration, slice_from=slice_from,
                  padding=NOT_DECLARED if padding is None else padding)
    # k SCALES WITH WHAT IT PROTECTS. R270 §2(a). The stride below is this
    # measurement plus one second, and the passes it schedules are the most
    # expensive thing this tool does -- so a complete run measures at
    # COMPLETE_SAMPLES rather than the default three, and prints the spread.
    probe0 = run_probe_a(frames, build, model, side="user",
                         cohort_stride=(STRIDE_NOT_DECLARED if stride is None
                                        else stride),
                         max_cohorts=0, reach_samples=COMPLETE_SAMPLES,
                         block_samples=COMPLETE_SAMPLES, **common)
    setup_s = time.time() - t_start
    if not probe0.determinism_ok:
        return probe0, ("COMPLETE RUN NOT MADE: the builder is not "
                        "deterministic across two clean builds, so no pass "
                        "could attribute anything.")

    # THE STRIDE IS THE LARGEST MEASURED FLOOR, ROUNDED UP. R271 §2(c)(d).
    # R268-R270 took `int(reach) + 1` from the single-second reach, and on the
    # acceptance fixture that reach had never corrupted the trades frame: 16 s
    # against a 60 s window, 163,143 false findings on a builder with no leak
    # (D-V30A-114). The floor is now the largest of the model's floor, the
    # single-second reach plus one second and the BLOCK reach plus one second,
    # and it is rounded UP -- `int()` also threw away the 0.9997 s that put the
    # R270 stride 0.3 ms above its reach.
    from .availability import ProbeError
    block = probe0.block_reach
    n_secs = probe0.decision_seconds
    per_rebuild = setup_s / float(2 + 2 * COMPLETE_SAMPLES)

    def _unbatched():
        return ("Unbatched instead -- one rebuild per decision second -- would "
                "be %d rebuilds, ~%.1f h at the ~%.0f s a rebuild took during "
                "this run's setup." % (n_secs, n_secs * per_rebuild / 3600.0,
                                       per_rebuild))

    if block is not None and block.all_censored:
        raise ProbeError(
            "COMPLETE RUN REFUSED: the block reach ran to the frame's end at "
            "every one of %d sampled positions -- corrupting the history before "
            "a second moved rows right up to the last one -- so no stride this "
            "frame can hold separates two cohorts, and a batched pass would "
            "report one cohort's corruption as another's finding (D-V30A-114). "
            "%s Run without --complete for a sampled audit." % (block.k, _unbatched()))
    # THE STRIDE, IN POSITIONS. R272 §2(c). A pass probes `seconds[offset::S]`,
    # so S counts positions in the sorted decision seconds. The reach terms are
    # compared in ROWS, the unit a rolling window reads -- a 60-row window
    # across an overnight gap spans hours of clock and still 60 rows -- and the
    # model's floor, a time bound, at one second a position, which never
    # undercounts because decision seconds are at least a second apart.
    from .reach import frames_never_corrupted, measured_rows
    never = frames_never_corrupted(block) if block is not None else ()
    if never:
        raise ProbeError(
            "COMPLETE RUN REFUSED: the block reach corrupted no cell of %s at "
            "any of its %d position(s), so no measurement exists for %s and no "
            "stride can be derived that is known to clear %s window (R272 "
            "section 1(c)). %s"
            % (", ".join(never), block.k,
               "it" if len(never) == 1 else "them",
               "its" if len(never) == 1 else "their", _unbatched()))
    model_floor = stride_floor(model, config.column_modes or None)
    parts = [("the model's floor, %s, at one second a position" % model_floor,
              int(math.ceil(model_floor.total_seconds())))]
    single_rows = measured_rows(probe0.reach)
    if single_rows is not None:
        parts.append(("the single-second reach, %d row(s), plus one"
                      % single_rows, single_rows + 1))
    block_rows = measured_rows(block)
    if block_rows is not None:
        parts.append(("the block reach, %d row(s) (%s), plus one"
                      % (block_rows, block.measured), block_rows + 1))
    governing, floor_S = max(parts, key=lambda p: p[1])
    listed = "; ".join("%s = %d" % (name, val) for name, val in parts)
    if stride is not None:
        S = int(stride)
        if S < floor_S:
            raise ProbeError(
                "COMPLETE RUN REFUSED: the declared stride %d is below the floor "
                "of %d positions, %s. Passes that close report one cohort's "
                "corruption as another's finding. Omit the stride and the floor "
                "is used." % (S, floor_S, governing))
        basis = ("the DECLARED stride %d, clearing the floor of %d positions "
                 "(%s)" % (S, floor_S, listed))
    else:
        S = floor_S
        basis = ("%s, %d positions -- the largest of: %s"
                 % (governing, S, listed))
    if n_secs and S >= n_secs:
        raise ProbeError(
            "COMPLETE RUN REFUSED: a stride of %d over %d decision seconds leaves "
            "a pass one cohort, so the frame cannot hold batched passes at the "
            "floor this builder needs (%s). %s" % (S, n_secs, listed, _unbatched()))

    # THE PREDICTION, PRINTED BEFORE THE WAIT. R269 §0(a). A complete run on the
    # acceptance fixture is most of an hour, and nobody should learn that at
    # minute forty. The plan prints before pass one; after pass one the time
    # left is printed as a MEASURED extrapolation -- that pass's own cost times
    # the passes remaining -- rather than a figure carried from another machine
    # or another builder. Printed straight to the terminal, not held for the
    # notes, because the notes arrive after the wait they would have warned of.
    if probe0.reach is not None:
        print(probe0.reach.spread())
    if block is not None:
        print(block.spread())
    print("COMPLETE RUN PLANNED: %d pass(es) at stride %d, from %s. Setup -- two "
          "clean builds and the reach measurement -- took %.1f s, with %d "
          "single-second samples and %d block positions. The time the passes "
          "will take is printed after the first pass, measured from that pass."
          % (S, S, basis, setup_s, COMPLETE_SAMPLES, COMPLETE_SAMPLES))
    sys.stdout.flush()
    combined = None
    first_pass_s = None
    for offset in range(S):
        # A PASS LIMIT, FOR TIMING ONE PASS. R271 §2(d)(f). The plan, the spreads
        # and the prediction print exactly as a complete run prints them; the
        # result then says, in its own notes, that it is not one.
        if max_passes is not None and offset >= max_passes:
            if combined is not None:
                combined.notes.append(
                    "STOPPED AFTER %d of %d pass(es) (max_passes=%d): this is NOT "
                    "a complete run, and its silence is about the passes that ran."
                    % (offset, S, max_passes))
            break
        t_pass = time.time()
        r = run_probe_a(frames, build, model, side="user", cohort_stride=S,
                        max_cohorts=10 ** 9, cohort_offset=offset,
                        reach=probe0.reach, block_reach=block, **common)
        if combined is None:
            combined = r
            first_pass_s = time.time() - t_pass
            # BOTH NUMBERS. R270 §0(c). R269's line printed only the passes left,
            # and the corrected side's run exceeded it by 325 s: the setup it
            # could not include. "Not a promise" covers drift in later passes;
            # it does not cover leaving out time already spent.
            elapsed = time.time() - t_start
            left = (S - 1) * first_pass_s
            print("COMPLETE RUN: %.1f s elapsed so far (setup and reach %.1f s, "
                  "pass 1 of %d %.1f s); %d pass(es) remaining, ~%.1f min at "
                  "pass one's cost; ~%.1f min in total. Later passes may drift "
                  "from pass one's cost, and that drift is not predicted."
                  % (elapsed, setup_s, S, first_pass_s, S - 1, left / 60.0,
                     (elapsed + left) / 60.0))
            sys.stdout.flush()
            continue
        combined.cohorts.extend(r.cohorts)
        combined.n_cohorts += r.n_cohorts
        combined.cells_perturbed += r.cells_perturbed
        combined.determinism_ok = combined.determinism_ok and r.determinism_ok
        # Each pass names its own head cohorts. The complete run's head is the
        # UNION -- keeping pass 0's alone would let a later pass's head cohort
        # count toward the silence the head rule exists to withhold. R269 §2(b).
        combined.head_seconds = (tuple(combined.head_seconds)
                                 + tuple(r.head_seconds))
        # Nothing a later pass says is dropped. Notes identical to pass 0's are
        # not repeated; the rest carry their pass, so a band row or an
        # attribution note from pass 9 is still on the page.
        for note in r.notes:
            if note not in combined.notes:
                combined.notes.append("[pass %d of %d] %s" % (offset + 1, S, note))

    note = ("COMPLETE RUN (R268 section 3(d)): %d pass(es) at stride %d, offsets "
            "0..%d, each its own rebuild; stride from %s. One reach measurement "
            "shared by every pass. L3.1 PASS BUDGET: %d of %d."
            % (S, S, S - 1, basis, S, S))
    return combined, note


from .coverage import BUDGET_TARGET_SECONDS  # noqa: E402

#: One isolated re-probe on the acceptance fixture, MEASURED: 2,156 s for twenty
#: at R270, the two clean builds included.
FIXTURE_CONFIRM_SECONDS = 107.8
#: How many batched finding cohorts `--confirm` re-probes. R271 §3(c): derived
#: from the same 600 s cost choice as C's L2a default, at the measured cost of a
#: re-probe, and printed with that arithmetic. R270 shipped 20 with no target.
DEFAULT_CONFIRM_CAP = max(1, int(BUDGET_TARGET_SECONDS // FIXTURE_CONFIRM_SECONDS))


def _confirm_findings(frames, build, model, config, result, cap,
                      complete=False):
    """Re-probe batched findings ALONE, split what vanishes, class each.

    R270 §2(b), R271 §3. A batched pass corrupts many seconds in one rebuild,
    so a finding it reports may depend on another cohort's corruption.
    `isolate_cohorts` corrupts one cohort and nothing else: a finding that
    persists there is the cohort's own.

    ISOLATION ALONE CANNOT CLASS WHAT VANISHES. A row at F reading a LATER
    cohort's cells -- unavailable to it, so a real leak -- moves in the batch and
    not alone, exactly as interference does. So each finding that vanishes is
    re-probed twice more, with the batch's later cohorts only and with its
    earlier cohorts only:

      CONFIRMED              -- persisted alone.
      CONFIRMED (lookahead)  -- returns with the later cohorts: a real leak, and
                                the later second is named where the nearest one
                                reproduces it alone.
      INTERFERENCE           -- returns with the earlier cohorts: available
                                cells, not a leak. A fact about the run's stride,
                                so the run's silences are no longer licensed.
      BATCHED ONLY           -- returns with neither.
      NOT RE-PROBED          -- above the cap; neither confirmed nor disconfirmed.

    Nothing is dropped. Above the cap, re-probed cohorts are chosen by rank over
    the findings in time order, `round(i * (n - 1) / (cap - 1))`.

    Returns (lines, summary).
    """
    from .availability import isolate_cohorts, split_isolated
    batched = sorted(result.findings, key=lambda c: c.second)
    n = len(batched)
    summary = {"batched": n, "confirmed": 0, "lookahead": 0, "interference": 0,
               "batched_only": 0, "not_reprobed": 0, "not_split": 0,
               "cap": cap,
               "interference_reason": None}
    if n == 0:
        return (["CONFIRM (R271 section 3): no batched finding to confirm. A "
                 "silence keeps its residual -- a propagation path the reach "
                 "samples did not exercise."], summary)
    if n <= cap:
        ranks = list(range(n))
        how = "all %d batched finding cohort(s), within the cap of %d" % (n, cap)
    else:
        ranks = ([0] if cap == 1 else
                 sorted({int(round(i * (n - 1) / float(cap - 1)))
                         for i in range(cap)}))
        how = ("%d of %d batched finding cohort(s), over the cap of %d, chosen "
               "by rank round(i*(n-1)/(cap-1)) over the findings in time order"
               % (len(ranks), n, cap))
    chosen = [batched[r] for r in ranks]
    cap_text = ("default cap %d (%d s target at ~%.1f s a re-probe, measured on "
                "the acceptance fixture)"
                % (DEFAULT_CONFIRM_CAP, BUDGET_TARGET_SECONDS,
                   FIXTURE_CONFIRM_SECONDS)
                if cap == DEFAULT_CONFIRM_CAP else "declared cap %d" % cap)
    # STAGE ONE: ISOLATION, PREDICTED BEFORE IT RUNS. R271 §3(c), R272 §2(d).
    print("CONFIRM STAGE 1 PLANNED: isolation of %d cohort(s) -- %s -- at "
          "~%.1f s a re-probe measured on the acceptance fixture, ~%.1f min "
          "against the %d s target. %s."
          % (len(chosen), how, FIXTURE_CONFIRM_SECONDS,
             len(chosen) * FIXTURE_CONFIRM_SECONDS / 60.0,
             BUDGET_TARGET_SECONDS, cap_text))
    sys.stdout.flush()
    iso = isolate_cohorts(frames, build, model, [c.second for c in chosen],
                          reach=result.reach, block_reach=result.block_reach,
                          batched={c.second: c for c in batched},
                          column_modes=config.column_modes or None,
                          bar_duration=config.bar_duration)
    # STAGE TWO: THE SPLIT, ON EVERY FINDING THAT VANISHED, UP TO THE SAME CAP,
    # PREDICTED BEFORE IT RUNS AND NEVER SILENTLY SKIPPED. R272 §2(d). A vanished
    # finding left unsplit is the worst outcome -- it could be a lookahead leak
    # isolation removed -- so any above the cap are listed with their count.
    vanished = [r for r in iso if not r.persisted]
    to_split, unsplit = vanished[:cap], vanished[cap:]
    if vanished:
        print("CONFIRM STAGE 2 PLANNED: %d vanished; split %d of them (cap %d) "
              "at two re-probes each, ~%.1f min at ~%.1f s a re-probe%s."
              % (len(vanished), len(to_split), cap,
                 2 * len(to_split) * FIXTURE_CONFIRM_SECONDS / 60.0,
                 FIXTURE_CONFIRM_SECONDS,
                 "" if not unsplit else
                 "; %d above the cap will be NOT RE-PROBED" % len(unsplit)))
        sys.stdout.flush()
        # THE BATCH A FINDING CAME FROM. A default run is one batch; a complete
        # run is passes, and a cohort's batch is the seconds a stride away.
        step = int(result.resolved_stride) if complete else 1
        split_isolated(frames, build, model, to_split,
                       batch=sorted(c.second for c in result.cohorts),
                       batch_step=max(1, step), reach=result.reach,
                       block_reach=result.block_reach,
                       column_modes=config.column_modes or None,
                       bar_duration=config.bar_duration)
    lines = ["CONFIRM (R272 section 2(d)): stage one isolated %s; stage two split "
             "%d of the %d that vanished. %s." % (how, len(to_split),
                                                  len(vanished), cap_text)]
    left_unsplit = {r.second for r in unsplit}
    for r in iso:
        if r.second in left_unsplit:
            continue
        klass = r.klass
        feats = ", ".join(r.batched_features) or "-"
        if klass == "CONFIRMED":
            summary["confirmed"] += 1
            lines.append(
                "  CONFIRMED  %s: a finding with nothing else corrupted -- %d "
                "row(s), feature(s) %s. No other cohort was in its rebuild, so "
                "no stride residual applies to it."
                % (r.second, r.moved, ", ".join(r.features) or "-"))
        elif klass == "CONFIRMED (lookahead)":
            summary["lookahead"] += 1
            named = ("later second %s, unavailable to the row, reproduces it "
                     "alone" % r.named_later if r.named_later is not None else
                     "one or more of the %d later cohort(s) from %s to %s, "
                     "unavailable to the row; the nearest one alone did not "
                     "reproduce it" % (len(r.later_seconds), r.later_seconds[0],
                                       r.later_seconds[-1]))
            lines.append(
                "  CONFIRMED (lookahead)  %s: A REAL LEAK. Not a finding alone, "
                "a finding again with only the batch's LATER cohorts corrupted: "
                "%s. Batched feature(s) %s." % (r.second, named, feats))
        elif klass == "INTERFERENCE":
            summary["interference"] += 1
            lines.append(
                "  INTERFERENCE  %s: not a finding alone, a finding again with "
                "only the batch's %d EARLIER cohort(s) corrupted. Those cells "
                "are available to the row, so this is not a leak: the run's "
                "stride put one cohort's corruption inside another's window. "
                "Batched feature(s) %s." % (r.second, len(r.earlier_seconds), feats))
        else:
            summary["batched_only"] += 1
            lines.append(
                "  BATCHED ONLY -- NOT CONFIRMED  %s: %d finding row(s) batched "
                "(feature(s) %s); alone %s; neither the later nor the earlier "
                "cohorts alone reproduce it. Kept and counted: this shows it "
                "was not this cohort's own, not that the row is clean."
                % (r.second, r.batched_moved, feats, r.verdict))
    summary["not_reprobed"] = n - len(iso)
    summary["not_split"] = len(unsplit)
    if summary["not_reprobed"]:
        lines.append(
            "  NOT RE-PROBED: %d batched finding cohort(s) above the cap stay "
            "batched findings, neither confirmed nor disconfirmed."
            % summary["not_reprobed"])
    if unsplit:
        lines.append(
            "  NOT RE-PROBED (split): %d finding(s) vanished alone and sat above "
            "the split cap of %d, so they were not split -- each stays a batched "
            "finding, neither confirmed nor disconfirmed, and could be a "
            "lookahead leak isolation removed: %s."
            % (len(unsplit), cap, ", ".join(str(r.second) for r in unsplit)))
    lines.append(
        "CONFIRM SUMMARY: %d confirmed, %d confirmed (lookahead), %d "
        "interference, %d batched only, %d not split, %d not re-probed, of %d "
        "batched finding cohort(s)."
        % (summary["confirmed"], summary["lookahead"], summary["interference"],
           summary["batched_only"], summary["not_split"],
           summary["not_reprobed"], n))
    if summary["interference"]:
        reason = ("interference detected at stride %d; block reach %s"
                  % (int(result.resolved_stride),
                     getattr(result.block_reach, "measured", None)))
        summary["interference_reason"] = reason
        lines.append(
            "INTERFERENCE MAKES THIS RUN'S SILENCES UNLICENSED. R271 §3(b). A "
            "silence here claims no cohort's corruption reached another's "
            "window, and at least one did. So every silence in this run is "
            "none(%s), whatever a coverage line or a per-cohort outcome above "
            "says, and the run exits %d, interference (R272 section 2(e)). The "
            "CONFIRMED findings above are real regardless." % (reason,
                                                               EXIT_INTERFERENCE))
    return lines, summary


def _run_availability(frames, build, model_path, stride, max_cohorts,
                      slice_from=None, padding=None, label_cohorts=None,
                      complete=False, confirm=False,
                      confirm_cap=DEFAULT_CONFIRM_CAP):
    """The availability probe, end to end, from a declared model file."""
    from .coverage import DEFAULT_L2A_COHORTS, budget_arithmetic
    label_cohorts = (DEFAULT_L2A_COHORTS if label_cohorts is None
                     else int(label_cohorts))
    from .availability import (NOT_DECLARED, eligible_cohorts, run_probe_a,
                               require_decision_column)
    from .availability_trace import traces_for
    from .findings import AuditResult
    from .model_file import ModelFileError, load_model

    try:
        config = load_model(model_path)
    except ModelFileError as e:
        raise SystemExit(str(e))
    model = config.model
    if not config.has_availability_model:
        raise SystemExit(
            "%s declares no `aggregate_frames`, so there is no availability "
            "model to probe with. Declare one, or drop --model and run the "
            "column dependency probe, or use `leakaudit check` for the checks "
            "that need no model." % model_path)

    # `column_modes` REACHES THE PROBE. R216 §0's sweep found it did not.
    #
    # The key was parsed, validated with four distinct refusals, stored on the
    # config, and documented at length by `leakaudit schema` -- and this call
    # omitted it, so a user declaring per-column modes silently got the
    # whole-frame path. That is not a missing capability: the two paths give
    # DIFFERENT answers, measured at R205 as 25 findings against 0 on the same
    # data, and the per-column one was built to suppress a false positive the
    # coarse path produces. A user declaring modes to correct a false positive
    # kept the false positive, with no error.
    #
    # THE LAST SENTENCE OF THAT PARAGRAPH IS SUSPENDED AT R261, and the
    # measurement it rests on is not. The 25-against-0 was measured; reading the
    # 0 as a false positive correctly suppressed is an INFERENCE, and D-V30A-98
    # showed the per-column bucket geometry can produce a 0 while the registered
    # comparator says finding. So a 0 on that path is not by itself evidence the
    # coarse path was wrong. The reading is not quoted until the pair is
    # re-measured under the repaired attribution rule.
    # `--padding` ABSENT AND `--padding` DECLARED-AS-NOTHING ARE DIFFERENT
    # STATES and argparse merges them into `None`. The sentinel is restored here
    # so the probe's refusal sees the state the user is actually in; passing
    # `None` through would trip the "not a declaration" branch with a message
    # about a value the user never typed.
    # `None` from argparse means the flag was omitted; the sentinel carries that
    # state into the one place the rule lives. R265 §2.
    from .availability import DEFAULT_STRIDE, STRIDE_NOT_DECLARED
    pass_note = None
    if complete:
        # R268 §3(d). Every eligible cohort, in passes. See `_probe_complete`.
        result, pass_note = _probe_complete(frames, build, model, config,
                                            stride, slice_from, padding)
    else:
        stride = STRIDE_NOT_DECLARED if stride is None else stride
        result = run_probe_a(frames, build, model, side="user",
                             cohort_stride=stride, max_cohorts=max_cohorts,
                             column_modes=config.column_modes or None,
                             bar_duration=config.bar_duration,
                             slice_from=slice_from,
                             padding=NOT_DECLARED if padding is None else padding)
    # L2a RUNS ON THIS PATH TOO, AND IT JOINS THE LIBRARY ENTRY AT
    # `run_probe_l2a`. R261 §4. The refusal for a partial or malformed
    # declaration lives in `resolve_label_declaration`, which both entries
    # reach, so there is no second copy of the words here to fall out of step --
    # the shape R255 §5 settled for the slice rule and R238 §1 for the clock.
    from .label_probe import run_probe_l2a
    label_result = run_probe_l2a(
        frames, build, model, side="user",
        raw_label=config.raw_label,
        label_availability=config.label_availability,
        # L2a rebuilds ONCE PER COHORT, so no two cohorts share a batch and the
        # floor has nothing to protect here: its stride is a sampling choice
        # only. An omitted flag takes the same shipped default the availability
        # probe takes, so the two rows probe the same seconds by default.
        # COMPLETE FOR L2a is every eligible cohort at a build each, R268
        # §3(d): stride 1 and no cap. Otherwise the shipped default stride and
        # the budgeted cohort count. `stride` is still None on the complete path,
        # which never resolved it to the sentinel, so both are handled.
        cohort_stride=(1 if complete else
                       DEFAULT_STRIDE if stride in (None, STRIDE_NOT_DECLARED)
                       else stride),
        max_cohorts=(10 ** 9 if complete else label_cohorts))
    # Eligibility is derived, not assumed: a second no aggregate frame carries a
    # row in has nothing to corrupt, and scheduling it would report a dead
    # process where the truth is an empty probe surface.
    built = build(dict(frames))
    # THE THIRD CONSUMER, AND IT HAD NO REFUSAL OF ITS OWN. R238 §1. These two
    # lines read the clock directly and were covered only because `run_probe_a`
    # above calls the shared refusal first -- ordering again, in the one
    # consumer with no membership test beside it. Asking here makes the cover
    # a call rather than a line number.
    dcol = require_decision_column(model.decision_column,
                                   "the CLI's cohort selection")
    # THE SECOND COHORT SELECTION, AND THE SLICE HAS TO REACH IT. R255 §5.
    #
    # This line re-derives the probed seconds instead of taking them from
    # `result`, so it is a second place the cohort set is decided. Left alone
    # under a slice it would hand `eligible_cohorts` the padding seconds, and
    # the eligibility table would list rows the probe never perturbed as probe
    # subjects -- context reported as audited, which is exactly what R255 §3
    # forbids. It does NOT re-decide the slice: the plan comes off the result,
    # already validated by the one refusal in `run_probe_a`, so there is no
    # second threshold here to drift from the first.
    _secs = sorted(pd.to_datetime(built[dcol]).dt.floor("s").unique())
    if result.slice_plan is not None:
        _secs = [s for s in _secs if s >= result.slice_plan.slice_from]
    # THE STRIDE THE PROBE RESOLVED, not the one the caller typed. R265 §2.
    # This line re-derives the probed seconds, so it needs the same stride the
    # probe used; reading the raw argument would resolve the sentinel a second
    # time and the two could disagree the moment the rule changes.
    # A COMPLETE RUN PROBED EVERY SECOND, across its passes. R268 §3(d). Offsets
    # 0..S-1 at stride S cover `_secs` exactly once by construction, and
    # `test_the_OFFSETS_between_them_probe_EVERY_second_EXACTLY_ONCE` pins it,
    # so the set is taken whole rather than re-derived pass by pass.
    if complete:
        picked = list(_secs)
    else:
        picked = _secs[::result.resolved_stride][:max_cohorts]
    elig = eligible_cohorts(frames, model, picked,
                            pd.to_datetime(built[dcol]))

    # THE TWO COVERAGE NUMBERS. R267 §3(c). Reported, never thresholded -- they
    # are the POPULATION of every silence this run prints, which is why they are
    # computed from the same `_secs`/`picked` the probe used rather than from a
    # count carried along beside them.
    # THE DENOMINATOR, WHICH HAS NOW BEEN SET TWICE. R267 made it the
    # separation-eligible set, `_secs[::stride]`, so a default run read as
    # complete over its thirteen probed cohorts. R268 §3 ruled that wrong: at
    # stride 97 a default run probes one second in ninety-seven, its silence is
    # incomplete, and saying so in the exit code is the distinction the class
    # exists to draw. So the denominator is every cohort the DECLARED MODEL makes
    # probe-able, independent of stride and budget, and each decision second is
    # placed in exactly one of three states (see `Coverage`). Eligibility is
    # the same `eligible_cohorts` the table below already uses, run over every
    # second rather than the picked ones.
    from .coverage import Coverage
    _floors = pd.to_datetime(built[dcol]).dt.floor("s")
    _universe = set(_secs)
    _E = set(eligible_cohorts(frames, model, _secs,
                              pd.to_datetime(built[dcol])).eligible)
    # THE HEAD OF THE FRAME LEAVES THE ELIGIBLE SET. R269 §2(b). A second a
    # declared frame carries a row in, whose rows decide within the measured
    # reach of the frame's first row, is not probe-able either: its lookback
    # reads cells before the frame. The cutoff is the probe's own, carried on
    # the result, so the table and the verdict cannot disagree about where the
    # head ends.
    _cutoff = getattr(result, "head_cutoff", None)
    _H = {s for s in _E if _cutoff is not None and s < _cutoff}
    _E = _E - _H
    _P = set(picked) & _E
    _U = _E - _P
    _I = _universe - _E
    _in_universe = _floors.isin(_universe)
    coverage = Coverage(
        cohorts_probed=len(_P),
        cohorts_unprobed=len(_U),
        cohorts_ineligible=len(_I),
        rows_probed=int(_floors.isin(_P).sum()),
        rows_unprobed=int(_floors.isin(_U).sum()),
        rows_ineligible=int((_in_universe & _floors.isin(_I)).sum()),
        context_rows=int((~_in_universe).sum()),
        cohorts_head=len(_H),
        rows_head=int(_floors.isin(_H).sum()),
        # The reason prints when there IS a head, or when the head could not
        # be assessed at all; an assessed head of zero needs no sentence.
        head_reason=(getattr(result, "head_reason", "")
                     if (_cutoff is None or _H) else ""),
        l2a_probed=label_result.n_cohorts,
        l2a_eligible=label_result.n_eligible)
    coverage.verify(len(_universe), len(built))
    traces = traces_for(result, elig.eligible, case_id="user")
    for note in elig.notes:
        result.notes.append(note)
    # R270 §2(b). After the traces, so every batched finding is already in the
    # output and the classes below annotate it rather than replace it.
    if confirm:
        confirm_lines, _summary = _confirm_findings(frames, build, model,
                                                    config, result, confirm_cap,
                                                    complete=complete)
        result.notes.extend(confirm_lines)
        # Read where the exit class is decided. R271 §3(b).
        result.interference_reason = _summary["interference_reason"]

    # A FINDING PRODUCED UNDER DRAFTED STRUCTURE CARRIES THAT FACT. R233 §1(d).
    #
    # There is no "accept the tool's guess" path for AVAILABILITY -- the tool
    # never guesses it, and the loader refuses a draft whose availability fields
    # are still blank. But STRUCTURE can be accepted unread: a user can run
    # `draft`, fill the availability blanks it left, and never look at the
    # `aggregate_frames` it determined. Every finding in this run then rests on a
    # key column a program chose, and that is a condition of the result rather
    # than a detail of how the file was made.
    prov = getattr(config, "draft_provenance", None)
    if prov:
        det = (prov.get("determined_from_data") or {}).get("aggregate_frames")
        result.notes.append(
            "THIS RUN'S STRUCTURE WAS DRAFTED, NOT WRITTEN. The model file "
            "carries `draft_provenance`: %s determined by `%s`%s, and "
            "`structure_edited_by_hand` is %s. Every finding here rests on those "
            "key columns. If a key is wrong, the probe is asking about the wrong "
            "clock and a clean result would mean nothing -- check them against "
            "what your pipeline actually joins on."
            % ("aggregate_frames for %s" % ", ".join(det) if det
               else "structure",
               prov.get("generated_by", "an unrecorded generator"),
               " at commit %s" % prov["commit"] if prov.get("commit") else "",
               prov.get("structure_edited_by_hand")))

    # L2a'S OUTCOME REACHES THE READER, AND IT CARRIES ITS ROW ON EVERY LINE.
    # R260 §3(d), R261 §4. Two runtime rows now produce findings, and `PREREG.md`
    # §6.2's criteria adjudicate "runtime findings" without naming a row -- a
    # registration finding recorded at item 7(v). The tool's own output does not
    # inherit that: every line below says which row it came from, so a reader
    # holding two results never has to infer it.
    result.notes.append(
        "[%s] verdict: %s. %d finding cohort(s) of %d probed."
        % (label_result.detector, label_result.verdict(),
           len(label_result.findings), label_result.n_cohorts))
    for note in label_result.notes:
        result.notes.append("[%s] %s" % (label_result.detector, note))
    # BOTH BUDGETS, PRINTED. R268 §3(d): L3.1's in passes, L2a's in cohorts. A
    # default run says what completeness would cost, so the gap between this
    # run and a complete one is a number on the page rather than an inference.
    if complete:
        result.notes.append(pass_note)
        if label_result.n_eligible > 0:
            result.notes.append(
                "L2a COHORT BUDGET: complete -- every eligible cohort (%d) at a "
                "build each, which is the complete run's own cost."
                % label_result.n_eligible)
    else:
        if result.resolved_stride:
            result.notes.append(
                "L3.1 PASS BUDGET: 1 of %d (default). One pass at stride %d "
                "probes one second in %d, so its silence is about that "
                "subsample. At this stride a complete run would take %d passes; "
                "`--complete` instead uses the smallest stride the measured "
                "reach allows, which is usually far fewer."
                % ((result.resolved_stride,) * 4))
        result.notes.append(budget_arithmetic(label_cohorts))
    result.notes.append(coverage.table())
    out = AuditResult(traces, source=result)
    # Carried on the result so the exit-class decision reads the same numbers
    # the run printed, rather than recomputing them and being free to disagree.
    out.coverage = coverage
    return out


def main(argv=None) -> int:
    """The CLI boundary. THE ONE PLACE A LIBRARY EXCEPTION STOPS.

    R210 §1 is the diagnosis this function was rewritten against: the CLI's own
    argument and config handling was already uniformly one clean line -- six of
    six on the walk -- and every traceback a stranger saw came from an exception
    escaping out of `run_probe_a`, `determinism` or `checks` with nothing
    between it and the terminal. Six friction points, one missing boundary.

    So the errors this package raises DELIBERATELY -- ProbeError, ContractError,
    ModelFileError, ModeError -- are caught here and printed as their message.
    Anything else is left to raise with its traceback intact, because an
    unexpected exception is a bug in this tool and hiding its stack would make
    it unreportable.
    """
    from .contract import audit

    try:
        return _main(argv)
    except _expected_errors() as e:
        print("leakaudit: %s" % e, file=sys.stderr)
        return EXIT_USAGE


def _main(argv=None) -> int:
    from .contract import audit, guarded_build

    ap = build_parser()
    args = ap.parse_args(sys.argv[1:] if argv is None else argv)

    # THE THIRD PATH, WHICH DOES NOT JOIN THE OTHER TWO, AND SO CARRIES ITS OWN.
    # R255 §5. `audit()` -- the column dependency probe, taken when no --model
    # is given -- reaches no `run_probe_a`, so the refusal there cannot cover
    # it. Silently ignoring a slice on that path would leave a user believing
    # they had audited a window when they had audited everything.
    #
    # IT SITS IMMEDIATELY AFTER PARSING, AND THE FIRST PLACEMENT DID NOT. Put
    # after the pipeline was resolved, it never ran: `--pipeline` fails first
    # and the user is told about their import while the flag that would have
    # been ignored goes unmentioned. This is pure argument validation and
    # belongs where nothing can fail ahead of it.
    if getattr(args, "slice_from", None) is not None and not getattr(args, "model", None):
        print("leakaudit: --slice-from needs --model. The slice rule "
              "(DESIGN.md section 5.3) is about window warmup, and without an "
              "availability model there is no window to reason about. Declare a "
              "model, or drop --slice-from and audit the whole frame.",
              file=sys.stderr)
        return EXIT_USAGE
    if getattr(args, "padding", None) is not None and not getattr(args, "model", None):
        print("leakaudit: --padding needs --model and --slice-from. Nothing was "
              "excluded from probing, so the padding describes no boundary.",
              file=sys.stderr)
        return EXIT_USAGE
    # R268 §3(d). `--complete` probes every eligible cohort of the AVAILABILITY
    # probe, in passes. Without --model there is no availability probe to make
    # complete, and ignoring the flag would let a user believe they had run a
    # complete audit when they had run the column dependency probe. Refused on
    # the same terms as the slice flags above.
    if getattr(args, "complete", False) and not getattr(args, "model", None):
        print("leakaudit: --complete needs --model. A complete run probes every "
              "eligible cohort of the availability probe, in passes at "
              "different offsets, and without an availability model there are "
              "no cohorts to complete.", file=sys.stderr)
        return EXIT_USAGE
    # R270 §2(b). `--confirm` re-probes the availability probe's findings, so
    # it needs the model for the same reason `--complete` does; a cap with
    # nothing to cap, or a cap that would re-probe nothing, is a declaration the
    # run could only ignore.
    if getattr(args, "confirm", False) and not getattr(args, "model", None):
        print("leakaudit: --confirm needs --model. It re-probes the availability "
              "probe's findings one cohort at a time, and without an "
              "availability model there are no findings of that probe to "
              "confirm.", file=sys.stderr)
        return EXIT_USAGE
    _cap = getattr(args, "confirm_cap", None)
    if _cap is not None and not getattr(args, "confirm", False):
        print("leakaudit: --confirm-cap without --confirm caps nothing. Add "
              "--confirm, or drop the cap.", file=sys.stderr)
        return EXIT_USAGE
    if _cap is not None and _cap < 1:
        print("leakaudit: --confirm-cap must be at least 1; a cap of %d would "
              "re-probe no finding while the run said it confirmed them."
              % _cap, file=sys.stderr)
        return EXIT_USAGE

    if args.command == "schema":
        from .model_file import SCHEMA_DOC
        print(SCHEMA_DOC)
        return 0
    if args.command == "draft":
        # INFERENCE PROPOSES; IT NEVER PICKS. The draft fills what is a shape in
        # the frames and leaves what is a fact about the world blank, and its
        # header says which is which. It writes no file and runs no probe: what
        # comes out is text for a person to read and complete.
        from .inference import DraftTargetExists
        from .inference import draft as make_draft
        from .inference import render_draft, write_draft
        frames = _parse_frames(args.frame)
        d = make_draft(frames)
        if not args.out:
            print(render_draft(d))
            return EXIT_OK_SILENT
        # WRITING IS THE DEFAULT PATH A USER TAKES. R233 §1(a). Printing only
        # means the user hand-copies the output into a file, which is the
        # transcription step this project spent five rounds removing from its
        # own records; a feature whose first step is "copy this carefully" is
        # not an ease feature.
        try:
            p = write_draft(
                d, args.out,
                generated_by="leakaudit draft",
                commit=_head_commit(),
                source_frames={k: (int(v.shape[0]), int(v.shape[1]))
                               for k, v in frames.items()})
        except DraftTargetExists as e:
            raise SystemExit(str(e))
        print(render_draft(d))
        print()
        print("WRITTEN: %s" % p)
        print("It is a DRAFT: its structure is determined and its availability "
              "fields are blank.")
        print("`leakaudit run --model %s` will REFUSE until you fill them, and "
              "the refusal names each one." % p)
        return EXIT_OK_SILENT
    if args.command not in ("run", "check"):
        ap.print_help()
        return EXIT_USAGE

    # The pipeline spec first: it is a string check needing no I/O, so a
    # malformed one is reported before megabytes are read for a run that was
    # never going to happen.
    build = guarded_build(_load_callable(args.pipeline))
    frames = _parse_frames(args.frame)
    if args.command == "check":
        return _run_checks(frames, build, args.model)
    if args.model:
        result = _run_availability(frames, build, args.model,
                                   args.stride, args.max_cohorts,
                                   slice_from=args.slice_from,
                                   padding=args.padding,
                                   label_cohorts=args.label_cohorts,
                                   complete=args.complete,
                                   confirm=args.confirm,
                                   confirm_cap=(DEFAULT_CONFIRM_CAP
                                                if args.confirm_cap is None
                                                else args.confirm_cap))
    else:
        result = audit(frames, build)

    if args.quiet:
        for f in result.findings:
            print(f)
    else:
        print(result)

    # AN INTERFERENCE CLASS IS ITS OWN EXIT. R272 §2(e). It is a fact about the
    # run's stride, not about one finding and not a usage error: a cohort's
    # corruption reached another cohort's window, so no silence in the run is
    # licensed. The findings stay printed above -- the confirmed ones are real
    # regardless -- and the exit takes precedence over the findings exit.
    _interference = getattr(getattr(result, "source", None),
                            "interference_reason", None)
    if _interference:
        print("leakaudit: RUN INTERFERED -- %s. Every silence in this run is "
              "none(%s); the CONFIRMED findings printed above are real "
              "regardless. Re-run without --stride so the floor from the block "
              "reach is used, or with a stride above it. Exit %d."
              % (_interference, _interference, EXIT_INTERFERENCE),
              file=sys.stderr)
        return EXIT_INTERFERENCE
    if result.findings:
        return EXIT_FINDINGS
    if result.outcome != "observed_silence":
        return EXIT_NOTHING_PROBED

    # FOUR CLASSES, NOT THREE. R267 §3(d). The run was silent; the question left
    # is whether it was silent over EVERYTHING eligible or over a subsample.
    cov = getattr(result, "coverage", None)
    if cov is None or cov.complete:
        return EXIT_OK_SILENT
    if getattr(args, "accept_partial_coverage", False):
        print("ACCEPTED: partial coverage was declared on the command line, so "
              "this INCOMPLETE run exits clean. The silence above is about the "
              "%d of %d cohorts probed, and the acceptance is yours."
              % (cov.cohorts_probed, cov.cohorts_eligible))
        return EXIT_OK_SILENT
    print("INCOMPLETE AND SILENT: nothing moved in the %d of %d eligible "
          "cohorts this run probed, which is not the same claim as nothing "
          "moving. Run it with --complete to probe every eligible cohort -- for "
          "L3.1 that is passes at different offsets, and a larger budget alone "
          "cannot do it, since one pass covers one second in the stride -- or "
          "pass --accept-partial-coverage to declare that a subsample is enough "
          "for your purpose." % (cov.cohorts_probed, cov.cohorts_eligible),
          file=sys.stderr)
    return EXIT_INCOMPLETE_SILENT


if __name__ == "__main__":                                   # pragma: no cover
    raise SystemExit(main())
