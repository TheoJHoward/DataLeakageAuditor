"""Read the recorded probe path set, and check a run against it. R212 §2.

WHY THIS IS A MODULE AND NOT A PARAGRAPH. The standing rule -- any round that
changes a module on the availability probe's execution path re-runs the
whole-frame fixture guard -- needs a population. A population written as prose in
a practices document is a docstring: it diverges from the real call graph the
first time a module is added, and nothing notices. So the set lives in
`evidence/session/PROBE_PATH_SET.json` as DATA and this module reads it. It does
not carry its own copy of the list.

IT FAILS LOUDLY WHEN IT CANNOT READ THE SET. A guard that silently covers nothing
because its population file moved is the discarded-parameter defect a third time
in this project, and it is the one failure this module refuses to have.

TWO THINGS IT DOES.

  `path_set()`      the recorded modules, for a caller deciding whether a round
                    touched one.
  `watch()`         a context manager that records every leakaudit/protocol
                    frame a run actually enters, so a module reached at guard
                    time and ABSENT from the file is reported by the guard
                    itself. That is the cheap staleness trigger: the set cannot
                    drift while the thing reading it keeps passing.

WHAT THE TRIGGER DOES NOT CATCH, stated rather than left for someone to find: a
module that becomes reachable only on data this run does not exercise. The
trigger sees what executed, so it detects additions along paths that are taken
and is silent about paths that are not.
"""
from __future__ import annotations

import contextlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
SET_FILE = REPO / "evidence" / "session" / "PROBE_PATH_SET.json"


class ProbePathSetError(RuntimeError):
    """The recorded path set could not be read. Never a silent empty set."""


def load() -> dict:
    """The whole record, or a refusal naming what is wrong with it."""
    if not SET_FILE.exists():
        raise ProbePathSetError(
            "%s is missing. The guard rule's population lives in that file and "
            "this module deliberately carries no copy of it, so a missing file "
            "is a guard that covers nothing rather than a guard that covers "
            "everything. Restore it, or re-measure the set." % SET_FILE)
    try:
        doc = json.loads(SET_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise ProbePathSetError(
            "%s could not be read as JSON (%s). It is refused rather than "
            "partially read: a half-parsed population covers less than it names "
            "and says nothing about the difference." % (SET_FILE, e))
    for key in ("path_set", "measured_at_commit", "method"):
        if key not in doc:
            raise ProbePathSetError(
                "%s has no %r key, so it is not the record this guard reads."
                % (SET_FILE, key))
    if not isinstance(doc["path_set"], list) or not doc["path_set"]:
        raise ProbePathSetError(
            "%s carries an empty or non-list `path_set`. An empty population is "
            "a rule that covers nothing, and it is refused rather than obeyed."
            % SET_FILE)
    return doc


def path_set() -> frozenset[str]:
    """Repo-relative module paths the availability probe's execution reaches."""
    return frozenset(load()["path_set"])


def measured_at() -> str:
    return str(load()["measured_at_commit"])


def _rel(filename: str) -> str | None:
    """A repo-relative path for a frame's file, or None if it is not ours."""
    try:
        p = pathlib.Path(filename).resolve()
    except (OSError, ValueError):
        return None
    try:
        rel = p.relative_to(REPO)
    except ValueError:
        return None
    s = str(rel).replace("\\", "/")
    # The fixture's own producing code is included because the opt-in tests
    # attest the ADAPTER AGAINST IT: if `phase5_ml_fixture.py` changes, "the
    # adapter reproduces the fixture exactly" is a claim about a different
    # fixture. It is not part of the probe's path set and `watch()` never sees
    # it there, because the probe is handed frames rather than producing them.
    if (s.startswith("src/leakaudit/") or s.startswith("protocol/")
            or s.startswith("evidence/fixture_spike/f2/")):
        return s
    return None


MONITORING_AVAILABLE = hasattr(sys, "monitoring") and hasattr(
    getattr(sys, "monitoring", None), "use_tool_id")


class Unsupported(RuntimeError):
    """The instrument cannot run here. NOT a failure, and not a pass either.

    `PREREG.md` §8.2's vocabulary: `unsupported` is accounted separately from
    findings, everywhere. A guard that cannot run on an interpreter reports that
    it did not run, which is the same three-state discipline the rest of this
    project applies to silences -- `none` is not `observed_silence`, and "the
    recorder is unavailable" is not "no drift".
    """


# WHY THERE IS NO setprofile FALLBACK, MEASURED RATHER THAN ASSERTED. R229 §2(b).
FALLBACK_MEASURED = (
    "A `sys.setprofile` fallback was measured on this recorder's actual "
    "workload -- one whole-frame guard side over the acceptance fixture, "
    "CPython 3.12.10 -- and REJECTED, but not for its cost, which turned out "
    "affordable: 379.5 s against a 209.2 s unprofiled baseline (x1.8), where "
    "`sys.monitoring` cost 185.8 s (x0.9, free within run-to-run noise). It was "
    "rejected because IT RECORDED HALF THE MODULES: 2 against monitoring's 4 on "
    "the same run. `PY_START` fires for every code object entered; a `call` hook "
    "does not, so the fallback's executed set is a SUBSET of the real one -- and "
    "this guard's whole job is to name modules that ran and are not in the "
    "recorded set. A recorder that sees less reports 'no drift' more often, "
    "which is a false negative in the one direction that matters. Closing that "
    "gap and re-measuring is open work, not a decision already taken."
)


TOOL_ID = 4                      # sys.monitoring "profiler" slot


@contextlib.contextmanager
def record_modules():
    """Record which of THIS REPOSITORY's modules a run executes. No comparison.

    Split out from `watch` because two different questions use the same
    instrument and only one of them compares against the probe path set. The
    opt-in fixture tests have their own execution set -- `fixture_adapter.py` is
    in it and not in the probe's -- and merging the two for tidiness would make
    one file answer two questions badly. See R213 §3.

    USES `sys.monitoring`, NOT `sys.setprofile`, AND THE REASON IS MEASURED. The
    setprofile version fires on every Python call for the life of the run. Over
    the opt-in fixture tests -- a real multi-million-row rebuild -- it had
    produced no answer after fifteen minutes against an unprofiled runtime of
    288 seconds, and was abandoned rather than waited out. `sys.monitoring` can
    DISABLE itself per code object, so each function is seen once and costs
    nothing thereafter: the answer wanted here is which files executed, not how
    often, and a first sighting is the whole of it.

    IMPORT TIME COUNTS AS EXECUTION, and a caller who does not want it must warm
    its imports before entering. A module's top level runs on first import, so a
    recorder started before the imports reports every module the package pulls in
    -- fifteen of them for a bare `import leakaudit` -- rather than the ones the
    work reaches. MV-8's measurement imported first and is unaffected; this note
    exists because the same instrument used carelessly gives a set four times too
    large, and a population that is too large makes the rule that reads it weaker
    while looking more thorough.
    """
    seen: set[str] = set()
    if not MONITORING_AVAILABLE:                            # pragma: no cover
        raise Unsupported(
            "this recorder needs `sys.monitoring`, which is CPython 3.12+, and "
            "this is %s. The instrument does not run here and says so rather "
            "than reporting a smaller executed set as if it were the whole one. "
            "%s" % (".".join(str(v) for v in sys.version_info[:3]),
                    FALLBACK_MEASURED))
    mon = sys.monitoring

    def on_start(code, offset):
        rel = _rel(code.co_filename)
        if rel is not None:
            seen.add(rel)
        return mon.DISABLE          # never ask about this code object again

    mon.use_tool_id(TOOL_ID, "leakaudit-path-recorder")
    try:
        mon.register_callback(TOOL_ID, mon.events.PY_START, on_start)
        mon.set_events(TOOL_ID, mon.events.PY_START)
        try:
            yield seen
        finally:
            mon.set_events(TOOL_ID, 0)
            mon.register_callback(TOOL_ID, mon.events.PY_START, None)
    finally:
        mon.free_tool_id(TOOL_ID)


@contextlib.contextmanager
def watch(report=print):
    """Record which of our modules a run enters, and report drift from the file.

    Yields the growing set, so a caller can inspect it. On exit it names any
    module that executed and is not in the recorded set -- the cheap staleness
    trigger R212 §2(d) asks for.

    THE RECORDER IS `record_modules`, AND IT WAS NOT ALWAYS. This function
    carried its own `sys.setprofile` hook, and the whole-frame fixture guard was
    wired to run inside it. `record_modules` was rewritten onto `sys.monitoring`
    when setprofile's cost was measured -- no answer in fifteen minutes against
    an unprofiled 288 seconds -- and THIS COPY WAS NOT. The next guard run took
    over thirty-four minutes against a usual eight and a half, and was killed
    rather than waited out.

    Two things that made it survive: no guard ran between the wiring and that
    run, so nothing exercised the combination; and the duplication was invisible
    because both functions were correct in isolation. It is TB-14's shape -- an
    extraction that replaced nothing -- with the copy left inside the caller.
    There is now ONE recorder and this function calls it.
    """
    recorded = path_set()
    try:
        with record_modules() as seen:
            yield seen
    finally:
        unrecorded = sorted(seen - recorded)
        if unrecorded:
            report(
                "PROBE PATH SET IS STALE: this run executed %s, which %s does "
                "not record. The set was measured at commit %s. Re-measure it, "
                "or the guard rule's population is smaller than the code it is "
                "meant to cover."
                % (", ".join(unrecorded), SET_FILE.name, recorded and
                   load()["measured_at_commit"]))
        else:
            report("probe path set: %d recorded, %d executed, no drift"
                   % (len(recorded), len(seen)))


if __name__ == "__main__":                                  # pragma: no cover
    doc = load()
    print("probe path set, measured at %s on %s"
          % (doc["measured_at_commit"], doc.get("measured_on", "?")))
    for m in doc["path_set"]:
        print("  %-40s %s" % (m, doc.get("path_set_reasons", {}).get(m, "")))
    extra = doc.get("added_by_judgment_not_by_the_trace", {})
    if extra:
        print("  -- added by judgment, not by the trace --")
        for m in extra:
            print("  %s" % m)
