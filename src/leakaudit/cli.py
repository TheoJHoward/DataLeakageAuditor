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


def _run_availability(frames, build, model_path, stride, max_cohorts):
    """The availability probe, end to end, from a declared model file."""
    from .availability import eligible_cohorts, run_probe_a
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

    result = run_probe_a(frames, build, model, side="user",
                         cohort_stride=stride, max_cohorts=max_cohorts)
    # Eligibility is derived, not assumed: a second no aggregate frame carries a
    # row in has nothing to corrupt, and scheduling it would report a dead
    # process where the truth is an empty probe surface.
    built = build(dict(frames))
    picked = sorted(
        pd.to_datetime(built[model.decision_column]).dt.floor("s").unique()
    )[::stride][:max_cohorts]
    elig = eligible_cohorts(frames, model, picked,
                            pd.to_datetime(built[model.decision_column]))
    traces = traces_for(result, elig.eligible, case_id="user")
    for note in elig.notes:
        result.notes.append(note)
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
    if args.command == "schema":
        from .model_file import SCHEMA_DOC
        print(SCHEMA_DOC)
        return 0
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
                                   args.stride, args.max_cohorts)
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
