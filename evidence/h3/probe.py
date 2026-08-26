"""Probe: run the EXISTING single-source detectors against every candidate
markdown file, read-only. No file in the repo is modified."""
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
sys.path.insert(0, str(ROOT))
import tools.check_registration as cr  # noqa: E402

CANDIDATES = [
    "DESIGN.md", "AVAILABILITY_DECLARATION.md", "README.md",
    "PRIOR_ART_VERIFICATION.md", "DEVIATIONS.md", "PARKING_LOT.md",
    "HISTORY.md", "tests/registration/EXPECTED_OUTPUTS.md",
]
CANDIDATES += [str(p.relative_to(ROOT)).replace("\\", "/")
               for p in sorted((ROOT / "evidence").rglob("*.md"))]

STATE_TOKENS = ("not_applicable", "unsupported", "completed", "incomplete",
                "short_circuited")

for rel in CANDIDATES:
    path = ROOT / rel
    if not path.exists():
        print(f"{rel}: MISSING")
        continue
    text = path.read_text(encoding="utf-8")
    hits = []
    for lineno, line in cr.normative_lines(path, text):
        for pattern, message in cr._SINGLE_SOURCE_RULES:
            if re.search(pattern, line):
                hits.append((lineno, message, line.strip()[:120]))
        st = [t for t in STATE_TOKENS if t in line]
        if len(st) >= 3:
            hits.append((lineno, f"state enumeration ({', '.join(st)})",
                         line.strip()[:120]))
    print(f"\n===== {rel}: {len(hits)} hit(s) =====")
    for lineno, msg, snippet in hits[:25]:
        print(f"  {lineno}: {msg}\n      {snippet!r}")
    if len(hits) > 25:
        print(f"  ... {len(hits) - 25} more")
