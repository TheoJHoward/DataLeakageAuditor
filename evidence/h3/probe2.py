"""Probe 2: (1) how well a verbatim-quote exemption works, (2) calibrate
candidate detectors across every candidate file. Read-only."""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
PREREG = (ROOT / "PREREG.md").read_text(encoding="utf-8")


def norm(s: str) -> str:
    s = s.strip()
    s = re.sub(r"^>+\s*", "", s)
    s = s.replace("**", "").replace("*", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


PREREG_NORM = "\n".join(norm(ln) for ln in PREREG.splitlines())

FILES = ["DESIGN.md", "AVAILABILITY_DECLARATION.md", "README.md",
         "PRIOR_ART_VERIFICATION.md", "DEVIATIONS.md", "PARKING_LOT.md"]

print("### blockquote lines and how many are verbatim PREREG text")
for rel in FILES:
    text = (ROOT / rel).read_text(encoding="utf-8")
    bq = [(i, ln) for i, ln in enumerate(text.splitlines(), 1)
          if ln.lstrip().startswith(">")]
    verbatim = [(i, ln) for i, ln in bq if len(norm(ln)) > 40
                and norm(ln) in PREREG_NORM]
    longish = [(i, ln) for i, ln in bq if len(norm(ln)) > 40]
    print(f"  {rel}: {len(bq)} blockquote lines, {len(longish)} longish, "
          f"{len(verbatim)} verbatim-in-PREREG")

CANDIDATES = {
    "definition_of_term": r"(?i)\b(?:is|are)\s+\*{0,2}(?:hereby\s+)?defined\b|"
                          r"\*\*DEFINITION\b|\bDEFINITION,\s|"
                          r"\b(?:means|shall mean),\s+for\s+(?:the\s+)?purpose",
    "denominator_membership": r"(?i)(?:enter(?:s|ing)?|excluded from|included in|"
                              r"removed from|drops? out of|member of)\s+"
                              r"(?:the\s+|any\s+|every\s+|a\s+)?[\w' ]{0,24}denominator",
    "iff_rule": r"\*\*[A-Z][A-Z _-]{2,}\*\*\s+iff\b|(?<![A-Za-z])iff\s+its\s+",
    "counts_as": r"(?i)\bcounts? as (?:a|an|the)\b|\bis (?:scored|counted) as\b",
    "never_reported": r"(?i)\bnever (?:reported|counted|scored) as\b|"
                      r"\bmay (?:not|never) be (?:reported|published|counted) as\b",
    "denominator_defn": r"(?i)\bdenominator\s+(?:is|=|derives|comprises|consists)",
}

print("\n### candidate detector hit counts per file")
for name, pat in CANDIDATES.items():
    print(f"\n-- {name}")
    rx = re.compile(pat)
    for rel in FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        hits = [(i, ln.strip()) for i, ln in enumerate(text.splitlines(), 1)
                if rx.search(ln)]
        # exclude verbatim-quote lines
        kept = [(i, ln) for i, ln in hits
                if not (ln.lstrip().startswith(">") and norm(ln) in PREREG_NORM)]
        print(f"   {rel}: {len(hits)} raw, {len(kept)} after quote-exemption")
        for i, ln in kept[:6]:
            print(f"      {i}: {ln[:130]!r}")
        if len(kept) > 6:
            print(f"      ... {len(kept)-6} more")
    # also: does it fire inside PREREG itself (sanity: it should)
    print(f"   [PREREG.md self-check: {len(rx.findall(PREREG))} hits]")
