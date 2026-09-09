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
        "run", help="probe which source columns your pipeline's output reads")
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
    run.add_argument("--stride", type=int, default=97, metavar="N",
                     help="probe every Nth second (availability runs only). "
                          "Corrupted seconds are kept far apart so a moved row "
                          "is attributable to exactly one of them")
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


def _run_availability(frames, build, model_path, stride, max_cohorts,
                      slice_from=None, padding=None):
    """The availability probe, end to end, from a declared model file."""
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
        cohort_stride=stride, max_cohorts=min(max_cohorts, 25))
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
    picked = _secs[::stride][:max_cohorts]
    elig = eligible_cohorts(frames, model, picked,
                            pd.to_datetime(built[dcol]))
    traces = traces_for(result, elig.eligible, case_id="user")
    for note in elig.notes:
        result.notes.append(note)

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
    return AuditResult(traces, source=result)


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
                                   padding=args.padding)
    else:
        result = audit(frames, build)

    if args.quiet:
        for f in result.findings:
            print(f)
    else:
        print(result)

    if result.findings:
        return EXIT_FINDINGS
    if result.outcome == "observed_silence":
        return EXIT_OK_SILENT
    return EXIT_NOTHING_PROBED


if __name__ == "__main__":                                   # pragma: no cover
    raise SystemExit(main())
