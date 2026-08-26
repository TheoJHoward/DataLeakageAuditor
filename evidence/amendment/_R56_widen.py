#!/usr/bin/env python3
"""Widen the completion-claim patterns to span sentences. DELTA R56/B2."""
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
p = D / "_completion_claims.py"
L = p.read_text(encoding="utf-8").split("\n")

start = next(i for i, x in enumerate(L) if x.startswith("CLAIM_PATTERNS = ["))
end = next(i for i in range(start, len(L)) if L[i].rstrip() == "]")

Q = '[\\"\\u201c]'
QE = '[\\"\\u201d]'
NEW = [
    "# The gap between the quotation and the completion marker must allow SENTENCES, not",
    "# merely clauses. The first draft required them within 120 chars with no intervening",
    "# period, and MISSED the instance it was written for. The real commentary reads:",
    '#     ... also said "the anchor\'s model family changed", relying on A.1 item 2. That',
    "#     claim was FALSE against its own cited source ... and is struck from both.",
    "# - two sentences apart. Mutation testing found that; reading the regex did not. H-L16.",
    '_DONE = (r"(?:is|was|has been)\\s+(?:struck|removed|corrected|withdrawn)"',
    '         r"|stood here until|no longer (?:appears|stands)")',
    "CLAIM_PATTERNS = [",
    '    re.compile(r"previously read[:,]?\\s*" + ' + repr(Q) + ' + r"(.{12,400}?)" + ' + repr(QE) + ", re.S),",
    '    re.compile(' + repr(Q) + ' + r"(.{12,400}?)" + ' + repr(QE) + ' + r".{0,400}?(?:" + _DONE + r")", re.S),',
    '    re.compile(r"(?:" + _DONE + r").{0,400}?" + ' + repr(Q) + ' + r"(.{12,400}?)" + ' + repr(QE) + ", re.S),",
    "]",
]
L[start:end + 1] = NEW
p.write_text("\n".join(L), encoding="utf-8")
print("patterns widened; compiling to verify")
import importlib.util
spec = importlib.util.spec_from_file_location("cc", str(p))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print("compiled OK; %d claim patterns" % len(m.CLAIM_PATTERNS))
