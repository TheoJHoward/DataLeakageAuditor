# K2 (S4) verification applier. Applies, to the K2 verify copy ONLY, three drafted edits:
#   (1) H1a status line  -> numeral-free form
#   (2) H1b block (applied lines 15-39) -> enumeration-first amendments block (the §AB
#       recording text at applied lines 41-53 is kept byte-exact)
#   (3) C1/C2 retention blocks (K2-F1 fix): the superseded v30 text of lines 992 and 1022
#       retained verbatim at their sites, marked NOT operative
# Refuses to run anywhere but amendment\_K2_verify. Asserts match count 1 at every anchor.
# Writes the block text it applied to _K2_BLOCK_TEXT_as_applied.md so the ledger can be
# checked against it word for word.
import sys, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "_K2_verify"
if not ROOT.is_dir() or ROOT.name != "_K2_verify":
    sys.exit("refusing: verify root missing")
P = ROOT / "PREREG.md"
text = P.read_text(encoding="utf-8")
assert hashlib.sha256(text.encode("utf-8")).hexdigest().startswith("e7ab52d3"), "not the e7ab52d3 applied file"
lines = text.split("\n")

def one(needle, where):
    hits = [i for i, l in enumerate(lines) if l == needle]
    assert len(hits) == 1, f"{where}: match count {len(hits)} for full-line anchor"
    return hits[0]

# ---------- (1) H1a ----------
OLD_H1A = ("**Amendment status:** **v30a — this file is amended.** Six class C changes under §0.2.1, listed in the v30a "
           "amendments block below. The v30 text of every amended clause is retained inline, marked superseded; "
           "`git show prereg-v30:PREREG.md` recovers the registered text byte-exact.")
NEW_H1A = ("**Amendment status:** **v30a — this file is amended.** The class C changes under §0.2.1 are enumerated, by "
           "registered surface and clause, in the v30a amendments block below; their number is read from that "
           "enumeration and is stated nowhere as a numeral. The v30 text of every superseded clause is retained "
           "inline at its site, marked superseded; `git show prereg-v30:PREREG.md` recovers the registered text "
           "byte-exact.")
i = one(OLD_H1A, "H1a")
lines[i] = NEW_H1A

# ---------- (2) H1b block: applied lines 15..39 (1-based) replaced ----------
start = one("## v30a amendments (class C under §0.2.1)", "H1b heading")
end_anchor_prefix = "**What an amendment may not do, restated here because this is the first one.**"
ends = [j for j, l in enumerate(lines) if l.startswith(end_anchor_prefix)]
assert len(ends) == 1, f"H1b end anchor count {len(ends)}"
end = ends[0]
assert end > start and (end - start) == 24, f"H1b block span unexpected: {end-start}"
# sanity: the §AB text follows after one blank line
assert lines[end + 1] == "" and lines[end + 2].startswith("**RECORDED DEFECT, NOT RESOLVED BY THIS AMENDMENT"), "§AB not where expected"

NEW_BLOCK = (Path(__file__).resolve().parent / "_K2_BLOCK_TEXT.md").read_text(encoding="utf-8").rstrip("\n").split("\n")
assert NEW_BLOCK[0] == "## v30a amendments (class C under §0.2.1)"
lines[start:end + 1] = NEW_BLOCK

# ---------- (3) C1 retention: after the phase table's last row ----------
P998 = "| **7** | Profiles, docs, v1.0 | 1–2 wknds | `futures` and `generic` profiles ship |"
k = one(P998, "phase table last row")
assert lines[k + 1] == "", "expected blank after phase table"
C1_RET = ("> **§10 line 992 (Phase 1 gate cell) — SUPERSEDED BY v30a, consequential to §6.2 lines 445 and 451. "
          "Registered v30 row, retained verbatim, NOT operative:** \"| **1** | Availability model and profiles; "
          "**verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded "
          "slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three "
          "controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation "
          "filed with the measurement; both fixture AUCs reproduce within ±0.010, full and sliced; **all four "
          "alignment-control cases behave as §6.5 requires**; snapshots hashed |\" *Retired because its Gate cell "
          "reads on two superseded objects: \"both\" names the retired anchor pair of line 445, and \"sliced\" names "
          "the artifact line 451 moves off the Phase 0 fixture and re-registers as a Phase 1 CI obligation. Only the "
          "Gate cell is changed in the operative row above; Phase, Work and Est. are byte-identical. Recover the "
          "registered row byte-exact with `git show prereg-v30:PREREG.md`.*")
lines[k + 1:k + 1] = ["", C1_RET]

# ---------- (3) C2 retention: under §10.1 item 3 ----------
A1277_PREFIX = "3. Fires on `fixture_contaminated` and, on `fixture_corrected`, reports findings **consistent with the declared ground-truth map"
hits = [j for j, l in enumerate(lines) if l.startswith(A1277_PREFIX)]
assert len(hits) == 1, f"C2 site count {len(hits)}"
m = hits[0]
assert lines[m + 1].startswith("4. Installs and runs through a documented public interface"), "expected item 4 after item 3"
C2_RET = ("   > **§10.1 line 1022 (kill-gate criterion 3) — SUPERSEDED BY v30a, consequential to §6.2 line 461. "
          "Registered v30 text, retained verbatim, NOT operative:** \"3. Fires on `fixture_contaminated` and is silent "
          "on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically "
          "ambiguous (§6.2), under the labelled hypothetical declaration**;\" *Retired because it is a second copy of "
          "the premise criterion 3 (line 461) retires — that silence on the corrected side is the correct behaviour. "
          "Under SC-3 the corrected side is characterized, never clean, and a tool silent where the map declares a "
          "violation is silent where it should fire. The ambiguity branch is carried through unchanged. Recover the "
          "registered line byte-exact with `git show prereg-v30:PREREG.md`.*")
lines[m + 1:m + 1] = [C2_RET]

out = "\n".join(lines)
P.write_text(out, encoding="utf-8", newline="\n")
h = hashlib.sha256(out.encode("utf-8")).hexdigest()
print("written", P, "lines", out.count("\n") + (0 if out.endswith("\n") else 1), "sha256", h)
(Path(__file__).resolve().parent / "_K2_BLOCK_TEXT_as_applied.md").write_text("\n".join(NEW_BLOCK) + "\n", encoding="utf-8", newline="\n")
