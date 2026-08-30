"""Put `src/` and the repository root on the path for the Phase 1 suite.

Phase 1 tests live here and NOT in `tests/registration/`, which is a registered
object: `PREREG.md` §11 item 1 names `tests/registration/` and item 8 puts every
file item 1 names into the tag's hash enumeration. Adding a file there would
change what the tag attests.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in (ROOT, ROOT / "src"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
