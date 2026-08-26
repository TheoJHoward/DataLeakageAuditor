"""G5(d) probe — does the prereg gate ever look at AVAILABILITY_DECLARATION.md?

Part 1: instrument Path.read_text and run the whole --stage prereg battery,
        recording every file the gate actually opens.
Part 2: apply check_single_source's OWN rule set to AVAILABILITY_DECLARATION.md
        to measure what the scan would find if the file were in scope.
Read-only: opens files, writes nothing into the tree.
"""
import io
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "tree"
sys.path.insert(0, str(ROOT))

import tools.check_registration as cr  # noqa: E402

# ---------------------------------------------------------------- Part 1
opened: list[str] = []
_orig = Path.read_text


def _spy(self, *a, **k):
    try:
        opened.append(str(self.resolve().relative_to(ROOT)).replace("\\", "/"))
    except ValueError:
        opened.append(str(self))
    return _orig(self, *a, **k)


Path.read_text = _spy
try:
    with redirect_stdout(io.StringIO()):
        rc = cr.run_stage("prereg", ROOT)
finally:
    Path.read_text = _orig

print("=== PART 1: files opened during the full --stage prereg run ===")
print(f"(run_stage returned {rc})")
for name in sorted(set(opened)):
    print(f"  opened: {name}   x{opened.count(name)}")
decl_hits = [o for o in opened if "AVAILABILITY_DECLARATION" in o]
print(f"\n  AVAILABILITY_DECLARATION.md opened: {len(decl_hits)} time(s) "
      f"-> {'IN SCOPE' if decl_hits else 'NEVER READ / OUT OF SCOPE'}")

# ---------------------------------------------------------------- Part 2
print("\n=== PART 2: apply check_single_source's own rules to the declaration ===")
decl = ROOT / "AVAILABILITY_DECLARATION.md"
text = decl.read_text(encoding="utf-8")
print(f"declaration size: {len(text)} chars, {len(text.splitlines())} lines")

# check_single_source returns [] for the declaration because it never names it:
print(f"check_single_source(root) findings mentioning the declaration: "
      f"{[f for f in cr.check_single_source(ROOT) if 'AVAIL' in f.file]}")

lines = cr.normative_lines(decl, text)
print(f"normative_lines() yields {len(lines)} scannable lines for the declaration")

would_flag: list[tuple[int, str, str]] = []
for lineno, line in lines:
    for pattern, message in cr._SINGLE_SOURCE_RULES:
        if re.search(pattern, line):
            would_flag.append((lineno, message, line.strip()[:110]))

state_tokens = ("not_applicable", "unsupported", "completed", "incomplete",
                "short_circuited")
for lineno, line in lines:
    hits = [t for t in state_tokens if t in line]
    if len(hits) >= 3:
        would_flag.append((lineno, f"state enumeration ({', '.join(hits)})",
                           line.strip()[:110]))

print(f"\nWOULD-FLAG COUNT if AVAILABILITY_DECLARATION.md were in scope: "
      f"{len(would_flag)}")
by_msg: dict[str, int] = {}
for _ln, msg, _t in would_flag:
    by_msg[msg] = by_msg.get(msg, 0) + 1
for msg, n in sorted(by_msg.items(), key=lambda kv: -kv[1]):
    print(f"  {n:5d}  {msg}")

print("\n--- first 15 would-be findings ---")
for lineno, msg, snippet in would_flag[:15]:
    print(f"  L{lineno}: {msg}\n        {snippet!r}")
