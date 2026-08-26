#!/usr/bin/env python3
"""DELTA R37 / D7 — ASSEMBLER SELF-CHECK.

Three assertions the assembler runs on its own output BEFORE any critic sees it.
All three failures the R36 critics found are mechanically detectable; a critic
catching them was a critic doing an assembler's job.

  (i)   every ledger row has operative text somewhere
  (ii)  no source line is targeted by two hunks
  (iii) every marker anchor sits at a COMPLETE-BLOCK boundary

Read-only. Prints a report; exits non-zero if any assertion fails.
"""

import json
import re
import sys
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]
ssf = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8")
diffdoc = (D / "PREREG_v30a_DIFF.md").read_text(encoding="utf-8")
k2 = (D / "K2_AMENDMENT_LEDGER.md").read_text(encoding="utf-8")
prereg = (REPO / "PREREG.md").read_text(encoding="utf-8").split("\n")

fail = 0


def head(t):
    print("\n" + "=" * 74)
    print(t)
    print("=" * 74)


def first_line(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else None


# ---------------------------------------------------------------- (i)
head("(i) EVERY LEDGER ROW HAS OPERATIVE TEXT")

block = k2[k2.index("<!-- K2-BLOCK-BEGIN -->"):k2.index("<!-- K2-BLOCK-END -->")]
rows = []
for ln in block.split("\n"):
    if not ln.startswith("|") or ln.startswith("|---") or "Registered surface" in ln \
       or "Site (after" in ln:
        continue
    cells = [c.strip() for c in ln.strip("|").split("|")]
    if not cells:
        continue
    m = re.search(r"line[s]?\s+(\d+)", cells[0])
    if m:
        rows.append((int(m.group(1)), cells[0], cells[1] if len(cells) > 1 else ""))

hunk_lines = {first_line(h) for h in hunks if first_line(h)}
hunk_lines |= {h["retains_line"] for h in hunks if h.get("retains_line")}
print(f"  ledger rows naming a v30 line : {len(rows)}")
print(f"  distinct lines covered by hunks: {len(hunk_lines)}")
missing = []
for line, surface, touch in rows:
    if line in hunk_lines:
        continue
    # is operative text drafted anywhere?
    in_ssf = bool(re.search(rf"line\s+\*{{0,2}}{line}\*{{0,2}}", ssf))
    in_diff = bool(re.search(rf"line\s+\*{{0,2}}{line}\*{{0,2}}", diffdoc))
    missing.append((line, surface, touch, in_ssf, in_diff))
if missing:
    fail += 1
    print(f"  *** {len(missing)} ledger row(s) with NO hunk in the artifact ***")
    for line, surface, touch, a, b in missing:
        src = "SCHEMA_SET_FINAL" if a else ("PREREG_v30a_DIFF only" if b else "NOWHERE")
        print(f"    line {line:<5} {surface[:58]:<58} touch={touch[:18]:<18} text in: {src}")
else:
    print("  PASS — every ledger row naming a v30 line has a hunk")

# ---------------------------------------------------------------- (ii)
head("(ii) NO SOURCE LINE TARGETED BY TWO HUNKS")

by_line = {}
for h in hunks:
    n = first_line(h)
    if n:
        by_line.setdefault(n, []).append(h)
collisions = {n: hs for n, hs in by_line.items() if len(hs) > 1}
# a collision is benign only if every hunk on the line is an insert AND order is stated
real = []
for n, hs in sorted(collisions.items()):
    ops = [h.get("operation") for h in hs]
    replaces = [o for o in ops if o in ("replace", "replace-row")]
    def blob(x):
        return ((x.get("prereg_line") or "") + " " + (x.get("what_changes") or "")
                + " " + (x.get("justification") or "")).lower()
    ordered = all(any(k in blob(h) for k in ("following", "after ", "order")) for h in hs)
    # One operation ON the line plus one after the block it produces is not a
    # collision; two replaces on one line is. Order is stated when ANY hunk in
    # the group fixes its position relative to the others.
    ordered = any(any(k in blob(h) for k in ("following", "after ", "order")) for h in hs)
    twin_replace = len(replaces) > 1
    verdict = ("BENIGN (one op on the line, order stated)" if not twin_replace and ordered
               else "*** COLLISION ***")
    if twin_replace or not ordered:
        real.append(n)
    print(f"  line {n:<5} {len(hs)} hunks  ops={ops}  -> {verdict}")
    for h in hs:
        print(f"          {h.get('clause','')[:60]}")
if real:
    fail += 1
    print(f"  *** {len(real)} line(s) need an explicit application order or a hunk removed ***")
else:
    print("  PASS — no unordered or replace-on-replace collision")

# ---------------------------------------------------------------- (iii)
head("(iii) EVERY MARKER ANCHOR AT A COMPLETE-BLOCK BOUNDARY")

print("  RULE: a supersession marker attaches to a COMPLETE BLOCK - a whole paragraph,")
print("        a whole table, or a whole list - never inside one. Mechanically: the line")
print("        after the anchor must be blank (the anchor ends its block), or the anchor")
print("        must be the last line of the file.")
print()


def block_kind(i):
    """What structure is line i (1-based) part of?"""
    ln = prereg[i - 1] if 0 < i <= len(prereg) else ""
    if ln.startswith("|"):
        return "table row"
    if re.match(r"\s*[-*+] |\s*\d+\. ", ln):
        return "list item"
    if ln.strip() == "":
        return "blank"
    return "paragraph"


bad = []
for h in hunks:
    if h.get("operation") != "marker":
        continue
    n = h.get("write_line") or first_line(h)
    if not n:
        continue
    nxt = prereg[n] if n < len(prereg) else ""
    ok = (nxt.strip() == "")
    kind = block_kind(n)
    nkind = block_kind(n + 1)
    print(f"  line {n:<5} {h.get('clause','')[:22]:<22} anchor={kind:<10} next={nkind:<10} "
          f"{'OK' if ok else '*** INSIDE A BLOCK ***'}")
    if not ok:
        bad.append((n, h.get("clause", ""), kind, nkind))
if bad:
    fail += 1
    print(f"\n  *** {len(bad)} marker anchor(s) inside a block ***")
    for n, cl, kind, nkind in bad:
        # find the end of the block
        j = n
        while j < len(prereg) and prereg[j].strip() != "":
            j += 1
        print(f"    line {n} ({cl}) is a {kind}; its block ends at line {j}. "
              f"Re-anchor the marker to line {j}.")
else:
    print("\n  PASS — every marker anchor ends its block")


# ---------------------------------------------------------------- (iv) F3
head("(iv) EVERY HUNK CARRIES READABLE OPERATIVE TEXT  [R39/F3]")
print("  Prose paraphrase is not operative text. The author must be able to read what")
print("  each hunk actually puts into PREREG.md.")
print()
noop = [h for h in hunks if not (h.get("operative_text") or "").strip()]
thin = [h for h in hunks
        if (h.get("operative_text") or "").strip() and len(h["operative_text"]) < 80]
print(f"  hunks: {len(hunks)}   without operative text: {len(noop)}   suspiciously short: {len(thin)}")
for h in noop:
    print(f"    MISSING  line {first_line(h)}  {h.get('clause','')[:58]}")
for h in thin:
    print(f"    SHORT    line {first_line(h)}  {h.get('clause','')[:58]}")
rendered = 0
art_check = D / "X5_FINAL_PREREG_DIFF.md"
if art_check.exists():
    rendered = art_check.read_text(encoding="utf-8").count("**Operative text — what this hunk")
    print(f"  operative-text blocks rendered in the artifact: {rendered} (need {len(hunks)})")
    print("  A field the author cannot read is not a field the author has. The check is on")
    print("  DELIVERY, not on storage.")
if noop or (art_check.exists() and rendered != len(hunks)):
    fail += 1
    print("  *** operative text is stored but not delivered ***" if not noop else "")
else:
    print("  PASS — every hunk carries operative text, and the artifact renders all of it")

# ---------------------------------------------------------------- (v) F6(i)
head("(v) NO CARRIED-FORWARD COUNT IN THE ASSEMBLED PROSE  [R39/F6(i)]")
print("  Every citation into a mutable file - counts, line numbers, quoted text - is")
print("  re-derived at assembly. A numeral written once and never re-checked is stale")
print("  by construction; that is how 'thirty-seven hunks' survived into a 36-hunk file.")
print()
art_p = D / "X5_FINAL_PREREG_DIFF.md"
if art_p.exists():
    art = art_p.read_text(encoding="utf-8")
    WORDS = {"thirty-six": 36, "thirty-seven": 37, "thirty-five": 35, "thirty-eight": 38,
             "thirty-nine": 39, "forty": 40}
    bad_words = [(w, v) for w, v in WORDS.items() if w in art.lower() and v != len(hunks)]
    m = re.search(r"\*\*(\d+) hunks\.", art)
    stated = int(m.group(1)) if m else None
    print(f"  derived hunk count: {len(hunks)}")
    print(f"  count stated in the artifact's summary: {stated}")
    for w, v in bad_words:
        print(f"    *** prose says '{w}' ({v}) but the data says {len(hunks)} ***")
    if bad_words or (stated is not None and stated != len(hunks)):
        fail += 1
    else:
        print("  PASS — no numeral in the artifact contradicts the derived count")
else:
    print("  artifact not yet assembled; check deferred")

# ---------------------------------------------------------------- (vi) F6(ii)
head("(vi) EVERY FINDING CARRIES A STATUS  [R39/F6(ii)]")
print("  OPEN / FIXED / WITHDRAWN, with what fixed it. Six findings once contradicted the")
print("  file they described because the defect was fixed and the finding was not withdrawn.")
print()
tri = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8")).get("findings_triaged")
if not tri:
    print("  *** no triage present ***")
    fail += 1
else:
    nostat = [t for t in tri if t.get("status") not in ("OPEN", "FIXED", "WITHDRAWN")]
    nofix = [t for t in tri if t.get("status") == "FIXED" and not t.get("fixed_by")]
    from collections import Counter
    c = Counter(t["status"] for t in tri)
    print(f"  findings: {len(tri)}   " + "   ".join(f"{k}={v}" for k, v in sorted(c.items())))
    print(f"  without a valid status: {len(nostat)}   FIXED without what-fixed-it: {len(nofix)}")
    if nostat or nofix:
        fail += 1
    else:
        print("  PASS — every finding has a status, and every FIXED names what fixed it")

# ---------------------------------------------------------------- (vii) R48/Q8
head("(vii) EVERY LIVE ABSENCE CLAIM DECLARES ITS SEARCH POPULATION  [R48/Q8, H-L15]")
print("  Four absence findings at PROVEN confidence in one workflow each declared a population")
print("  that excluded the active root in ROUND_STATE \u00a70. All four were wrong. The lesson text")
print("  already said 'an absence finding is only as good as the search behind it'; repeating it")
print("  would not have caught this, so it is asserted here instead.")
print()
_SIG = re.compile(r"\b(no hunk|does not exist|do(es)? not appear|is absent|are absent|nowhere|"
                  r"never (ran|runs)|not present|no such|has no|carried by no|no clause|appears in no)\b", re.I)
_UNSCOPED = re.compile(r"\b(nowhere|does not exist|never ran|anywhere in the (corpus|repository|archive))\b", re.I)
_ROOT = "8b1d67a4"

_tri = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8")).get("findings_triaged") or []
_abs = [(i, t) for i, t in enumerate(_tri)
        if _SIG.search(t["text"]) and t.get("status") != "WITHDRAWN"]
_nopop = [i for i, t in _abs if "SEARCHED:" not in t["text"]]
_unscoped_norot = [i for i, t in _abs
                   if _UNSCOPED.search(t["text"]) and _ROOT not in t["text"]
                   and "SCOPED absence claim" not in t["text"]]

print(f"  live absence claims (OPEN/FIXED)      : {len(_abs)}")
print(f"  without a declared SEARCHED: population: {len(_nopop)}  {_nopop if _nopop else ''}")
print(f"  UNSCOPED and not naming the active root: {len(_unscoped_norot)}  {_unscoped_norot if _unscoped_norot else ''}")
if _nopop or _unscoped_norot:
    fail += 1
    print("  *** an absence claim whose population is undeclared may not carry a disposition ***")
    print("  *** remedy (H-L15): name the artifact and why it is authoritative, or downgrade  ***")
    print("  *** the claim to 'not found in X' and let no disposition follow from it.        ***")
else:
    print("  PASS \u2014 every live absence claim declares the population it searched")

# ---------------------------------------------------------------- (viii) R51/W1
head("(viii) SECTION-B HUNK PROVENANCE — FULL COVERAGE, BOTH DIRECTIONS")
print("  REPLACED at R51/W1. The previous form sampled five 110-char windows, first hit")
print("  wins — 21.1%% of a 2,612-char hunk — and mutation testing showed it passed ALL of:")
print("  tolerance 0.010->0.100; deleting the fails-this-gate-row sentence; dropping `tier`;")
print("  FLIPPING \"fails this gate row\" -> \"is recorded as a deviation\"; deleting the")
print("  pass/fail-evidence sentence. It reported green on the exact reduction it existed")
print("  to catch. This form catches all five.")
print()
print("  FORWARD  — every character of the hunk has provenance in a named source,")
print("             its own anchor, or PREREG.md (greedy longest-match tiling, 100%% required).")
print("  CONVERSE — where the manifest declares a source SPAN, that span survives in the")
print("             hunk verbatim. Coverage alone is DELETION-BLIND: removing text never")
print("             lowers the provenance of what remains.")
print()
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location("_prov", str(D / "_provenance.py"))
_prov = _ilu.module_from_spec(_sp)
_sp.loader.exec_module(_prov)
_fails, _rows = _prov.run()
if _fails:
    fail += 1
    print(chr(10)+"*** %d section-B hunk(s) failed provenance: %s ***" % (len(_fails), _fails))
else:
    print(chr(10)+"PASS — every section-B hunk is fully provenanced and no declared span is broken")

# ---------------------------------------------------------------- (ix) R55/W5
head("(ix) NO WITHDRAWN CLAIM IS ASSERTED LIVE IN OPERATIVE TEXT")
print("  Every other check compares a hunk against its source. When a claim is withdrawn")
print("  and the correction lands on only one of the places carrying it, source and hunk")
print("  still AGREE - on the withdrawn text - so coverage is 100%, the span is intact,")
print("  and everything reports green. This is the gap that let a falsified claim ship")
print("  for two rounds in the one field that lands in PREREG.md.")
print()
_sp = _ilu.spec_from_file_location("_wc", str(D / "_withdrawn_claims.py"))
_wc = _ilu.module_from_spec(_sp)
_sp.loader.exec_module(_wc)
if _wc.run():
    fail += 1
    print(chr(10) + "  *** a withdrawn claim is asserted live; see the register ***")

# ---------------------------------------------------------------- (x) R56/B2
head("(x) EVERY COMPLETION CLAIM IN COMMENTARY IS TRUE OF THE OPERATIVE FIELD")
print("  A record of a fix is not a fix, and a FALSE record is worse than none: it turns")
print("  an open defect into a closed one in the reader's mind. Wherever commentary says a")
print("  correction happened, that sentence is itself a claim and is checked here against")
print("  the field that ships. This generalises (ix): (ix) knows only what someone")
print("  remembered to register; this knows whatever the drafter wrote down as done -")
print("  which is exactly the set at risk, because a drafter who records a fix believes it.")
print()
_sp = _ilu.spec_from_file_location("_cc", str(D / "_completion_claims.py"))
_cc = _ilu.module_from_spec(_sp)
_sp.loader.exec_module(_cc)
if _cc.run():
    fail += 1
    print(chr(10) + "  *** commentary records a correction the operative field does not carry ***")

# ---------------------------------------------------------------- (xi) R59/E1
head("(xi) EVERY LEDGER CITATION IN OPERATIVE TEXT RESOLVES, OR IS PLANNED")
print("  A citation to a ledger entry that does not exist and that NOTHING will write is")
print("  the SC-8(g) defect in a different file. PENDING is legitimate while drafting -")
print("  the ledgers take one hashed state at the ceremony - but it is fatal at the tag,")
print("  and it is reported every run so it cannot quietly become an orphan.")
print()
_sp = _ilu.spec_from_file_location("_lc", str(D / "_ledger_citations.py"))
_lc = _ilu.module_from_spec(_sp)
_sp.loader.exec_module(_lc)
if _lc.run():
    fail += 1
    print(chr(10) + "  *** operative text cites a ledger entry nothing will write ***")

head("SELF-CHECK RESULT")
print(f"  assertions failed: {fail} of 11")
sys.exit(1 if fail else 0)
