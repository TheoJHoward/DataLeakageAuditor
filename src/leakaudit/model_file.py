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
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .availability import AvailabilityModel
from .modes import AVAILABILITY_FN, FILE_MODES, ColumnMode, ModeError

SCHEMA_VERSION = 3
SUPPORTED_VERSIONS = (1, 2, 3)

# THE FILE VERSIONS WITH THE TOOL, NEVER WITH A REGISTRATION. R203 §1.
#
# `PREREG.md` is closed and will never version again, so a config pinned to it
# is pinned to a fossil; a future registration would be a different document
# with its own vocabulary, and a user's config cannot chase both. A user who
# wants their model inside their own pre-registration includes this file and
# hashes it -- that is inclusion, not version coupling, and it works better as
# one coherent artifact than two.
#
# KEYS ARRIVE WITH THEIR CONSUMER. A key the loader reads and ignores is the
# discarded-parameter defect in a file, so `label_column` and `split` are known
# only at version 2 -- the version that shipped with the checks that read them.
# A version-1 file naming them is refused, which is the correct friction: adding
# a key is a versioned change.
_V1_KEYS = {"version", "aggregate_frames", "decision_column", "window_seconds",
            "ties_available", "note"}
_V2_KEYS = _V1_KEYS | {"label_column", "split"}
# Version 3 adds per-column availability modes. `AVAILABILITY_MODES.md`
# states what each computes and was committed before this parser existed.
_V3_KEYS = _V2_KEYS | {"column_modes", "timestamp_column"}
_KEYS_BY_VERSION = {1: _V1_KEYS, 2: _V2_KEYS, 3: _V3_KEYS}

# `aggregate_frames` is required only where an availability model is the point.
# A version-2 file may declare a label and a split and no aggregate frame at all
# -- that is a user running the checks of `leakaudit.checks` and nothing else,
# which is a whole and legitimate use.
_REQUIRED_BY_VERSION = {1: {"version", "aggregate_frames"}, 2: {"version"},
                        3: {"version"}}


class ModelFileError(Exception):
    """The model file cannot be read as written."""


@dataclass(frozen=True)
class LoadedConfig:
    """Everything one config file declares.

    ONE FILE, and R203 §1 is why. To the person writing it this is one thing --
    what my data means. When values became knowable, which column is the label,
    how the split works: those are not two kinds of thing to them. The
    registered/unregistered split is an artifact of this project's history, not
    a property of a user's world, and building that history into their
    configuration surface is how tools become strange to use.

    The distinction is kept where a reader who needs it will find it: the schema
    doc marks, per key, which correspond to vocabulary declared in this
    project's registration and which do not.
    """
    model: AvailabilityModel
    label_column: str | None = None
    train_idx: list | None = None
    test_idx: list | None = None
    column_modes: dict | None = None
    timestamp_column: str = "timestamp"
    version: int = SCHEMA_VERSION

    @property
    def has_availability_model(self) -> bool:
        return bool(self.model.aggregate_frames)


SCHEMA_DOC = """\
leakaudit config, schema version 3.

    {
      "version": 3,
      "aggregate_frames": {"trades": "ts_event", "book": "ts_floor"},
      "decision_column": "timestamp",
      "window_seconds": 1.0,
      "ties_available": true,
      "label_column": "target",
      "split": {"train": [0, 1, 2], "test": [3, 4]},
      "timestamp_column": "timestamp",
      "column_modes": {
        "price":     "at_timestamp",
        "bar_volume": "at_bar_close",
        "cpi":       {"mode": "at_source_timestamp", "column": "cpi_released"},
        "tick_size": "always"
      },
      "note": "free text, for whoever reads this next"
    }

ONE FILE. To you this is one thing: what your data means. Declare what you have
and the tool runs what that supports; declare nothing and it says so rather than
reporting a clean result it did not earn.

  version           required. Refused if not one this build understands.
  aggregate_frames  frame name -> the column holding the key of the window that
                    frame aggregates. The declared availability instant is
                    floor(key) + window -- the END OF THE WALL-CLOCK SECOND the
                    key falls in: an aggregate over [floor(k), floor(k)+window)
                    is knowable at floor(k)+window, and a row deciding inside
                    that span could not have used it.
                    THE FLOOR MATTERS AND THIS TEXT USED TO OMIT IT. If your key
                    is already a whole second the two are the same number. If it
                    is a raw event stamp -- "trades": "ts_event" in the example
                    above is one -- they differ by however far into its second
                    each stamp sits, up to a full window. The run TELLS YOU when
                    it floors a key, with the measured fraction, so this is
                    visible where you meet it and not only here.
                    Required at version 1; optional at version 2, where a file
                    may declare only a label and a split.
  decision_column   the built output's column holding each row's decision
                    instant. Default "timestamp".
  window_seconds    the aggregation window. Default 1.0.
  ties_available    whether a value whose instant equals the decision instant
                    counts as available. Default true, which is the registered
                    default (PREREG.md section 2.3). Setting it false makes a row
                    stamped EXACTLY at an aggregate's completion instant a
                    finding; it changes nothing else, because that is the only
                    input the two comparators disagree about. A run under the
                    non-default branch SAYS SO in its own output, on every
                    finding it produces.
  label_column      version 2. The built output's label column.
  split             version 2. {"train": [...], "test": [...]}, row POSITIONS
                    into the built output.
  timestamp_column  version 3. The frame's clock column. Default "timestamp".
                    READ AND NOT YET CONSUMED, and said here rather than left to
                    be discovered: the probe uses each aggregate frame's own
                    declared KEY as the clock for the modes that need one, so
                    this key is stored and currently reaches nothing. It is
                    documented as inert rather than removed, because removing it
                    would silently break a file that sets it. Declaring it is
                    harmless and changes no result.
  column_modes      version 3. Column -> the rule for when its values became
                    knowable. A bare string names a mode; an object names a mode
                    and the column it reads. THE ARITHMETIC OF EACH MODE IS IN
                    AVAILABILITY_MODES.md, which was written before the parser
                    that reads these. The five a file may declare:
                      at_timestamp         the row's own stamp
                      at_bar_close         that stamp plus the bar duration
                      at_source_timestamp  a named column's value at the row
                      always               before every decision in the frame
                      explicit             a named column's value at the row
                    `availability_fn` is a sixth, reachable from the library
                    only: a file cannot carry a function.
                    A column with NO mode is not given one. It is reported as
                    undeclared rather than defaulted, because an assumed mode is
                    an availability model you did not write.
  note              ignored by the tool; kept for the reader.

WHICH KEYS CORRESPOND TO REGISTERED VOCABULARY, for a reader who needs to know:

  aggregate_frames, decision_column, window_seconds, ties_available,
  column_modes, timestamp_column
      correspond to vocabulary declared in this project's registration -- the
      availability model, the decision instant, the tie comparator, and the
      per-column roles.
  label_column, split, note
      do NOT. They serve checks that are not registered detector rows, or are
      in the neighbourhood of one without being it.

A reader who does not need that distinction is not made to navigate it: the
file is one object and the tool reads it as one.

A frame NOT named in aggregate_frames is not perturbed, and the probe says so:
its silence is `none`, not `observed_silence`. The same holds for every check:
one with nothing declared to run against reports that it did not look, which is
a different sentence from finding nothing.

THIS IS A TOOL CONFIG AND NOT A REGISTERED DECLARATION. It versions with the
TOOL, never with a registration. It has no standing, it supersedes nothing, and
a result produced with it is not a gate result. If you want your model inside
your own pre-registration, include this file and hash it -- that is inclusion,
not version coupling.
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

    known = _KEYS_BY_VERSION[version]
    unknown = sorted(set(raw) - known)
    if unknown:
        later = sorted(k for k in unknown if k in _V3_KEYS)
        newest = {k: (2 if k in _V2_KEYS else 3) for k in later}
        hint = ("" if not later else
                " %s known at version %s; this file declares version %d."
                % (later, sorted(set(newest.values())), version))
        _refuse("unknown key(s) %s at version %d. Refused rather than ignored: "
                "an ignored key is a setting you wrote and the tool did not "
                "apply. Known keys at this version: %s.%s"
                % (unknown, version, sorted(known), hint), path)
    missing = sorted(_REQUIRED_BY_VERSION[version] - set(raw))
    if missing:
        _refuse("missing required key(s) %s at version %d" % (missing, version), path)

    frames = raw.get("aggregate_frames")
    if frames is None:
        # Legitimate at version 2: a file declaring only a label and a split is
        # a user running the checks that need no availability model.
        frames = {}
    elif not isinstance(frames, dict) or not frames:
        _refuse("`aggregate_frames` is present and empty. Omit it, or name at "
                "least one frame: a model naming none would perturb nothing and "
                "report a silence about itself", path)
    for k, v in frames.items():
        if not isinstance(k, str) or not isinstance(v, str):
            _refuse("`aggregate_frames` entry %r -> %r is not string -> string"
                    % (k, v), path)

    label = raw.get("label_column")
    if label is not None and (not isinstance(label, str) or not label):
        _refuse("`label_column` is %r; a column name was expected" % (label,), path)

    modes = None
    raw_modes = raw.get("column_modes")
    if raw_modes is not None:
        if not isinstance(raw_modes, dict) or not raw_modes:
            _refuse("`column_modes` is present and not a non-empty object of "
                    "column -> mode. Omit it, or declare at least one column",
                    path)
        modes = {}
        for col, spec in raw_modes.items():
            if not isinstance(col, str):
                _refuse("`column_modes` key %r is not a column name" % (col,), path)
            if isinstance(spec, str):
                name, src = spec, None
            elif isinstance(spec, dict):
                extra = sorted(set(spec) - {"mode", "column"})
                if extra:
                    _refuse("`column_modes[%r]` carries unknown key(s) %s; "
                            "`mode` and `column` are the two it takes"
                            % (col, extra), path)
                name, src = spec.get("mode"), spec.get("column")
            else:
                _refuse("`column_modes[%r]` is %s; a mode name or an object with "
                        "`mode` and `column` was expected"
                        % (col, type(spec).__name__), path)
            if name not in FILE_MODES:
                _refuse("`column_modes[%r]` names mode %r. A file may declare %s. "
                        "%r exists and is reachable only from the library, "
                        "because a file cannot carry a function."
                        % (col, name, list(FILE_MODES), AVAILABILITY_FN), path)
            try:
                modes[col] = ColumnMode(name, src)
            except ModeError as e:
                _refuse("`column_modes[%r]`: %s" % (col, e), path)

    timestamp_column = raw.get("timestamp_column", "timestamp")
    if not isinstance(timestamp_column, str) or not timestamp_column:
        _refuse("`timestamp_column` is %r; a column name was expected"
                % (timestamp_column,), path)

    split = raw.get("split")
    if split is not None:
        if not isinstance(split, dict):
            _refuse("`split` is %s; an object with `train` and `test` row "
                    "positions was expected" % type(split).__name__, path)
        split_unknown = sorted(set(split) - {"train", "test"})
        if split_unknown:
            _refuse("`split` carries unknown key(s) %s; `train` and `test` are "
                    "the two it takes" % split_unknown, path)
        for side in ("train", "test"):
            if side not in split:
                _refuse("`split` has no `%s`. A one-sided split is not a split, "
                        "and the checks that read it would have nothing to "
                        "compare across" % side, path)
            if not isinstance(split[side], list) or not all(
                    isinstance(i, int) and not isinstance(i, bool)
                    for i in split[side]):
                _refuse("`split.%s` must be a list of integer row positions"
                        % side, path)

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

    return LoadedConfig(
        model=AvailabilityModel(
            aggregate_frames=dict(frames),
            decision_column=decision,
            window=window_td,
            ties_available=ties),
        label_column=label,
        train_idx=None if split is None else list(split["train"]),
        test_idx=None if split is None else list(split["test"]),
        column_modes=modes,
        timestamp_column=timestamp_column,
        version=version)
