#!/usr/bin/env python3
"""DELTA R49 / R6 blockers B5 and B7.

B5  SC-4(k2) made an UNCOMMITTED DRAFT a gate input. The manifest carries
    "manifest_status": "DRAFT - author review required", the declaration's SC-8(a)
    freeze does not enumerate it, and the declaration expressly withdraws its
    leaking-source COUNT from the arithmetic. (k2) as drafted would let an author
    review that is not a class C amendment make a complete reconciliation incomplete.

B7  SC-13c(c5)(i) says its map is indexed "as SC-3(a) declares" and then RESTATES
    (a)'s indexing triple in the same sentence - while declaring, one clause earlier,
    that it holds things "by citation and not restated here". R47/P5 edited (a) and
    left this copy behind, so the second copy is now DIVERGENT: it lacks (a)'s
    diagnostic-rows carve-out. Single normative source, SS0.2.1 line 77.

Source and hunk edited from ONE string so they cannot drift.
"""
import json
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
ssf = D / "SCHEMA_SET_FINAL.md"
hp = D / "_X5_hunks_v2.json"


def swap(old, new, label):
    """Replace in the quoted source and in the one hunk that carries it."""
    s = ssf.read_text(encoding="utf-8")
    oq = "\n".join(("> " + x).rstrip() for x in old.split("\n"))
    nq = "\n".join(("> " + x).rstrip() for x in new.split("\n"))
    assert s.count(oq) == 1, "%s: source match %d" % (label, s.count(oq))
    ssf.write_text(s.replace(oq, nq, 1), encoding="utf-8")
    d = json.loads(hp.read_text(encoding="utf-8"))
    n = 0
    for h in d["hunks"]:
        op = h.get("operative_text") or ""
        if old in op:
            h["operative_text"] = op.replace(old, new, 1)
            n += 1
    assert n == 1, "%s: hunk match %d" % (label, n)
    json.dump(d, open(hp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%s: source + 1 hunk updated" % label)


# ------------------------------------------------------------------ B5
OLD5 = """**(k2) THE RECONCILIATION.** The REQUIRED list is published alongside a **per-unit reconciliation
against the manifest's independently-leaking-source list** (\u00a76.2 line 446). **Every unit the
manifest records as a leaking source that this derivation does not class REQUIRED is named**, with
**the registered predicate of (b) that produced its class** and the declared facts on which it
satisfies that predicate. A difference stated as a count, a total, or a summary of where the
differences "mostly" sit does not satisfy this limb; the unit is named or it is not reconciled."""
NEW5 = """**(k2) THE RECONCILIATION.** The REQUIRED list is published alongside a **per-unit reconciliation
against the fixture manifest's list of columns classed as leaking sources** \u2014 the **named list**,
not the count. **Every unit the manifest so classes that this derivation does not class REQUIRED is
named**, with **the registered predicate of (b) that produced its class** and the declared facts on
which it satisfies that predicate. A difference stated as a count, a total, or a summary of where
the differences "mostly" sit does not satisfy this limb; the unit is named or it is not reconciled.

**The list is a publication input, and the count remains not a gate number.** Reading the list under
this limb neither makes the manifest's leaking-source **count** a gate quantity nor admits it to any
denominator \u2014 (k3) governs, and \u00a76.2 line 446's manifest requirement is unamended. **Because the
gate now reads that list, the manifest is an object the gate consumes: the declaration enumerates it
in the SC-8(a) freeze, and its recorded status is not `DRAFT` at the tag.** A list that invites its
own later revision cannot decide a gate outcome; an author review that silently made a complete
reconciliation incomplete would be a change to a gate input outside the class C route."""
swap(OLD5, NEW5, "B5")

# ------------------------------------------------------------------ B7
OLD7 = """scoring rule and its three dispositions are SC-3(b)'s, held by citation and not restated here**;
its map is indexed as SC-3(a) declares \u2014 **per side, per declared violation class, and per
declared cell** of the declared scored population. **The cell key is the declaration's to supply,"""
NEW7 = """scoring rule and its three dispositions are SC-3(b)'s, and **its map, its indexing, and what the
artifact publishing it may carry are SC-3(a)'s \u2014 all held by citation and none restated here.**
*(R49/B7: this clause previously restated (a)'s indexing triple in the same breath as declaring it
unrestated. R47/P5 then amended (a) and left the copy behind, so the copy became DIVERGENT \u2014 it
lacked (a)'s carve-out for artifact rows that are not cells of the map. Two normative copies of one
rule is \u00a70.2.1 line 77's defect; the second copy silently going stale is why.)* **The cell key is
the declaration's to supply,"""
swap(OLD7, NEW7, "B7")
