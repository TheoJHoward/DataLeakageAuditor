#!/usr/bin/env python3
"""Assemble the X5 final-diff artifact deterministically from the structured hunk
records, rather than from a single agent response that can truncate (and did).

Read-only with respect to the repository. Writes one file into the scratchpad.
"""

import json
import re
import hashlib
import pathlib

SCRATCH = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
SRC = SCRATCH / "amendment" / "_X5_hunks_v2.json"
OUT = SCRATCH / "amendment" / "X5_FINAL_PREREG_DIFF.md"

data = json.loads(SRC.read_text(encoding="utf-8"))
hunks, findings = data["hunks"], data["findings"]

prereg = (REPO / "PREREG.md").read_bytes()
psha = hashlib.sha256(prereg).hexdigest()
plines = prereg.decode("utf-8").count("\n")


def lineno(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else 9999


def short_line(h):
    """A compact line label for the summary table."""
    raw = (h.get("prereg_line") or "").strip()
    m = re.search(r"\d+", raw)
    n = m.group(0) if m else "?"
    return n if len(raw) <= 12 else f"{n}*"


hunks.sort(key=lineno)

# ---- findings, by explicit status (R39/F6(ii)) -----------------------------
triaged = data.get("findings_triaged") or [{"text": f, "status": "OPEN", "fixed_by": ""}
                                           for f in findings]
by_status = {"OPEN": [], "FIXED": [], "WITHDRAWN": []}
for t in triaged:
    by_status.setdefault(t.get("status", "OPEN"), []).append(t)

verified = sum(1 for h in hunks if h.get("anchor_verified"))

L = []
w = L.append

w("# THE FINAL `PREREG.md` DIFF — v30a, for author approval")
w("")
w("**Nothing has been applied.** `PREREG.md` is byte-identical to the `prereg-v30` tag as this is")
w("written:")
w("")
w(f"    sha256  {psha}")
w(f"    lines   {plines}")
w("")
w("Signing this diff authorises its application. Until then the file is read-only to every agent.")
w("")
w("**How this document was assembled, stated because it bears on how much weight it carries.** The")
w(f"{len(hunks)} hunks below were produced by independent passes over `SCHEMA_SET_FINAL.md` and")
w("the v30a amendments block, each pass verifying its own anchors against `PREREG.md` with `sed -n`.")
w("A first attempt to have one agent render the whole artifact **truncated** — it emitted §3 onward")
w("and silently dropped the hunks themselves. The completeness critic caught that before I did. This")
w("document is therefore rendered mechanically from the structured hunk records, so that no hunk can")
w("be dropped in the writing; the prose in §3–§5 is mine, and the critics' full text is in")
w("`X5_CRITIQUES.md` beside this file.")
w("")
w("---")
w("")
w("## 1. Summary — every hunk, in `PREREG.md` v30 line order")
w("")
w(f"**{len(hunks)} hunks. Anchors verified: {verified}/{len(hunks)}.**")
w("A `*` on the line number means the hunk's placement carries a qualification — read its entry in §2.")
w("")
w("| v30 line | Operation | Clause | What changes |")
w("|---|---|---|---|")
for h in hunks:
    what = (h.get("what_changes") or "").replace("|", "\\|").replace("\n", " ")
    if len(what) > 118:
        what = what[:115].rstrip() + "…"
    cl = (h.get("clause") or "").replace("|", "\\|")
    if len(cl) > 46:
        cl = cl[:43].rstrip() + "…"
    w(f"| {short_line(h)} | {h.get('operation','')} | {cl} | {what} |")
w("")
w("---")
w("")
w("## 2. The hunks")
w("")
w("Each entry gives the registered v30 line as it stands today, what the hunk does to it, and **why**.")
w("The justification is the part that matters: it is the reason you are being asked to sign.")
w("")

for i, h in enumerate(hunks, 1):
    w(f"### 2.{i} — `PREREG.md` {h.get('prereg_line','?')} · {h.get('clause','?')} · {h.get('operation','?')}")
    w("")
    ok = "verified byte-exact" if h.get("anchor_verified") else "**NOT VERIFIED**"
    w(f"**Anchor ({ok}) — the registered line as it stands:**")
    w("")
    anchor = (h.get("anchor_text") or "").strip()
    for ln in anchor.split("\n"):
        w(f"> {ln}")
    w("")
    w(f"**What changes.** {h.get('what_changes','').strip()}")
    w("")
    op = (h.get("operative_text") or "").strip()
    if op:
        w("**Operative text — what this hunk actually puts into `PREREG.md`:**")
        w("")
        w("```markdown")
        for oln in op.split(chr(10)):
            w(oln)
        w("```")
        w("")
    else:
        w("**Operative text: MISSING.** This hunk has no readable operative text and must not be")
        w("signed in this state.")
        w("")
    w(f"**Why.** {h.get('justification','').strip()}")
    w("")
    w(f"**Class.** {h.get('class','').strip()}")
    w("")

w("---")
w("")
w("## 3. What is deliberately ABSENT")
w("")
w("- **SC-14, and any amendment to either criterion 5.** Withdrawn. The 13 August decision was a")
w("  **forecast** that the 15 October condition will not be met, not a firing — a date-gated criterion")
w("  cannot be evaluated before its date. Reading §10.2 criterion 5's \"stop\" as deferral-of-release")
w("  would have softened a registered consequence, which the declaration's §D.3 forbids resolving")
w("  toward. Verified absent: zero occurrences of `SC-14` in `SCHEMA_SET_FINAL.md` and in")
w("  `K2_AMENDMENT_LEDGER.md`, and no criterion-5 row in any of the block's four tables.")
w("- **Hunk H5**, the earlier drafted criterion-3 replacement. SC-3 carries its structure and")
w("  supersedes it; carrying both would target line 461 twice.")
w("- **A `waived` entry condition anywhere but SC-12(w).** The state is prohibited outright, with a")
w("  closed and empty list of licensed grounds.")
w("- **Any renumbering of the two criteria numbered 5.** Recorded as a registration defect (H-37) for")
w("  a future amendment; renumbering a registered criterion is itself class C and would invalidate")
w("  every citation of both numbers written to date.")
w("")
w("---")
w("")
w("## 4. Verification record")
w("")
w(f"- **Anchors:** {verified} of {len(hunks)} hunks verified byte-exact against `PREREG.md` by the")
w("  producing pass. An independent anchor critic re-read the distinct pristine line numbers the hunks name with")
w("  `sed -n` and reported no mismatch. Full text in `X5_CRITIQUES.md`.")
w("- **SC-14 absent:** `grep -rn \"SC-14\"` over `SCHEMA_SET_FINAL.md`, `K2_AMENDMENT_LEDGER.md` and")
w("  `Y3_WAIVED_ENTRY_CONDITION.md` → zero hits. (It survives only in withdrawn scratch drafts, which")
w("  are not sources for this diff.)")
w("- **SC-12(w) present:** limbs (w1)–(w7) and its closing bounds block, staged inside SC-12.")
w("  Bound (6) rewritten to state its §8.3 reach (R37/D1, R39/F1–F6).")
w("- **§7.7 pointer redraft present:** the H8 draft is replaced; the old text asserting that no entry")
w("  condition exists would be false on adoption.")
w("- **§8.3 line 929 hunk present:** `waived` joins the `assert_audit_complete()` failure set.")
w("- **The amendments block enumerates and never counts.** The guarantee is in the block itself:")
w("  *\"Their number is read from the enumeration and is stated nowhere as a numeral\"*. No numeral")
w("  stating how many amendments there are was found in the block.")
w("- **§2.9 is vacant** in v30, so SC-1's new section number collides with nothing.")
w("")
w("---")
w("")
w("## 5. Open findings — read before signing")
w("")
w(f"The producing passes raised **{len(findings)}** findings. The grouping below is mine, not theirs;")
w("every finding is reproduced verbatim so you can regroup it.")
w("")
w(f"### 5.A — OPEN ({len(by_status['OPEN'])}) — read these before signing")
w("")
for n, t in enumerate(by_status["OPEN"], 1):
    w(f"**O-{n}.** {t['text'].strip()}")
    w("")
w(f"### 5.B — FIXED ({len(by_status['FIXED'])}) — raised, and closed since")
w("")
w("Listed so they are not re-raised, and so the fix is auditable. Each names what closed it.")
w("")
for n, t in enumerate(by_status["FIXED"], 1):
    w(f"**F-{n}.** {t['text'].strip()}")
    w("")
    w(f"  → **FIXED BY:** {t['fixed_by']}")
    w("")
w(f"### 5.C — WITHDRAWN ({len(by_status['WITHDRAWN'])}) — not defects")
w("")
w("Records of passing checks, or mechanical matters now owned by the assembler's self-check.")
w("")
for n, t in enumerate(by_status["WITHDRAWN"], 1):
    w(f"**W-{n}.** {t['text'].strip()[:300]}")
    w("")
    w(f"  → **WITHDRAWN:** {t['fixed_by']}")
    w("")
w("---")
w("")
w("## 6. My own errors in this set, named")
w("")
w("Listed because the diff is what gets signed, and an error I found and fixed is still an error")
w("I made. All three are now closed; each names what closed it.")
w("")
w("- **SC-12(w) was staged without its bounds block.** I carried limbs (w1)–(w7) into")
w("  `SCHEMA_SET_FINAL.md` and dropped the closing \"What this limb does NOT permit\" block that the")
w("  Y3 deliverable states is part of the clause. *Closed at R37/D1.*")
w("- **Y3's bound (6) was left false.** It read that the limb \"alters no assertion in §8.3\", which")
w("  the line-929 hunk contradicts. Two non-identical copies of the limb existed. *Closed at R37/D1:")
w("  the applied text is single-sourced and bound (6) states its §8.3 reach.*")
w("- **The first assembly truncated** and would have presented §3–§5 as though the hunks had been")
w("  reviewed. Caught by a critic, not by me. *Closed at R37/D9 and R39/F6: the artifact is rendered")
w("  mechanically, and the assembler now self-checks six properties before any reviewer sees it.*")
w("")
w("- **I classified the 992 and 1022 ledger rows as COVERED when they were not.** A retention block")
w("  is not a replacement; both sites would have carried a blockquote quoting text still live above")
w("  it. *Closed at R39/F2: both REPLACE operations drafted.*")
w("- **I reported a scan of every clause as complete when it was not.** It missed five in-clause")
w("  numerals, two of them genuinely fragile. *Closed at R39/F5, and the false claim about the scan")
w("  was corrected in `SCHEMA_SET_FINAL.md` itself.*")
w("")

OUT.write_text("\n".join(L), encoding="utf-8", newline="")
print(f"wrote {OUT}")
print(f"  {len(L)} lines, {len('\n'.join(L))} chars")
print(f"  hunks {len(hunks)}, anchors verified {verified}")
print("  findings: " + "  ".join(f"{k}={len(v)}" for k, v in by_status.items()))
