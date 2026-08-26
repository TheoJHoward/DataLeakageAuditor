#!/usr/bin/env python3
"""DELTA R45 / M1 — rebuild the hunk JSON FROM the manifest.

Direction of authority: manifest -> JSON -> artifact. The manifest's section A table is
read as the specification; every claimed entry's text is extracted from source at its
stated anchor; each hunk's operative_text is rebuilt as the ordered concatenation of the
entries that claim it. The previous JSON is NEVER consulted for text that has a source -
it is displaced, and consulting it is what the direction of authority forbids.

Section B hunks draw from other files; those are re-extracted from their named sources
too. Only two hunks have no file source - H29 and H32, drafted directly at R39/F2 - and
they are the sole values carried over.

SEPARATOR RULE (R44/L2): a bare '>' line between two markers belongs to the entry ABOVE.
The manifest's ranges already encode this; the extractor honours the ranges as written.
"""

import json
import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

SSF = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8").split("\n")
K2 = (D / "K2_AMENDMENT_LEDGER.md").read_text(encoding="utf-8")
DD = (D / "PREREG_v30a_DIFF.md").read_text(encoding="utf-8")

data = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))
hunks = data["hunks"]


def ln(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else 9999


# H-numbering: hunks sorted by first line number, 1-based - the manifest's convention.
ordered = sorted(hunks, key=ln)
HN = {f"H{i}": h for i, h in enumerate(ordered, 1)}
print(f"hunks: {len(ordered)}  (H1..H{len(ordered)})")


def block_text(a, b):
    """Source lines a..b inclusive, quote markers stripped, fences dropped."""
    out = []
    for raw in SSF[a - 1:b]:
        if raw.startswith("```"):
            continue
        out.append(re.sub(r"^>\s?", "", raw) if raw.startswith(">") else raw)
    return "\n".join(out).strip()


# ---- parse the manifest's section A table ---------------------------------
man = (D / "BLOCK_MANIFEST.md").read_text(encoding="utf-8")
secA = man[man.index("## §A —"):man.index("## §B —")]
ROW = re.compile(r"^\|\s*(\S+?)\s*\|\s*(\d+)(?:[–-](\d+))?\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")
entries = []
for line in secA.split("\n"):
    m = ROW.match(line)
    if not m:
        continue
    eid, a, b, desc, target = m.groups()
    if eid in ("#",) or set(eid) <= set("-"):
        continue
    entries.append({"id": eid, "a": int(a), "b": int(b or a),
                    "desc": desc, "target": target})
print(f"manifest section A rows parsed: {len(entries)}")

claimed, apparatus = [], []
for e in entries:
    hm = re.search(r"\*\*(H\d+)\*\*", e["target"])
    (claimed if hm else apparatus).append(e)
    e["hunk"] = hm.group(1) if hm else None
print(f"  claimed: {len(claimed)}   apparatus: {len(apparatus)}")
assert len(entries) == 42, f"expected 42 entries, parsed {len(entries)}"
assert len(claimed) == 36, f"expected 36 claimed, got {len(claimed)}"
assert len(apparatus) == 6, f"expected 6 apparatus, got {len(apparatus)}"

# ---- section B sources, re-extracted --------------------------------------
def fenced_after(text, marker):
    i = text.find(marker)
    if i < 0:
        return None
    seg = text[i:]
    f = seg.find("```")
    if f < 0:
        return None
    e = seg.find("```", f + 3)
    return seg[f + 3:e].strip("\n") if e > 0 else None


def diff_replace(label):
    i = DD.find(f"### {label} — ")
    return fenced_after(DD[i:], "**REPLACE with") if i >= 0 else None


SECTION_B = {
    "H1": fenced_after(K2, "### 8.1 The status line"),
    "H2": K2[K2.index("<!-- K2-BLOCK-BEGIN -->") + 23:K2.index("<!-- K2-BLOCK-END -->")].strip(),
    "H10": diff_replace("H2"),
    "H11": diff_replace("H3"),
    "H13": diff_replace("H4"),
    "H23": ("**`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it "
            "appears, including this table, and **SC-12(w) registers the condition under which a "
            "detector-case may be reported in this state.** Neither is restated here."),
    "H30": fenced_after(K2, "**9.1 — C1 (line 992).**"),
    "H31": fenced_after(K2, "**9.2 — C2 (line 1022).**"),
}
CARRY = {"H29", "H32"}   # drafted at R39/F2; no file source
for k, v in SECTION_B.items():
    print(f"  §B {k:<4} {'OK ' + str(len(v)) + 'c' if v else '*** MISSING ***'}")

# ---- rebuild ---------------------------------------------------------------
byhunk = {}
for e in claimed:
    byhunk.setdefault(e["hunk"], []).append(e)

rebuilt = 0
for key, h in HN.items():
    parts = []
    if key in SECTION_B and SECTION_B[key]:
        parts.append(SECTION_B[key])
    for e in byhunk.get(key, []):
        parts.append(block_text(e["a"], e["b"]))
    if key in CARRY and not parts:
        continue                      # keep the delta-drafted text as-is
    if not parts:
        h["operative_text"] = ""
        h["manifest_entries"] = []
        continue
    h["operative_text"] = "\n\n".join(parts)
    h["manifest_entries"] = [e["id"] for e in byhunk.get(key, [])]
    rebuilt += 1

print(f"\nhunks rebuilt from the manifest: {rebuilt}")
json.dump(data, open(D / "_X5_hunks_v2.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("wrote _X5_hunks_v2.json")

# ---- M4 / M5 verification --------------------------------------------------
print("\n" + "=" * 74)
print("M4 / M5 VERIFICATION")
print("=" * 74)
fail = 0

h20 = HN["H20"]
ok20 = bool((h20.get("operative_text") or "").strip()) and "suppression clause above" in (h20.get("operative_text") or "")
print(f"  M4  H20 non-empty and renders the §13c-P pointer : {'PASS' if ok20 else '*** FAIL ***'}"
      f"   ({len(h20.get('operative_text') or '')} chars)")
fail += 0 if ok20 else 1

for a, b in (("H3", "H37"), ("H22", "H26")):
    ta = (HN[a].get("operative_text") or "")
    tb = (HN[b].get("operative_text") or "")
    diff = ta != tb
    print(f"  M5  {a} != {b} : {'PASS' if diff else '*** FAIL — byte-identical ***'}"
          f"   ({len(ta)}c vs {len(tb)}c)")
    fail += 0 if diff else 1

empty = [k for k, h in HN.items() if not (h.get("operative_text") or "").strip()]
print(f"  M5  no hunk empty : {'PASS' if not empty else '*** FAIL ***'}   {empty}")
fail += 0 if not empty else 1

seen = {}
for key, h in HN.items():
    for eid in h.get("manifest_entries", []):
        seen.setdefault(eid, []).append(key)
multi = {k: v for k, v in seen.items() if len(v) > 1}
missing = [e["id"] for e in claimed if e["id"] not in seen]
print(f"  M5  all 36 claimed entries assigned exactly once : "
      f"{'PASS' if len(seen) == 36 and not multi and not missing else '*** FAIL ***'}"
      f"   assigned={len(seen)} multi={multi} missing={missing}")
fail += 0 if (len(seen) == 36 and not multi and not missing) else 1

print(f"\nM4/M5 failures: {fail}")
