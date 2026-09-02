"""Read an availability model from a file. R202 §1.

WHY A FILE AND NOT FLAGS. The model's vocabulary is one shape today and the
registered vocabulary has six modes; putting it on the command line would mean
inventing CLI syntax for something that does not exist yet, and then breaking
users when it does. A file is versioned data: the format grows, the flag does
not. It is also diffable, reviewable and kept in version control.

And the third reason is the one that matters: AN AVAILABILITY MODEL IS A
DECLARATION. This project's whole thesis is that declarations are written down,
kept and checked rather than improvised. A flag invites improvisation at a
prompt; a file invites the thing the method actually requires.

THIS IS A TOOL CONFIG. IT IS NOT THE REGISTERED DECLARATION.
`AVAILABILITY_DECLARATION.md` is a signed, timestamped artifact hashed in a git
tag, carrying a reconstructed availability model for one specific fixture along
with its evidence, its per-column derivations and its gate dispositions. This
file is none of those things: it is what a user hands the tool so the probe knows
which frames are aggregates. It has no standing, it is not a successor to
anything, and no result produced with it is a registered gate result. The names
differ deliberately -- `.leakaudit-model.json`, not anything shaped like the
registered file -- so the two cannot be confused at a glance.

THE VERSION IS REFUSED, NOT NEGOTIATED. An unknown version is not read
best-effort. A partially-understood model produces a probe that looks like it ran
and did not check what the user wrote down, which is the silent-wrong-answer
shape this package refuses everywhere else.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .availability import AvailabilityModel

SCHEMA_VERSION = 1
SUPPORTED_VERSIONS = (1,)

# Everything version 1 understands. A key outside this set is refused rather
# than ignored: a typo in a key name is otherwise a silently unapplied setting.
_V1_KEYS = {"version", "aggregate_frames", "decision_column", "window_seconds",
            "ties_available", "note"}
_V1_REQUIRED = {"version", "aggregate_frames"}


class ModelFileError(Exception):
    """The model file cannot be read as written."""


SCHEMA_DOC = """\
leakaudit availability model, schema version 1.

    {
      "version": 1,
      "aggregate_frames": {"trades": "ts_event", "book": "ts_floor"},
      "decision_column": "timestamp",
      "window_seconds": 1.0,
      "ties_available": true,
      "note": "free text, for whoever reads this next"
    }

  version           required. Refused if not one this build understands.
  aggregate_frames  required. Frame name -> the column holding the key of the
                    window that frame aggregates. The frame's declared
                    availability instant is that key plus the window: an
                    aggregate over [k, k+window) is knowable at k+window, and a
                    row deciding inside that span could not have used it.
  decision_column   the built output's column holding each row's decision
                    instant. Default "timestamp".
  window_seconds    the aggregation window. Default 1.0.
  ties_available    whether a value whose instant equals the decision instant
                    counts as available. Default true.
  note              ignored by the tool; kept for the reader.

A frame NOT named in aggregate_frames is not perturbed, and the probe says so:
its silence is `none`, not `observed_silence`.

THIS IS A TOOL CONFIG AND NOT A REGISTERED DECLARATION. It has no standing, it
supersedes nothing, and a result produced with it is not a gate result.
"""


def _refuse(msg: str, path: Path) -> None:
    raise ModelFileError("%s: %s" % (path, msg))


def load_model(path) -> AvailabilityModel:
    """Read an availability model, refusing anything it does not fully understand."""
    path = Path(path)
    if not path.exists():
        raise ModelFileError("%s: no such file" % path)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        _refuse("not valid JSON (%s). The model is refused rather than guessed "
                "at: a partially-read model probes less than you declared and "
                "says nothing about the difference." % e, path)
    if not isinstance(raw, dict):
        _refuse("the top level is %s; an object was expected"
                % type(raw).__name__, path)

    if "version" not in raw:
        _refuse("no `version` field. Refused rather than assumed: a model read "
                "under the wrong schema is a probe that looks like it ran and "
                "did not check what you wrote down. Expected one of %s."
                % (list(SUPPORTED_VERSIONS),), path)
    version = raw["version"]
    if version not in SUPPORTED_VERSIONS:
        _refuse("`version` is %r and this build understands %s. REFUSED, not "
                "read best-effort. Upgrade the tool, or write a model at a "
                "version it knows."
                % (version, list(SUPPORTED_VERSIONS)), path)

    unknown = sorted(set(raw) - _V1_KEYS)
    if unknown:
        _refuse("unknown key(s) %s at version %d. Refused rather than ignored: "
                "an ignored key is a setting you wrote and the tool did not "
                "apply. Known keys: %s."
                % (unknown, version, sorted(_V1_KEYS)), path)
    missing = sorted(_V1_REQUIRED - set(raw))
    if missing:
        _refuse("missing required key(s) %s at version %d" % (missing, version), path)

    frames = raw["aggregate_frames"]
    if not isinstance(frames, dict) or not frames:
        _refuse("`aggregate_frames` must be a non-empty object of "
                "frame name -> key column; a model naming no aggregate frame "
                "would perturb nothing and report a silence about itself", path)
    for k, v in frames.items():
        if not isinstance(k, str) or not isinstance(v, str):
            _refuse("`aggregate_frames` entry %r -> %r is not string -> string"
                    % (k, v), path)

    window = raw.get("window_seconds", 1.0)
    try:
        window_td = pd.Timedelta(seconds=float(window))
    except Exception:                                       # noqa: BLE001
        _refuse("`window_seconds` is %r, which is not a number" % (window,), path)
    if window_td <= pd.Timedelta(0):
        _refuse("`window_seconds` is %r; a window that is zero or negative "
                "describes no span and would mark nothing unavailable"
                % (window,), path)

    ties = raw.get("ties_available", True)
    if not isinstance(ties, bool):
        _refuse("`ties_available` is %r; true or false was expected" % (ties,), path)

    decision = raw.get("decision_column", "timestamp")
    if not isinstance(decision, str) or not decision:
        _refuse("`decision_column` is %r; a column name was expected"
                % (decision,), path)

    return AvailabilityModel(
        aggregate_frames=dict(frames),
        decision_column=decision,
        window=window_td,
        ties_available=ties)
