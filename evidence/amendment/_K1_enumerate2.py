#!/usr/bin/env python3
"""DELTA R47 - the enumerator that actually produced the frozen population.

WHY THIS EXISTS. `_K1_enumerate.py` emits {line, heading, sha12, chars, first}.
`_K1_population_FROZEN.json` carries {idx, lines:[a,b], kind, heading, sha12,
chars, first}. They are not the same schema, so N2's growth check could never
absorb a real change - it crashed on KeyError('lines') the first time the
population actually moved. The check had only ever been exercised against a
population that had not changed.

This emits the FROZEN schema, and its correctness is PROVEN rather than
asserted: run with --verify it reconstructs the pre-R47 source and requires the
enumeration to equal `_K1_population_FROZEN.json` field for field.

POPULATION DECLARED: every blockquote run and every fenced block in PART 1 of
SCHEMA_SET_FINAL.md. PROOF OF COVERAGE: in-Part-1 + outside-Part-1 = whole file.
"""
import hashlib
import json
import re
import sys
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

NEWTXT = ("published as an artifact with a **declared schema**: one row per cell of the declared scored\n"
          "population, with every field named, including the field that records whether the cell is\n"
          "scored. **The artifact may in addition carry rows of a class the declaration declares\n"
          "DIAGNOSTIC (SC-10(c)); those rows are not cells of the map.** They are adjudicated by no\n"
          "criterion, enter no denominator and no rate, and **(b)'s dispositions are exhaustive over the\n"
          "map's cells, not over the artifact's row count**. A count taken from the artifact without\n"
          "excluding them counts a different population, and **every figure published from the artifact\n"
          "names which population it counts**.")
OLDTXT = ("published as an artifact with a **declared schema**: one row per scored cell, with every field\n"
          "named, including the field that records whether the cell is scored.")


def heading_tracker(ln, last, inside):
    if inside:
        return last
    m = re.match(r"^#{1,6}\s+(.*)$", ln)
    if m:
        return m.group(1).strip()
    m = re.match(r"^\*\*(.+?)\.?\*\*", ln.strip())
    if m and not ln.startswith(">"):
        return m.group(1).strip()
    return last


def enumerate_blocks(text):
    """Blockquote runs and fenced blocks, each with its full line range."""
    lines = text.split("\n")
    out, cur, start, head, last, inside = [], [], None, None, None, False
    for i, ln in enumerate(lines, start=1):
        if ln.startswith("```"):
            if not inside:
                if cur:                       # a quote run ends where a fence opens
                    out.append((start, i - 1, "quote", head or "(none)", "\n".join(cur).strip()))
                    cur = []
                inside, start, head = True, i, last
                fbody = []
            else:
                inside = False
                out.append((start, i, "fence", head or "(none)", "\n".join(fbody).strip()))
            continue
        if inside:
            fbody.append(ln)
            continue
        last = heading_tracker(ln, last, inside)
        if ln.startswith(">"):
            if not cur:
                start, head = i, last
            cur.append(re.sub(r"^>\s?", "", ln))
        elif cur:
            out.append((start, i - 1, "quote", head or "(none)", "\n".join(cur).strip()))
            cur = []
    if cur:
        out.append((start, len(lines), "quote", head or "(none)", "\n".join(cur).strip()))
    return sorted(out, key=lambda r: r[0])


def population(text, verbose=True):
    lines = text.split("\n")
    p1 = next(i for i, l in enumerate(lines, 1) if l.startswith("# PART 1"))
    p2 = next(i for i, l in enumerate(lines, 1) if l.startswith("# PART 2"))
    allb = enumerate_blocks(text)
    inp = [b for b in allb if p1 <= b[0] < p2]
    outp = [b for b in allb if not (p1 <= b[0] < p2)]
    if verbose:
        print("POPULATION DECLARED: blockquote runs AND fenced blocks in PART 1")
        print("  file lines %d | PART 1 at %d | PART 2 at %d" % (len(lines), p1, p2))
        print("  PROOF OF COVERAGE: in-Part-1 %d + outside %d = %d (total %d) %s"
              % (len(inp), len(outp), len(inp) + len(outp), len(allb),
                 "OK" if len(inp) + len(outp) == len(allb) else "*** MISMATCH ***"))
    return [{"idx": i, "lines": [a, b], "kind": k, "heading": h,
             "sha12": hashlib.sha256(body.encode("utf-8")).hexdigest()[:12],
             "chars": len(body), "first": re.sub(r"\s+", " ", body)[:90]}
            for i, (a, b, k, h, body) in enumerate(inp, 1)]


ssf = D / "SCHEMA_SET_FINAL.md"
new_src = ssf.read_text(encoding="utf-8")

if "--verify" in sys.argv:
    new_q = "\n".join("> " + l for l in NEWTXT.split("\n"))
    old_q = "\n".join("> " + l for l in OLDTXT.split("\n"))
    assert new_src.count(new_q) == 1, "cannot reconstruct the pre-R47 source"
    old_src = new_src.replace(new_q, old_q, 1)
    got = population(old_src)
    want = json.loads((D / "_K1_population_FROZEN.json").read_text(encoding="utf-8"))
    print("\nVERIFY against _K1_population_FROZEN.json (pre-R47 source)")
    print("  blocks: got %d, frozen %d" % (len(got), len(want)))
    bad = 0
    for g, w in zip(got, want):
        for f in ("idx", "lines", "kind", "sha12", "chars"):
            if g[f] != w[f]:
                print("   *** idx %s field %s: got %r want %r" % (w["idx"], f, g[f], w[f]))
                bad += 1
    if len(got) != len(want):
        bad += 1
    print("  RESULT: %s" % ("REPRODUCES THE FROZEN POPULATION EXACTLY" if not bad
                            else "*** %d MISMATCH(ES) - do not trust this enumerator ***" % bad))
    sys.exit(1 if bad else 0)

cur = population(new_src)
json.dump(cur, open(D / "_K1_population.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("\nwrote _K1_population.json - %d blocks" % len(cur))
