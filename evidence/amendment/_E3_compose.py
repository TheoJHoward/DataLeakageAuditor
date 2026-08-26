#!/usr/bin/env python3
"""DELTA R38 / E3 — compose the amended sections into a scratch PREREG.md.

Applies the corrected hunks that land in sections 6.2, 7.7, 8.3, 10.1 and 10.2 to a
SCRATCH copy, so an independent reader can read the RESULT as a whole rather than as
a pile of hunks. The repository's PREREG.md is opened READ-ONLY and never written.

Operative text is extracted from the sources, never invented:
  SC-n         -> the blockquote following "**THE CLAUSE.**" in SCHEMA_SET_FINAL.md
  SC-n INSERT  -> the blockquote following an "**INSERTION TEXT" heading
  H2/H3/H4     -> the fenced block following "**REPLACE with" in PREREG_v30a_DIFF.md
  C2           -> the fenced block in K2_AMENDMENT_LEDGER.md section 9.2

Anything that cannot be extracted is emitted as an explicit
[[UNEXTRACTED: ...]] marker so the reader is never shown a silent gap.
"""

import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
OUT = D / "_E3_composed_sections.md"

prereg = (REPO / "PREREG.md").read_text(encoding="utf-8").split("\n")
ssf = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8")
dd = (D / "PREREG_v30a_DIFF.md").read_text(encoding="utf-8")
k2 = (D / "K2_AMENDMENT_LEDGER.md").read_text(encoding="utf-8")


def blockquote_after(text, marker, start=0):
    """The blockquote immediately following `marker`."""
    i = text.find(marker, start)
    if i < 0:
        return None
    lines = text[i:].split("\n")
    out, started = [], False
    for ln in lines[1:]:
        if ln.startswith(">"):
            started = True
            out.append(re.sub(r"^>\s?", "", ln))
        elif started and ln.strip() == "":
            out.append("")
        elif started:
            break
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) if out else None


def clause_of(tag):
    """THE CLAUSE blockquote for a given SC-n heading."""
    m = re.search(rf"^### {re.escape(tag)} — ", ssf, re.M)
    if not m:
        return None
    return blockquote_after(ssf, "**THE CLAUSE.**", m.start())


def fenced_after(text, marker, start=0):
    i = text.find(marker, start)
    if i < 0:
        return None
    seg = text[i:]
    f = seg.find("```")
    if f < 0:
        return None
    end = seg.find("```", f + 3)
    return seg[f + 3:end].strip("\n") if end > 0 else None


# ---- gather operative text -------------------------------------------------
OPS = {}
for tag in ("SC-2", "SC-3", "SC-4", "SC-5", "SC-6", "SC-7", "SC-8",
            "SC-12", "SC-13a", "SC-13b", "SC-13c"):
    OPS[tag] = clause_of(tag)

for label, marker, src in (("H2", "### H2 — ", dd), ("H3", "### H3 — ", dd), ("H4", "### H4 — ", dd)):
    i = src.find(marker)
    OPS[label] = fenced_after(src, "**REPLACE with", i) if i >= 0 else None

OPS["C2"] = fenced_after(k2, "**9.2 — C2 (line 1022).**")
OPS["PTR77"] = ("**`waived` is defined in §10.2 (v30a).** That definition governs the word wherever "
                "it appears, including this table, and **SC-12(w) registers the condition under "
                "which a detector-case may be reported in this state.** Neither is restated here.")
OPS["A83"] = ("- **`assert_audit_complete()`** — fails on any `unsupported`, `could_not_run`, or "
              "**`waived`** **detector-case** entry, including a mode whose exact comparison was "
              "unavailable (§6.10). Ignores findings. *(`waived` added v30a, carried with SC-12(w), "
              "whose (w1) prohibits the state outright; the assertion is what makes that prohibition "
              "checkable rather than merely stated.)*")
OPS["SC-12w"] = blockquote_after(ssf, "> **(w) ENTRY CONDITION FOR §7.7's `waived` COVERAGE STATE")
if OPS["SC-12w"] is None:
    i = ssf.find("**(w) ENTRY CONDITION FOR")
    if i >= 0:
        seg = ssf[i - 2:].split("\n")
        out = []
        for ln in seg:
            if ln.startswith(">"):
                out.append(re.sub(r"^>\s?", "", ln))
            elif out and ln.strip() == "":
                out.append("")
            elif out:
                break
        OPS["SC-12w"] = "\n".join(out).strip()

print("extracted operative text:")
for k, v in OPS.items():
    print(f"  {k:<8} {'OK  ' + str(len(v)) + ' chars' if v else '*** MISSING ***'}")

# ---- the edit plan, per section --------------------------------------------
# (line, kind, key, note)   kind: replace | insert_after
PLAN = [
    (445, "replace", "H2", "§6.2 reference AUC anchor"),
    (450, "replace", "H3", "§6.2 contamination availability class"),
    (451, "replace", "H4", "§6.2 sliced variant"),
    (451, "insert_after", "SC-2", "§6.2 fixture composition (lands AFTER H4's block)"),
    (461, "replace", "SC-3", "§6.2 acceptance criterion 3"),
    (464, "insert_after", "SC-4", "§6.2 criterion-1 denominator and partition"),
    (464, "insert_after", "SC-5", "§6.2 adjudication routing (follows SC-4)"),
    (468, "insert_after", "SC-7", "§6.2 gate input surface"),
    (480, "insert_after", "SC-8", "§6.2 the freeze"),
    (856, "insert_after", "SC-6", "§7.7 unscored coverage state"),
    (856, "insert_after", "PTR77", "§7.7 pointer, redrafted"),
    (929, "replace", "A83", "§8.3 assert_audit_complete failure set"),
    (1022, "insert_after", "C2", "§10.1 criterion-3 retention block"),
    (1030, "replace", "SC-13a", "§10.2 criterion 2, ambiguity branch"),
    (1035, "insert_after", "SC-12", "§10.2 'waived' defined"),
    (1035, "insert_after", "SC-12w", "§10.2 SC-12(w) entry condition (inside SC-12)"),
    (1035, "insert_after", "SC-13b", "§10.2 admissibility (follows SC-12)"),
    (1036, "insert_after", "SC-13c", "§10.2 interactions"),
]

SECTIONS = [("6.2", 443, 481), ("7.7", 849, 856), ("8.3", 917, 932),
            ("10.1", 1016, 1027), ("10.2", 1028, 1043)]

L = []
w = L.append
w("# COMPOSED SECTIONS — `PREREG.md` AS v30a WOULD LEAVE IT")
w("")
w("**This is a SCRATCH composition for an adversarial read. It is not `PREREG.md`, and nothing")
w("has been applied to `PREREG.md`, which remains byte-identical to the `prereg-v30` tag.**")
w("")
w("Registered v30 text is shown as-is. Text v30a inserts or substitutes is marked **[v30a]**.")
w("Read each section as a finished whole, not as a base plus a patch.")
w("")
for name, a, b in SECTIONS:
    w("")
    w("---")
    w("")
    w(f"# §{name} — as composed")
    w("")
    for n in range(a, b + 1):
        reps = [p for p in PLAN if p[0] == n and p[1] == "replace"]
        if reps:
            key = reps[0][2]
            w(f"**[v30a REPLACES registered line {n}]**")
            w("")
            w(OPS.get(key) or f"[[UNEXTRACTED: {key} — operative text not extractable]]")
            w("")
        else:
            w(prereg[n - 1])
        for p in [p for p in PLAN if p[0] == n and p[1] == "insert_after"]:
            w("")
            w(f"**[v30a INSERTS here — {p[3]}]**")
            w("")
            w(OPS.get(p[2]) or f"[[UNEXTRACTED: {p[2]} — operative text not extractable]]")
            w("")

OUT.write_text("\n".join(L), encoding="utf-8", newline="")
txt = OUT.read_text(encoding="utf-8")
print(f"\nwrote {OUT.name}: {txt.count(chr(10))} lines, {len(txt)} chars")
print(f"  unextracted markers: {txt.count('[[UNEXTRACTED')}")
