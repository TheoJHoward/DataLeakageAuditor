"""Probe 4: final patterns + substring quote exemption. Read-only."""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
PREREG = (ROOT / "PREREG.md").read_text(encoding="utf-8")


def norm(s: str) -> str:
    s = re.sub(r"^\s*>+\s*", "", s.strip())
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


PREREG_BLOB = " ".join(norm(ln) for ln in PREREG.splitlines())

NEW = {
    "definition_here": r"\*\*DEFINITION\b|\bDEFINITION,\s+declared\b|"
                       r"\bdefined here\b|\b(?:is|are)\s+defined\s+as\s+follows\b|"
                       r"\bwe define\b|\b(?:is|are)\s+hereby\s+defined\b",
    "iff_rule": r"\*\*[A-Z][A-Z][A-Z _-]*\*\*\s+iff\b",
    "denominator_membership": r"(?:enter(?:s|ing)?|excluded from|included in|"
                              r"removed from|member of)\s+"
                              r"(?:the\s+|any\s+|every\s+|a\s+|no\s+)?"
                              r"[\w' -]{0,24}denominator",
    "denominator_constitution": r"\bdenominator\s+(?:derives|comprises|consists|"
                                r"is constituted|is drawn|is the set)\b",
    "never_reported": r"\bnever (?:reported|counted|scored) as\b|"
                      r"\b(?:may|can|shall) (?:not|never) be "
                      r"(?:reported|published|counted) as\b",
}

_ATTRIB = re.compile(r"(?:defined|specified|owned|governed|resolved|stated)\s+"
                     r"(?:by|in)\s+`?PREREG\.md`?|not restated here")

FILES = ["DESIGN.md", "AVAILABILITY_DECLARATION.md", "README.md",
         "PRIOR_ART_VERIFICATION.md", "DEVIATIONS.md", "PARKING_LOT.md",
         "HISTORY.md"]

total = 0
for rel in FILES:
    text = (ROOT / rel).read_text(encoding="utf-8")
    per = []
    for i, ln in enumerate(text.splitlines(), 1):
        n = norm(ln)
        if len(n) >= 40 and n in PREREG_BLOB:
            continue
        if _ATTRIB.search(ln):
            continue
        for name, pat in NEW.items():
            if re.search(pat, ln):
                per.append((i, name, ln.strip()))
    print(f"\n== {rel}: {len(per)}")
    for i, name, ln in per:
        print(f"   {i} [{name}] {ln[:118]!r}")
    if rel != "HISTORY.md":
        total += len(per)
print(f"\nTOTAL (excl HISTORY): {total}")

# how many lines does the substring exemption clear, and could it over-clear?
decl = (ROOT / "AVAILABILITY_DECLARATION.md").read_text(encoding="utf-8")
cleared = [ln for ln in decl.splitlines()
           if len(norm(ln)) >= 40 and norm(ln) in PREREG_BLOB]
print(f"\nquote-exemption clears {len(cleared)} declaration lines (>=40 norm chars)")
