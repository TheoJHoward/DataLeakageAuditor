"""The `aggressor_side` class: columns the builder READS that no probe can move.

WHAT THIS IS FOR. B8.3 found `trades.aggressor_side` silent under a valid
shuffle while the builder demonstrably reads it, and the mechanism turned out to
be a predicate that is false for every row: `isin(["B","Buy","buy"])` against a
column holding `SELL_AGGRESSOR`/`BUY_AGGRESSOR`/`UNKNOWN`. **No permutation of
those values can move the output, so no value probe can see the dependency, and
the null detector cannot either -- the mechanism is a constantly false
predicate, not a null pattern.**

That finding was made by reading the source after noticing one odd silence. This
makes the noticing mechanical: **the set of columns the builder's source
references, minus the set the probes moved.** Every member is a candidate for
the class, and each one is a place where a dependency exists in the code and no
detector in the suite can reach it.

WHAT A CANDIDATE IS AND IS NOT. This is a SCREEN, not a verdict. A name in the
source can be a reference the builder never executes, a column of a frame that
is not probed, a string that happens to match, or a genuine
constantly-false-predicate dependency. **Each candidate is a question for a
human to answer by reading, and the screen says so rather than pronouncing.**
The alternative -- reporting the silence alone -- is what would have let
`aggressor_side` die as a probe hole.

THE INSTRUMENT'S POPULATION EXCLUDES THE INSTRUMENT. This file is not the
builder and is never scanned. The builder source is named on the command line
and its line count is asserted before anything is derived.

    usage: reference_but_silent.py <builder-source.py> <merged-result.json> [...]
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

SRC = pathlib.Path(sys.argv[1])
RESULTS = [pathlib.Path(p) for p in sys.argv[2:]]

source = SRC.read_text(encoding="utf-8", errors="replace")
print("=" * 78)
print("POPULATION, ASSERTED BEFORE ANYTHING IS DERIVED")
print("=" * 78)
print("  builder source : %s" % SRC.name)
print("  lines          : %d" % len(source.split("\n")))
if len(source.split("\n")) < 100:
    sys.exit("HALT: the builder source is %d lines; that is not the file this "
             "screen was written against, and a screen over the wrong source "
             "returns an empty candidate list that reads like a clean result."
             % len(source.split("\n")))

# Cohort ids are `col:<frame>.<column>`. Both halves are needed: a bare column
# name would collide across frames, and the fired/silent sets are keyed by id.
fired: set[str] = set()
silent: set[str] = set()
for p in RESULTS:
    d = json.loads(p.read_text(encoding="utf-8"))
    if "dependency_map" in d:                       # B8's merged shape
        fired |= set(d["dependency_map"])
        silent |= set(d.get("silent_cohorts", []))
    for det in d.get("detectors", {}).values():     # B9's merged shape
        fired |= set(det.get("dependency_map", {}))
        silent |= set(det.get("silent_cohorts", []))
silent -= fired                                     # fired anywhere is not silent
print("  results read   : %s" % ", ".join(p.name for p in RESULTS))
print("  cohorts fired  : %d" % len(fired))
print("  cohorts silent : %d (silent in EVERY detector supplied)" % len(silent))
if not fired and not silent:
    sys.exit("HALT: no cohorts were read from the result files. An empty screen "
             "is not an empty finding.")

# A column is REFERENCED if its name appears as a quoted subscript. Quoted forms
# only: a bare word can be anything.
#
# THE RECEIVER AND THE ENCLOSING FUNCTION ARE CAPTURED WITH THE MATCH, because a
# bare column name COLLIDES ACROSS FRAMES and the first version of this screen
# was fooled by exactly that. `col:trades.side` and `col:trades.action` matched
# `df["side"]` and `df["action"]` inside `load_mbo_aggregated` -- a different
# frame entirely, the 8.2M-row MBO parquet the adapter deliberately never
# opens. Reported bare, those two read as `aggressor_side`-class findings. With
# the receiver and the function attached, they read as what they are.
SUBSCRIPT = r'(\w+)\s*\[\s*[\'"]%s[\'"]\s*\]'
DEF = re.compile(r"^\s*def\s+(\w+)")
LINES = source.split("\n")


def enclosing(n: int) -> str:
    for i in range(n - 1, -1, -1):
        m = DEF.match(LINES[i])
        if m:
            return m.group(1)
    return "(module level)"


def referenced(col: str) -> list[dict]:
    """Every quoted subscript of `col`, with its receiver and function."""
    rx = re.compile(SUBSCRIPT % re.escape(col))
    out = []
    for n, line in enumerate(LINES, 1):
        m = rx.search(line)
        if m:
            out.append({"line": n, "receiver": m.group(1),
                        "function": enclosing(n), "text": line.strip()[:86]})
    return out


print()
print("=" * 78)
print("CANDIDATES -- referenced in the builder, moved by no probe")
print("=" * 78)
cands = []
for cid in sorted(silent):
    frame, col = (cid.split(":", 1)[1].split(".", 1) if ":" in cid and "." in cid
                  else ("?", cid))
    hits = referenced(col)
    if hits:
        cands.append({"cohort": cid, "frame": frame, "column": col,
                      "references": hits})

if not cands:
    print("  NONE. Every silent cohort's column is unreferenced in the builder,")
    print("  so every silence has the ordinary reading: the pipeline does not")
    print("  read that column.")
strong = []
for c in cands:
    print("  %s   (frame `%s`)" % (c["cohort"], c["frame"]))
    same_frame = False
    for h in c["references"]:
        # The receiver names the frame at the call site. A receiver equal to the
        # cohort's frame is the same object; anything else is a name collision
        # until someone shows otherwise.
        match = h["receiver"] == c["frame"]
        same_frame |= match
        print("      l.%-4d %-10s in %-22s %s"
              % (h["line"], h["receiver"] + "[..]", h["function"],
                 "<- SAME FRAME" if match else "(different receiver)"))
        print("             %s" % h["text"])
    if same_frame:
        strong.append(c)
        print("      => CANDIDATE. The builder reads THIS frame's column and no")
        print("         perturbation moved the output. Read the predicate.")
    else:
        print("      => name collision: every reference is to another receiver.")
        print("         Not this cohort's dependency. Reported, not counted.")
    print()

print("=" * 78)
print("SUMMARY")
print("=" * 78)
print("  silent cohorts                    : %d" % len(silent))
print("  name matches anywhere in source   : %d" % len(cands))
print("  ...of which SAME-FRAME candidates : %d  <- questions, not verdicts"
      % len(strong))
print("  ...of which name collisions       : %d  <- another frame's column"
      % (len(cands) - len(strong)))
print("  unreferenced                      : %d  <- ordinary silence"
      % (len(silent) - len(cands)))
for c in strong:
    print()
    print("  ** %s -- READ THE PREDICATE." % c["cohort"])
