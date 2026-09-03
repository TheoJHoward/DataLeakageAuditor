"""Put `src/` and the repository root on the path for the Phase 1 suite.

Phase 1 tests live here and NOT in `tests/registration/`, which is a registered
object: `PREREG.md` §11 item 1 names `tests/registration/` and item 8 puts every
file item 1 names into the tag's hash enumeration. Adding a file there would
change what the tag attests.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in (ROOT, ROOT / "src", ROOT / "tools"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Say what the four skips ARE, in the summary where the count is read.

    `4 skipped` puts a cost-deferred test that passes and a genuinely
    inapplicable one in the same word, one shade from displayed-as-a-pass --
    which is the display problem `PREREG.md` §8.2 exists to prevent, one level
    above where §8.2 was written. §8.2 is registered vocabulary in a closed
    registration and is NOT amended for this; the suite is a tool artifact and
    may use tool-level wording, exactly as R203 settled for config keys.

    The currency half is why this line can be written at all. "Passing as of
    <commit>" is a claim about whether the recorded result still describes the
    code on disk, and a summary line asserting that without a check behind it is
    prose nobody verifies -- the defect being fixed, moved somewhere more
    visible. `tools/opt_in_currency.py` is the check; this only prints it.
    """
    skipped = terminalreporter.stats.get("skipped", [])
    if not any("test_fixture_adapter" in str(getattr(r, "nodeid", ""))
               for r in skipped):
        return
    try:
        import opt_in_currency as oic
        line = oic.suite_line()
    except Exception as e:                                       # noqa: BLE001
        line = ("opt-in fixture tests deferred; their currency could NOT be "
                "determined (%s: %s). That is not the same as current."
                % (type(e).__name__, e))
    terminalreporter.write_sep("-", "opt-in fixture tests")
    terminalreporter.write_line(line)
