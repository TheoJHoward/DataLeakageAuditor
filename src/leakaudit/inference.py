"""Draft an availability model from the frames. R232 §5, spec at R215 §3.

**INFER WHAT IS IN THE DATA; REQUIRE WHAT IS ABOUT THE WORLD.** That sentence is
the whole design and it is the reason this module can exist at all.

STRUCTURE is in the frames: which column is a key, what granularity it has,
whether it sits on second boundaries, which frames join to which. Those are shapes
and they are determinable, so they are determined and marked as determined, with
the evidence named per column.

AVAILABILITY is not in the frames. When a value became knowable is a fact about
how it was published, and `PRE_BUILD_READS.md` §1 measured the demonstration:
**two datasets with byte-identical key columns can have availability a full second
apart** — an aggregate over [t, t+1s) and an instantaneous reading at t look the
same and are not. No signal over shape can separate them, so this module never
writes an availability value. It writes the observable evidence beside the column
and leaves the field blank.

    INFERENCE PROPOSES; IT NEVER PICKS.  R204, R212 §4.1. What comes out is a
    DRAFT MODEL FILE, not an audit. A column this cannot resolve is reported
    unresolved rather than defaulted -- `PREREG.md` §8.2's shape, which this
    package applies everywhere else.

WHY A BLANK AND NOT A GUESS-WITH-A-WARNING. A warned guess is still a value, and a
value in an availability model is a claim the audit will act on. The failure this
whole package exists to prevent is a declaration accepted and silently wrong; a
drafted availability value would be that failure shipped as a convenience.

S6 IS OMITTED, AND THE REASON IS HERE BECAUSE HERE IS WHERE SOMEBODY WOULD ADD IT.
The column probe already produces a dependency map -- which columns the build
actually reads -- and it is the most reliable-looking signal available:

    Which columns are read is not when they became knowable; it can only produce
    "read, therefore available" -- the assumption of no leak restated as a
    finding.

It is the most tempting signal precisely because it is the most reliable, and it
is the one that would turn the tool into a mirror. `draft()` names it as omitted
in its own output, so the omission is visible rather than absent.
"""
from __future__ import annotations

import json
import pathlib

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

# The signals, by the identifiers `PRE_BUILD_READS.md` §1 gave them. Each ships
# with the wrong case that document constructed for it, and each wrong case is a
# test that this module must NOT answer confidently on.
SIGNALS_USED = ("S2", "S3")
SIGNALS_OMITTED = {
    "S1": ("a datetime column whose NAME suggests a release instant. Names are "
           "not evidence: `expiry_at` matches and holds a FUTURE instant, and "
           "`birth_date` matches and is knowable decades early. Both would put "
           "availability somewhere it is not."),
    "S4": ("a column constant in the sample, proposing `always`. Constant IN THE "
           "WINDOW is not constant in general -- a quarterly-revised "
           "configuration value sampled inside one quarter is indistinguishable "
           "from a genuinely static one."),
    "S5": ("the same, for the availability direction."),
    "S6": ("THE DEPENDENCY MAP, and this one is a category error rather than an "
           "edge case. Which columns are read is not when they became knowable; "
           "it can only produce 'read, therefore available' -- the assumption of "
           "no leak restated as a finding. It is the most reliable-LOOKING "
           "signal available and the one that would turn the tool into a "
           "mirror."),
    "S7": ("a column named like the decision column. A reference table's "
           "`timestamp` is its LOAD time, which says nothing about the instant "
           "of the fact it records."),
}

UNFILLED = None                      # never a value; never a default


@dataclass
class ColumnDraft:
    """What was determined about one column, and what deliberately was not."""
    column: str
    frame: str
    dtype: str
    # STRUCTURE -- determined, with the evidence that determined it.
    role: str = ""                   # "key candidate", "numeric", "identifier"...
    structure_evidence: list = field(default_factory=list)
    # AVAILABILITY -- never determined. The evidence is FOR THE USER to read.
    availability: object = UNFILLED
    availability_evidence: list = field(default_factory=list)

    @property
    def availability_is_unfilled(self) -> bool:
        return self.availability is UNFILLED


@dataclass
class FrameFork:
    """One frame's datetime evidence, and the choice it does NOT make.

    `aggregate_frames` IS AN AVAILABILITY MODE, NOT STRUCTURE. R234 §0. Declaring
    a frame an aggregate says its cells become knowable at `floor(key) + window`
    rather than at the key -- a claim about publication, which is the require
    side. The first version of this module assigned it to any frame with one
    datetime column, because that is what a lone timestamp LOOKS like.

    THE STATION FRAME IS THE PROOF AND IT IS THE DISCRIMINATING CASE. In the live
    run it has exactly one datetime column and got `aggregate_frames` -- and it
    carries the DECISION INSTANT, not an aggregate. The draft filled a field it
    should have left blank, through the one field nobody guarded because it
    looked structural. That is the mirror risk this whole draft/require split
    exists to prevent, found inside the feature built to prevent it.
    """
    frame: str
    datetime_columns: list = field(default_factory=list)
    evidence: list = field(default_factory=list)
    mode: object = UNFILLED          # never assigned here

    @property
    def mode_is_unfilled(self) -> bool:
        return self.mode is UNFILLED


@dataclass
class Draft:
    """A draft model file: structure reported, every mode blank, both said."""
    frames: dict = field(default_factory=dict)      # frame -> [ColumnDraft]
    forks: dict = field(default_factory=dict)       # frame -> FrameFork
    decision_column: object = UNFILLED
    notes: list = field(default_factory=list)
    unresolved: list = field(default_factory=list)  # (frame, column, why)

    @property
    def columns(self) -> list:
        return [c for cols in self.frames.values() for c in cols]

    @property
    def unfilled_fields(self) -> list:
        """Everything the audit will refuse on. ONE list, not two. R234 §0(b)."""
        out = ["%s (availability mode)" % f
               for f, fk in sorted(self.forks.items()) if fk.mode_is_unfilled]
        out += ["%s.%s (availability)" % (c.frame, c.column)
                for c in self.columns
                if c.availability_evidence and c.availability_is_unfilled]
        return sorted(out)


HEADER = (
    "The structure below was determined from your data. Every AVAILABILITY field "
    "is blank because your data does not contain it: when a value became "
    "knowable is a fact about how it was published, not a shape in the frames -- "
    "two datasets with identical timestamps can have availability a full second "
    "apart. THAT INCLUDES WHICH FRAMES ARE AGGREGATES: `aggregate_frames` is an "
    "availability mode, not a shape, and a frame with one timestamp column looks "
    "the same whether it aggregates an interval or carries your decision "
    "instant. Fill them in, or the audit will refuse rather than guess on your "
    "behalf.")


def _is_datetimeish(s: pd.Series) -> bool:
    """Does this column hold instants, however it is stored?

    EXCLUDE WHAT CANNOT BE A TIMESTAMP, THEN TRY TO PARSE. The first version
    asked `s.dtype == object`, which is how a string column presents under
    pandas 2 and NOT how it presents under pandas 3 -- where it is `str`. So on
    the development environment every CSV-loaded timestamp column was reported as
    not-datetime-like, and the draft determined nothing at all.

    IT WAS NOT CAUGHT BY THE UNIT TESTS BECAUSE THEY BUILT THEIR FRAMES. Every
    test frame here is constructed with `pd.date_range`, which yields
    `datetime64` and takes the first branch. The CLI loads CSVs, where every
    column arrives as text. **The positive did not exercise the path the user
    takes** -- R215 §0's refinement, and it was found on the first live run
    through `leakaudit draft`, not by the suite.

    Excluding by dtype and then parsing is resolution- and version-independent:
    it does not enumerate the ways a library spells "text".
    """
    if pd.api.types.is_datetime64_any_dtype(s):
        return True
    if (pd.api.types.is_numeric_dtype(s) or pd.api.types.is_bool_dtype(s)
            or pd.api.types.is_timedelta64_dtype(s)):
        return False
    head = s.head(200)
    if not len(head):
        return False
    try:
        parsed = pd.to_datetime(head, errors="coerce", format="mixed")
    except (ValueError, TypeError):
        return False
    return bool(parsed.notna().mean() > 0.95)


def _boundary_fraction(s: pd.Series) -> float:
    """S2's observable: what fraction of stamps sit exactly on a second.

    THE MEASUREMENT IS REPORTED; THE CONCLUSION IS NOT DRAWN. `PRE_BUILD_READS.md`
    §1 constructed S2's wrong case and it is decisive: a 1 Hz sensor lattice has
    every stamp on an exact second and no row is an aggregate. An aggregate over
    [t, t+1s) and an instantaneous reading at t have IDENTICAL key columns, so
    this fraction cannot tell them apart -- and the difference between them is a
    full second of availability.
    """
    t = pd.to_datetime(s, errors="coerce")
    t = t.dropna()
    if not len(t):
        return float("nan")
    # FLOOR-AND-COMPARE, NOT MODULO ON THE INTEGER VIEW. The first version was
    # `t.astype("int64") % 1_000_000_000 == 0`, which assumes the integer view is
    # NANOSECONDS. On a `datetime64[us]` column -- what `pd.date_range` produces
    # under pandas 3 -- it is microseconds, so every stamp on an exact second
    # came out as NOT on a boundary and the fraction read 0.00%. Caught on the
    # first run of S2's own wrong-case test, which is the case that exists to
    # notice exactly this. Flooring is resolution-independent.
    return float((t.dt.floor("s") == t).mean())


def _monotone(s: pd.Series) -> bool:
    t = pd.to_datetime(s, errors="coerce").dropna()
    return bool(len(t)) and bool(t.is_monotonic_increasing)


def draft(frames: dict) -> Draft:
    """Draft a model from the frames. Structure determined, availability blank.

    Every column gets an entry. A column whose structure cannot be determined is
    reported unresolved with the ambiguity named, which is `PREREG.md` §8.2's
    shape: not resolved is reported as not resolved, never as a default.
    """
    d = Draft()
    d.notes.append(HEADER)
    d.notes.append(
        "SIGNALS USED: %s. OMITTED: %s. Each omission has a constructed case "
        "where it would be wrong, recorded in "
        "`evidence/session/PRE_BUILD_READS.md` and in this module's "
        "`SIGNALS_OMITTED`."
        % (", ".join(SIGNALS_USED), ", ".join(sorted(SIGNALS_OMITTED))))

    for fname, f in frames.items():
        cols = []
        for c in f.columns:
            s = f[c]
            cd = ColumnDraft(column=str(c), frame=fname, dtype=str(s.dtype))
            if _is_datetimeish(s):
                frac = _boundary_fraction(s)
                mono = _monotone(s)
                cd.role = "timestamp candidate"
                cd.structure_evidence.append(
                    "parses as datetime; %.4f%% of values sit exactly on a "
                    "wall-clock second; %s"
                    % (100.0 * frac, "monotone increasing" if mono
                       else "NOT monotone -- so successive differences would run "
                            "backwards if taken in row order"))
                # S2 and S3 are OBSERVATIONS handed to the user, not conclusions.
                cd.availability_evidence.append(
                    "S2: %.2f%% of stamps are on a second boundary. If these "
                    "rows AGGREGATE an interval, the value is knowable at the "
                    "interval's end, not at its start -- and if they are "
                    "instantaneous readings it is knowable at the stamp. The key "
                    "column is IDENTICAL in both cases; only you know which."
                    % (100.0 * frac))
                if not mono:
                    cd.availability_evidence.append(
                        "S3: this column is not monotone, so it is not an event "
                        "clock in arrival order. That is a fact about the "
                        "column; whether it is the right clock for availability "
                        "is not.")
            elif pd.api.types.is_numeric_dtype(s):
                cd.role = "numeric"
                n = int(s.nunique(dropna=True))
                cd.structure_evidence.append("%d distinct value(s)" % n)
                if n <= 1:
                    d.unresolved.append((
                        fname, str(c),
                        "one distinct value in this sample. S4's wrong case: "
                        "constant IN THE WINDOW is not constant in general, so "
                        "neither `always` nor anything else is proposed here."))
            else:
                cd.role = "non-numeric"
                cd.structure_evidence.append("dtype %s" % s.dtype)
            cols.append(cd)
        d.frames[fname] = cols

        keys = [c for c in cols if c.role == "timestamp candidate"]
        fork = FrameFork(frame=fname,
                         datetime_columns=[k.column for k in keys])
        if len(keys) == 1:
            k = keys[0]
            keys[0].structure_evidence.append(
                "the only datetime-like column in frame %r" % fname)
            fork.evidence.append(
                "one datetime column, %r. THE FORK, AND ONLY YOU CAN TAKE IT: "
                "if this frame AGGREGATES an interval, `aggregate_frames[%r] = "
                "%r` fits and its cells become knowable at floor(key) + window. "
                "If it carries the DECISION INSTANT -- the clock your output "
                "rows are built on -- it is not an aggregate at all and belongs "
                "in `decision_column` instead. The two look identical here."
                % (k.column, fname, k.column))
        elif len(keys) > 1:
            fork.evidence.append(
                "%d datetime columns, %s. S3's wrong case, live: monotonicity "
                "gives no basis to choose between them, and naming one would "
                "infer a pipeline that may not exist."
                % (len(keys), ", ".join(repr(k.column) for k in keys)))
            d.unresolved.append((
                fname, ", ".join(k.column for k in keys),
                "S3's wrong case, live: %d datetime-like columns and "
                "monotonicity gives no basis to choose between them."
                % len(keys)))
        else:
            fork.evidence.append(
                "no datetime column, so this frame has no key to aggregate on.")
            d.unresolved.append((
                fname, "(whole frame)",
                "no datetime-like column, so no key was determined."))
        d.forks[fname] = fork
    return d


def render_draft(d: Draft) -> str:
    """The draft as a user reads it, with the header first.

    THE HEADER IS THE FEATURE, not decoration. Without it a reader meets a file
    that is half filled in and concludes the tool failed on the other half. With
    it they meet a file that says which half is knowable from data and why the
    other half is theirs -- which is the one idea this whole module exists to
    communicate.
    """
    out = [HEADER, ""]
    for note in d.notes[1:]:
        out += [note, ""]

    out.append("OBSERVED IN YOUR DATA -- and NOT turned into a mode")
    for fname, fork in sorted(d.forks.items()):
        out.append("  %s: %s" % (fname, "; ".join(fork.evidence)))
        out.append("    availability mode: <BLANK -- you decide>")
    out.append("")

    out.append("NOT DETERMINED, AND NOT GUESSED -- availability")
    out.append("  Every column below has a BLANK availability field. The evidence")
    out.append("  under each is what your data shows; the answer is what you know.")
    for cd in d.columns:
        if not cd.availability_evidence:
            continue
        out.append("")
        out.append("  %s.%s  (%s, %s)"
                   % (cd.frame, cd.column, cd.dtype, cd.role))
        out.append("    availability: <BLANK -- fill this in>")
        for e in cd.structure_evidence:
            out.append("    structure:    %s" % e)
        for e in cd.availability_evidence:
            out.append("    evidence:     %s" % e)

    if d.unresolved:
        out += ["", "UNRESOLVED -- reported as unresolved, never defaulted"]
        for fname, col, why in d.unresolved:
            out.append("  %s.%s" % (fname, col))
            out.append("    %s" % why)

    out += ["", "SIGNALS DELIBERATELY OMITTED, with the case that rules each out"]
    for sig in sorted(SIGNALS_OMITTED):
        out.append("  %s: %s" % (sig, SIGNALS_OMITTED[sig]))
    return "\n".join(out)


class UnfilledAvailability(ValueError):
    """A draft reached the audit with its availability fields still blank.

    NOT A DEFAULT AND NOT AGREEMENT. `PREREG.md` §2.4 says label availability is
    never defaulted, and the same reasoning governs here: a blank field is the
    user not having answered, and reading silence as assent is exactly the defect
    -- a declaration accepted and silently wrong -- that this package exists to
    find in other people's pipelines.
    """


def accept(d: Draft, availability: dict) -> dict:
    """Turn a draft into a model dict once the user has filled the blanks.

    REFUSES rather than defaulting. `availability` maps "frame.column" to the
    user's answer, and every column the draft left blank has to appear in it.
    """
    missing = [f for f in d.unfilled_fields if f not in availability]
    if missing:
        raise UnfilledAvailability(
            "these fields were drafted BLANK and are still blank: %s. The draft "
            "does not fill them and neither does this: when a value became "
            "knowable is a fact about how your data was published, and nothing "
            "in the frames carries it. THE FRAME-LEVEL MODES ARE IN THAT LIST "
            "TOO -- `aggregate_frames` says a frame's cells arrive at "
            "floor(key) + window rather than at the key, which is a claim about "
            "publication and not a shape. An unfilled field is refused rather "
            "than defaulted, because a default here is an availability model "
            "you did not write." % ", ".join(sorted(missing)))
    aggregates = {}
    for fname, fork in d.forks.items():
        answer = availability.get("%s (availability mode)" % fname)
        if isinstance(answer, str) and answer.startswith("aggregate:"):
            aggregates[fname] = answer.split(":", 1)[1]
    return {"version": 3, "aggregate_frames": aggregates,
            "note": "accepted from a draft; availability supplied by the user"}


class DraftTargetExists(FileExistsError):
    """The draft would have overwritten a file that is already there.

    NEVER OVERWRITE. A user with a hand-written model who runs `draft` by mistake
    must not lose it, and there is no recovery path from a clobbered config: the
    availability fields in it are the ones nothing can reconstruct, because they
    were never in the data. One check, and it is the irreversible-act rule
    applied at the only place in this package that writes a user's file.
    """


def as_model_dict(d: Draft, *, generated_by: str, commit: str,
                  source_frames: dict) -> dict:
    """The draft as a config file, with its provenance and its blanks marked.

    THE FRAME TRAVELS WITH THE FIGURE, applied to a model file. Every field the
    draft filled is marked DETERMINED-FROM-DATA and every field it left blank is
    listed under `unfilled_availability`, so the loader can refuse by name rather
    than generically and a later reader can tell what a person decided from what
    a program observed.
    """
    from .model_file import FILL_ME

    # THE SKELETON IS GENERATED FROM THE SAME PASS, NOT TYPED ALONGSIDE IT.
    # R234 §1. A skeleton written by hand beside the draft is two descriptions of
    # one thing, and they drift -- which is the defect this project has recorded
    # under a dozen names. Both come out of `d` here.
    #
    # JSON HAS NO COMMENTS, so the guidance cannot sit beside the value. It sits
    # in `column_mode_evidence`, keyed the same, and the value is a sentinel the
    # LOADER refuses. A fill-me left unfilled is an unfilled field, not a mode.
    skeleton, evidence = {}, {}
    for c in d.columns:
        if not c.availability_evidence:
            continue
        skeleton[c.column] = FILL_ME
        evidence[c.column] = " | ".join(c.availability_evidence)
    for fname, fork in sorted(d.forks.items()):
        evidence["(frame) %s" % fname] = " | ".join(fork.evidence)

    # THE DECISION COLUMN IS SCAFFOLDED TOO, and the evidence says why this
    # draft cannot name candidates for it. R235 §1.
    #
    # `decision_column` names a column of the BUILT OUTPUT. `draft()` takes
    # frames and never runs the pipeline -- the boundary that keeps S6 out --
    # so the built output is a thing it has never seen. It can scaffold the
    # question and it cannot enumerate the answers, and saying so is more use
    # than listing source-frame columns that may not survive the build.
    evidence["(decision) decision_column"] = (
        "THE COLUMN OF YOUR BUILT OUTPUT holding each row's decision instant -- "
        "the moment that row's prediction was made. This draft cannot list "
        "candidates for it: it reads your FRAMES and never runs your pipeline, "
        "so it has not seen the output. There is NO DEFAULT: until R235 an "
        "undeclared decision column silently became `timestamp`, and on a frame "
        "set whose true clock produced three findings that default produced "
        "`observed_silence` -- a real leak reported as evidence of absence.")

    body = {
        "version": 3,
        "decision_column": FILL_ME,
        "note": HEADER,
        "draft_provenance": {
            "generated_by": generated_by,
            "commit": commit,
            "source_frames": {k: list(v) for k, v in sorted(source_frames.items())},
            "observed_not_decided": {
                f: fk.datetime_columns for f, fk in sorted(d.forks.items())},
            "unfilled_availability": list(d.unfilled_fields),
            "unfilled_other": (["decision_column"]
                               if d.decision_column is UNFILLED else []),
            "decision_column_is_scaffolded": d.decision_column is UNFILLED,
            "column_mode_evidence": evidence,
            "structure_edited_by_hand": False,
            "signals_used": list(SIGNALS_USED),
            "signals_omitted": sorted(SIGNALS_OMITTED),
        },
    }
    if skeleton:
        body["column_modes"] = skeleton
    return body


def write_draft(d: Draft, path, *, generated_by: str, commit: str,
                source_frames: dict) -> pathlib.Path:
    """Write the draft as JSON. REFUSES if the target exists."""
    p = pathlib.Path(path)
    if p.exists():
        raise DraftTargetExists(
            "%s already exists and this will not overwrite it. If it is a model "
            "you wrote, its availability fields are the ones nothing can "
            "reconstruct -- they were never in your data. Move it aside, or "
            "name a different target." % p)
    body = as_model_dict(d, generated_by=generated_by, commit=commit,
                         source_frames=source_frames)
    p.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n",
                 encoding="utf-8", newline="\n")
    return p
