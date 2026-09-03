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
    if s.startswith("src/leakaudit/") or s.startswith("protocol/"):
        return s
    return None


@contextlib.contextmanager
def watch(report=print):
    """Record which of our modules a run enters, and report drift from the file.

    Yields the growing set, so a caller can inspect it. On exit it names any
    module that executed and is not in the recorded set -- the cheap staleness
    trigger R212 §2(d) asks for.
    """
    recorded = path_set()
    seen: set[str] = set()

    def hook(frame, event, arg):
        if event == "call":
            rel = _rel(frame.f_code.co_filename)
            if rel is not None:
                seen.add(rel)
        return None

    old = sys.getprofile()
    sys.setprofile(hook)
    try:
        yield seen
    finally:
        sys.setprofile(old)
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
