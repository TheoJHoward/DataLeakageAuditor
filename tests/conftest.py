"""Root conftest: the suite records which tree it ran on. R267 §1.1, R272 §2(g).

The logic lives in `tools/suite_tree.py` so it is testable on its own; this file
is the hook and nothing else. It never raises into the session -- a failed write
leaves no record, and a missing record is what `tools/suite_tree.py` and the
commit route refuse on. Turning it into a test failure would make an unrelated
suite red for a bookkeeping problem.

The session is timed here, so the record carries the runner's own wall time.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

import pathlib
import sys
import time

_ROOT = pathlib.Path(__file__).resolve().parents[1]
for _p in (str(_ROOT), str(_ROOT / "tools")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_STARTED = {}


def pytest_sessionstart(session):
    _STARTED["t"] = time.time()


def pytest_sessionfinish(session, exitstatus):
    try:
        import suite_tree

        counts = {}
        rep = getattr(session.config, "_lastreport_counts", None)
        if rep:
            counts = rep
        else:
            tr = session.config.pluginmanager.getplugin("terminalreporter")
            if tr is not None:
                counts = {k: len(v) for k, v in sorted(tr.stats.items())
                          if k in ("passed", "failed", "error", "skipped",
                                   "xfailed", "xpassed")}
        wall = (round(time.time() - _STARTED["t"], 1)
                if "t" in _STARTED else None)
        suite_tree.record(list(session.config.args), exitstatus, counts,
                          wall_seconds=wall)
    except Exception:                                        # noqa: BLE001
        pass
