"""Probe 3: final calibration — refined detectors + verbatim-quote exemption.
Read-only."""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
PREREG = (ROOT / "PREREG.md").read_text(encoding="utf-8")


def norm(s: str) -> str:
    s = re.sub(r"^\s*>+\s*", "", s.strip())
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


PREREG_LINES = {norm(ln) for ln in PREREG.splitlines() if len(norm(ln)) >= 40}

# sanity: known verbatim quotes in the declaration
DECL = (ROOT / "AVAILABILITY_DECLARATION.md").read_text(encoding="utf-8").splitlines()
for ln_no in (1024, 1028, 1032, 1533, 1537):
    q = norm(DECL[ln_no - 1])
    print(f"decl:{ln_no} verbatim-in-PREREG={q in PREREG_LINES}  {q[:70]!r}")

_ATTRIB = re.compile(r"(?:defined|specified|owned|governed|resolved|stated)\s+"
                     r"(?:by|in)\s+`?PREREG\.md`?|not restated here|"
                     r"PREREG\.md`?\s*§[\d.]+\s*(?:defines|owns|governs)")

REFINED = {
    "definition_here": (
        r"\*\*DEFINITION\b|\bDEFINITION,\s+declared|\bdefined here\b|"
        r"\b(?:is|are)\s+defined\s+as\s+follows\b|\bwe define\b|"
        r"\b(?:is|are)\s+hereby\s+defined\b|"
        r"\", defined for\b|\bdefined for\b"),
    "iff_rule": r"\*\*[A-Z][A-Z][A-Z _-]*\*\*\s+iff\b",
    "denominator_membership": (
        r"(?:enter(?:s|ing)?|excluded from|included in|removed from|"
        r"member of)\s+(?:the\s+|any\s+|every\s+|a\s+|no\s+)?"
        r"[\w' -]{0,24}denominator"),
    "denominator_defn": r"\bdenominator\s+(?:is|=|derives|comprises|consists|"
                        r"shall be|must be)\b",
    "never_reported": r"\bnever (?:reported|counted|scored) as\b|"
                      r"\b(?:may|can|shall) (?:not|never) be "
                      r"(?:reported|published|counted) as\b",
}

FILES = ["DESIGN.md", "AVAILABILITY_DECLARATION.md", "README.md",
         "PRIOR_ART_VERIFICATION.md", "DEVIATIONS.md", "PARKING_LOT.md"]

print("\n### refined detectors, quote-exempt + attribution-exempt applied")
for name, pat in REFINED.items():
    rx = re.compile(pat)
    print(f"\n-- {name}")
    for rel in FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        kept = []
        for i, ln in enumerate(text.splitlines(), 1):
            if not rx.search(ln):
                continue
            if norm(ln) in PREREG_LINES:
                continue                      # verbatim quotation
            if _ATTRIB.search(ln):
                continue                      # reference, not restatement
            kept.append((i, ln.strip()))
        flag = "  <-- FP RISK" if kept and rel != "AVAILABILITY_DECLARATION.md" else ""
        print(f"   {rel}: {len(kept)}{flag}")
        for i, ln in kept[:8]:
            print(f"      {i}: {ln[:125]!r}")
        if len(kept) > 8:
            print(f"      ... {len(kept)-8} more")
