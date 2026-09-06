#!/usr/bin/env python3
"""Append one disclosure to `DEVIATIONS.md`. Append-only, and it checks that.

    $ py -3.12 tools/append_disclosure.py <body.md>

**WHY THIS FILE EXISTS IN `tools/` AND NOT IN A SCRATCH DIRECTORY.**
`OPERATING_RULES.md` §2 has said since R178 that `DEVIATIONS.md` is append-only
*"via the disclosure applier"* — and the applier was rebuilt in session scratch
every round and committed in none of them. `git log --all -- tools/` lists nine
files and this was not one. So the rule named an enforcement mechanism that did
not exist in the repository, and every append ran through a script nobody else
could re-run or inspect.

That is the class D-V30A-60 recorded for `15dc83c7…` and the one R231 acted on
when it moved `wholeframe_guard.py` out of scratch: **an assertion that lives in
a file that can vanish is an assertion nobody can re-run.** The applier is a
stronger case than the guard, because a guard that vanishes stops producing
evidence while an applier that vanishes stops enforcing a rule that is still
being cited.

WHAT IT CHECKS, and each is a thing that has gone wrong somewhere in this
project rather than a thing that might:

  APPEND-ONLY, VERIFIED BY BYTES. The prior content has to survive as an exact
  prefix. Not "the tool only appends" as a property of how it was written --
  compared, so a mistake here fails rather than being trusted.

  THE NUMBER IS THE SUCCESSOR. A disclosure reusing or skipping a number breaks
  the ledger silently; the next number is computed from the file, never passed
  in, because a hand-typed figure beside a derivable one is the class
  `HAND_TYPED_FIGURES.md` was opened for.

  NO RULE-SHAPED SENTENCE IN THE BODY. A disclosure records WHAT HAPPENED. A
  sentence saying what one "must" or "should" do is a rule, and a rule created
  in `DEVIATIONS.md` is a rule outside `OPERATING_RULES.md` -- a second place
  where the rule set lives, which is the two-lists hazard applied to the rules
  themselves. HALTS rather than rewrites: the wording is the author's.

  LINE ENDINGS UNCHANGED. Delegated to `safe_edit.edit`, per R220.

IT DOES NOT COMMIT. Writing and committing are different acts and the second is
`safe_edit.commit`'s, which takes a message from a file on disk.
"""
from __future__ import annotations

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import safe_edit as se  # noqa: E402

REPO = HERE.parent
DEVIATIONS = REPO / "DEVIATIONS.md"

HEADING = re.compile(r"^## (D-V30A-(\d+)) — (.+)$", re.M)

#: Words that make a sentence a rule rather than a record. The list is short and
#: deliberately blunt: a check that tried to tell a real rule from a quoted one
#: would be a judgment, and a judgment that halts is worse than a blunt one that
#: halts, because it is harder to argue with.
RULE_WORDS = ("must", "should", "shall", "never do", "always do")


class DisclosureRefused(Exception):
    """The append was refused. The file is untouched."""


def next_number(text: str) -> int:
    """One past the highest heading in the file. DERIVED, never supplied."""
    nums = [int(m.group(2)) for m in HEADING.finditer(text)]
    if not nums:
        raise DisclosureRefused(
            "no `## D-V30A-N` heading was found, so the successor cannot be "
            "derived. Refused rather than starting at 1 against a file that "
            "plainly has content: a wrong guess here renumbers the ledger.")
    return max(nums) + 1


def check_body(body: str) -> None:
    """The body is a record, not a rule."""
    if not body.strip():
        raise DisclosureRefused("the body is empty")
    heads = HEADING.findall(body)
    if len(heads) != 1:
        raise DisclosureRefused(
            "the body carries %d `## D-V30A-N —` headings; exactly one is "
            "expected, and it is what the number check reads." % len(heads))
    low = body.lower()
    hits = sorted({w for w in RULE_WORDS if re.search(r"\b%s\b" % w, low)})
    if hits:
        raise DisclosureRefused(
            "HALT. The body contains rule-shaped word(s) %s.\n"
            "A disclosure records WHAT HAPPENED. A sentence saying what one "
            "%s do is a rule, and a rule written here is a rule outside "
            "`OPERATING_RULES.md` -- a second place the rule set lives, which "
            "is the hazard this project keeps finding in its own documents.\n"
            "Reword it as a record of what was done, or put the rule where "
            "rules go. NOT REWRITTEN AUTOMATICALLY: the wording is yours."
            % (", ".join(repr(h) for h in hits), hits[0]))


def append(body: str, path: pathlib.Path = DEVIATIONS) -> str:
    """Append `body`, or refuse. Returns the heading that was written."""
    check_body(body)
    before = path.read_text(encoding="utf-8")
    tag, num, _ = HEADING.search(body).groups()
    want = next_number(before)
    if int(num) != want:
        raise DisclosureRefused(
            "the body is numbered %s and the next number in %s is "
            "D-V30A-%d. Refused: a reused number overwrites a record in the "
            "reader's mind and a skipped one reads as a deleted disclosure."
            % (tag, path.name, want))
    if ("## %s " % tag) in before:
        raise DisclosureRefused("%s is already in %s" % (tag, path.name))

    chunk = ("\n" if not before.endswith("\n") else "") + "\n" + body.strip() + "\n"

    def transform(text: str) -> str:
        return text + chunk

    se.edit(path, transform)

    after = path.read_text(encoding="utf-8")
    # APPEND-ONLY, COMPARED RATHER THAN ASSUMED.
    if not after.startswith(before):
        raise DisclosureRefused(
            "the prior content of %s is not a prefix of the result. The append "
            "modified existing text and that is the one thing this exists to "
            "prevent." % path.name)
    return tag


def main(argv: list) -> int:
    if len(argv) != 1:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    body = pathlib.Path(argv[0]).read_text(encoding="utf-8")
    try:
        tag = append(body)
    except DisclosureRefused as e:
        print("REFUSED: %s" % e)
        return 1
    print("appended %s to %s" % (tag, DEVIATIONS.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
