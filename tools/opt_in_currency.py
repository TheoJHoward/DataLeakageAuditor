"""Is the opt-in fixture tests' recorded result still about the CURRENT code?

WHY THIS EXISTS. Four tests in `tests/phase1/test_fixture_adapter.py` are gated
behind `LEAKAUDIT_FIXTURE=1` for cost -- about five minutes. Two of them are
KNOWN POSITIVES for the adapter's equality claim. Their result therefore has to
be recorded, and the record has to be checkable, or every default suite line
reports four tests as "skipped" with nothing saying whether what they last
attested is still true.

`test_every_opt_in_test_has_a_recorded_result` already checks that a result
EXISTS. It cannot check that the result is CURRENT, and nothing else did either.

THE TRUE HISTORY, AND THE ZERO. **No content-staleness has yet occurred. Both
prior "stale" findings were commit-ancestry FALSE POSITIVES.** The record went
COMMIT-stale twice -- it cited an older commit while every module it attests was
byte-identical to the code then on disk -- and both times that was reported as a
defect, in two consecutive deltas, and believed by both people reading them.

So this check has **zero demonstrated true positives**, and the sentence it would
be easy to write beside it -- "built after the record went stale twice" -- would
record a history that did not happen. Its justification is two things and not the
third:

  IT MAKES THE SUITE LINE SAYABLE. "Passing as of <commit>" is a currency claim,
  and a currency claim with no check behind it is prose nobody verifies, moved
  somewhere more visible. This stands.

  IT WOULD DETECT CONTENT-STALENESS. A capability, stated as one.

  ~~It fixes a defect that has bitten twice.~~ It has not bitten once.

AND THE EPISODE IS EVIDENCE FOR THE COMPARATOR CHOICE, which is the part worth
keeping. R213 ruled against keying currency to commit ancestry on the grounds
that it fires on unrelated changes and gets walked past. Its very first
application turned a twice-reported finding into a twice-made false positive.
The failure mode was not hypothetical; it had already happened and been written
down as fact.

THE COMPARATOR IS CONTENT, NOT COMMIT ANCESTRY, and that choice is the whole
design. R213 §3: a check keyed to "is the attested commit HEAD" goes red on every
unrelated commit, gets overridden within a week, and is then worse than nothing,
because it is a red light everyone has learned to walk past. So the record
attests a DIGEST PER MODULE for the modules the opt-in tests actually execute,
and currency is a digest comparison. It fires when something that could change
the answer changed, and stays quiet otherwise.

WHICH MODULES. Measured with `probe_path_guard.record_modules()` -- the same
instrument that measured the probe's path set, used for a different question.
THE TWO SETS ARE NOT THE SAME AND ARE NOT MERGED: `fixture_adapter.py` and the
fixture's own producing code are in this one and not in the probe's, because the
probe is handed frames and these tests produce them. Two questions, two records,
each with its reason.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
RECORD = REPO / "tests" / "phase1" / "fixture_run_record.json"
ATTESTS = "attests_module_digests"


class OptInRecordError(RuntimeError):
    """The record could not be read. Never a silent 'current'."""


def _digest(rel: str) -> str | None:
    p = REPO / rel
    if not p.is_file():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load() -> dict:
    if not RECORD.exists():
        raise OptInRecordError(
            "%s is missing. It carries the only record of what the opt-in tests "
            "last attested, so its absence is 'nothing is known', not "
            "'everything is fine'." % RECORD)
    try:
        return json.loads(RECORD.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise OptInRecordError("%s could not be read as JSON (%s)" % (RECORD, e))


def latest_run(doc: dict) -> tuple[str, dict]:
    """The newest `run_YYYY_MM_DD` entry. Dated keys sort correctly as strings."""
    keys = sorted(k for k in doc if k.startswith("run_"))
    if not keys:
        raise OptInRecordError(
            "%s carries no `run_*` entry, so no opt-in result has been recorded "
            "in the dated form this check reads." % RECORD)
    return keys[-1], doc[keys[-1]]


def status() -> dict:
    """current | stale | unattested, with the modules that moved named."""
    doc = load()
    key, run = latest_run(doc)
    attested = run.get(ATTESTS)
    if not attested:
        return {
            "state": "unattested",
            "run": key,
            "detail": (
                "the newest recorded run carries no %r block, so there is "
                "nothing to compare against. Re-run the opt-in tests with "
                "`python tools/opt_in_currency.py --measure` to record one."
                % ATTESTS),
            "moved": [], "gone": [],
        }
    moved, gone = [], []
    for rel, want in sorted(attested.items()):
        have = _digest(rel)
        if have is None:
            gone.append(rel)
        elif have != want:
            moved.append(rel)
    return {
        "state": "current" if not (moved or gone) else "stale",
        "run": key,
        "commit": run.get("commit", "?"),
        "date": run.get("date", "?"),
        "n_modules": len(attested),
        "moved": moved,
        "gone": gone,
        "detail": "",
    }


def suite_line() -> str:
    """The line a report may quote in place of `4 skipped`.

    R213 §3: `4 skipped` is wrong and `4 deferred (opt-in), passing as of
    <commit>` is right -- and that sentence is unsayable without this check,
    because "passing as of" is a currency claim.
    """
    s = status()
    n = 4
    if s["state"] == "current":
        return ("%d deferred (opt-in), passing as of %s (%s); the %d modules "
                "they attest are unchanged since"
                % (n, s["commit"], s["date"], s["n_modules"]))
    if s["state"] == "stale":
        what = ", ".join(s["moved"] + ["%s (gone)" % g for g in s["gone"]])
        return ("%d deferred (opt-in), and their recorded result is STALE: %s "
                "changed since %s. Re-run them before believing any clean "
                "result that rests on them." % (n, what, s["commit"]))
    return "%d deferred (opt-in), currency UNATTESTED: %s" % (n, s["detail"])


def measure_and_record(run_key: str) -> list[str]:
    """Run the opt-in tests IN-PROCESS under the recorder and write the digests.

    In-process on purpose: `sys.setprofile` sees this interpreter's frames, so a
    subprocess would record nothing and the block would be silently empty. That
    is the failure this function is shaped to avoid rather than to have.
    """
    import os

    import pytest

    sys.path.insert(0, str(REPO / "tools"))
    import probe_path_guard as ppg

    os.environ["LEAKAUDIT_FIXTURE"] = "1"

    # WARM THE IMPORTS FIRST. A module's top level runs on first import, so a
    # recorder started cold reports every module the package pulls in rather
    # than the ones these tests reach -- fifteen instead of the handful that
    # matter. A population that is too large makes the check that reads it
    # weaker while looking more thorough.
    sys.path.insert(0, str(REPO / "src"))
    sys.path.insert(0, str(REPO))
    import leakaudit                                    # noqa: F401
    import leakaudit.determinism                        # noqa: F401
    import leakaudit.fixture_adapter                    # noqa: F401
    import tests.phase1.test_fixture_adapter            # noqa: F401

    with ppg.record_modules() as seen:
        rc = pytest.main(["-q", str(REPO / "tests" / "phase1"
                                    / "test_fixture_adapter.py")])
    if rc != 0:
        raise SystemExit("the opt-in tests did not pass (rc=%s); "
                         "nothing recorded" % rc)
    if not seen:
        raise SystemExit(
            "the recorder saw no modules of this repository, which cannot be "
            "true if the tests ran. Refusing to write an empty attestation.")

    doc = load()
    if run_key not in doc:
        raise SystemExit("%s has no %r entry to attach digests to"
                         % (RECORD, run_key))
    digests = {}
    for rel in sorted(seen):
        d = _digest(rel)
        if d is not None:
            digests[rel] = d
    doc[run_key][ATTESTS] = digests
    doc[run_key]["attests_method"] = (
        "sha256 per module, over the modules these tests EXECUTED, measured "
        "in-process with probe_path_guard.record_modules(). Currency is a digest "
        "comparison, not commit ancestry: it fires when something that could "
        "change the answer changed, and stays quiet otherwise.")
    RECORD.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8", newline="")
    return sorted(digests)


if __name__ == "__main__":                                  # pragma: no cover
    if "--measure" in sys.argv:
        key = sys.argv[sys.argv.index("--measure") + 1]
        mods = measure_and_record(key)
        print("recorded %d module digests under %s:" % (len(mods), key))
        for m in mods:
            print("   %s" % m)
        raise SystemExit(0)
    s = status()
    print(json.dumps(s, indent=2))
    print()
    print(suite_line())
    raise SystemExit(0 if s["state"] == "current" else 1)
