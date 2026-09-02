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
from pathlib import Path

EXIT_OK_SILENT = 0          # probes ran, nothing moved
EXIT_FINDINGS = 1           # something moved
EXIT_NOTHING_PROBED = 3     # `none` -- not evidence of absence
EXIT_USAGE = 2


def _load_callable(spec: str):
    if ":" not in spec:
        raise SystemExit(
            "--pipeline takes module:function, e.g. mypkg.features:build. "
            "Got %r, which names no function." % spec)
    mod_name, func_name = spec.rsplit(":", 1)
    try:
        mod = importlib.import_module(mod_name)
    except Exception as e:                                  # noqa: BLE001
        raise SystemExit("could not import %r: %s: %s"
                         % (mod_name, type(e).__name__, e))
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
                     help="your build function, taking the frames and returning "
                          "the built output")
    run.add_argument("--frame", action="append", metavar="name=path",
                     help="an input frame; repeat for several. .parquet, .csv "
                          "or .json")
    run.add_argument("--quiet", action="store_true",
                     help="print the findings only, without the explanation")
    return ap


def main(argv=None) -> int:
    from .contract import audit

    ap = build_parser()
    args = ap.parse_args(sys.argv[1:] if argv is None else argv)
    if args.command != "run":
        ap.print_help()
        return EXIT_USAGE

    # The pipeline spec first: it is a string check needing no I/O, so a
    # malformed one is reported before megabytes are read for a run that was
    # never going to happen.
    build = _load_callable(args.pipeline)
    frames = _parse_frames(args.frame)
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
