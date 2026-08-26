#!/usr/bin/env python3
"""DELTA R49 / R5 - draft SC-4(k): the criterion-1 floor and the reconciliation.

Built on the F7 draft (F1: a finding is not discarded because the round moved on),
tightened in three ways R47-R48 make necessary:
  - (k1) says WHY non-emptiness is the whole floor - any number above zero would be
    chosen from the data, which is the same reasoning that ruled P6.
  - (k4) states the failure condition, because R49/R2's refined SC-8(g) requires every
    gate item to, and says which of R2's two kinds this is.
  - the reconciliation target is the MANIFEST's leaking-source list, which is NOT what
    the declaration's existing per-unit table (A.6.5) cross-tabulates.

Source of record is SCHEMA_SET_FINAL.md (M1). Source and hunk are edited from ONE
string so they cannot drift. N2's growth procedure follows.
"""
import json
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

TAIL = ("**(j) THE SCORED SET IS NAMED, NOT COUNTED.** The declared scored set is identified by "
        "**the named\nconstant the declaration declares**, never by its cardinality. Any "
        "re-derivation names the constant,\nnot the length; two sets of equal size are not "
        "thereby the same set.")

K = """

**(k) THE REQUIRED LIST IS NON-EMPTY, AND THE DENOMINATOR IS RECONCILED AGAINST THE MANIFEST.**

**(k1) THE FLOOR.** The declared scored set and the REQUIRED list are enumerated by name **before
any detector runs** and are **non-empty on every declared side**. **If either is empty on any
declared side, criterion 1 is not discharged and the outcome is STOP** \u2014 lifted only by
supplementing the declaration with declared, enumerated units for that side and re-freezing under
\u00a711's integrity chain; never by scoring criterion 1 on the remaining side, never by suppressing the
empty side's gate, and never by a `DEVIATIONS.md` entry or a working resolution. **Non-emptiness is
the whole floor, and deliberately so:** any minimum above zero would be a threshold chosen from the
distribution this fixture already exhibits, which \u00a77.0 forbids. A floor that cannot be set without
looking at the data is not set.

**(k2) THE RECONCILIATION.** The REQUIRED list is published alongside a **per-unit reconciliation
against the manifest's independently-leaking-source list** (\u00a76.2 line 446). **Every unit the
manifest records as a leaking source that this derivation does not class REQUIRED is named**, with
**the registered predicate of (b) that produced its class** and the declared facts on which it
satisfies that predicate. A difference stated as a count, a total, or a summary of where the
differences "mostly" sit does not satisfy this limb; the unit is named or it is not reconciled.

**(k3) THE RECONCILIATION IS A DISCLOSURE, NOT A CLASSIFICATION.** **A reconciliation published
under this limb is a disclosure, not a classification entering a criterion, denominator, or count**
(a). It derives nothing, changes no class, and no quantity appearing in it is N. This sentence is
load-bearing: without it (a) forbids the very comparison that makes the denominator auditable, and
the limb would contradict the clause it sits in.

**(k4) WHAT MAKES THIS LIMB FAIL** \u2014 stated because SC-8(g) requires every gate item to state it.
This limb fails where the REQUIRED list is empty on a declared side; **or where the reconciliation
is absent**; or where any difference in it is unnamed, or is named without the registered predicate
that produced its class. **This is a live gate item and not a regression guard (SC-8(g)(a)): it can
fail on an artifact that is behaving correctly, and on the fixture as declared at the date of this
amendment it is UNSATISFIED.** The declaration publishes a per-unit cross-tabulation of the
construction-SOURCE cut against the gate cut, which is a different pair of partitions; it publishes
no per-unit reconciliation against the manifest's leaking-source list. The difference the limb
would surface is **fourteen units**."""

# ---- 1. source of record -----------------------------------------------------
ssf = D / "SCHEMA_SET_FINAL.md"
src = ssf.read_text(encoding="utf-8")
tail_q = "\n".join("> " + l for l in TAIL.split("\n"))
k_q = "\n".join(("> " + l).rstrip() for l in K.split("\n"))
assert src.count(tail_q) == 1, "SC-4(j) tail match %d" % src.count(tail_q)
assert "**(k) THE REQUIRED LIST IS NON-EMPTY" not in src, "SC-4(k) already present"
ssf.write_text(src.replace(tail_q, tail_q + k_q, 1), encoding="utf-8")
print("SCHEMA_SET_FINAL.md : SC-4(k) inserted after (j)  (+%d lines)" % len(k_q.split("\n")))

# ---- 2. the hunk, from the SAME string ---------------------------------------
p = D / "_X5_hunks_v2.json"
d = json.loads(p.read_text(encoding="utf-8"))
n = 0
for h in d["hunks"]:
    op = h.get("operative_text") or ""
    if TAIL in op:
        h["operative_text"] = op.replace(TAIL, TAIL + K, 1)
        h["what_changes"] = (h.get("what_changes") or "").rstrip() + (
            "  **R49/R5 adds limb (k)**: the criterion-1 floor (non-empty REQUIRED list on every "
            "declared side, on pain of STOP, modelled on SC-13b(b1)'s existing sentence) and the "
            "per-unit reconciliation against the manifest's leaking-source list, with the express "
            "carve-out that the reconciliation is a disclosure rather than a classification \u2014 "
            "without which (a) forbids the check that closes the hole. **(k) is unsatisfied by the "
            "declaration as it stands** and is the only limb of SC-4 that is.")
        n += 1
assert n == 1, "hunk match %d" % n
json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("SC-4 hunk        : operative text and what_changes updated")

s2 = ssf.read_text(encoding="utf-8")
d2 = json.loads(p.read_text(encoding="utf-8"))
assert sum(1 for h in d2["hunks"] if K in (h.get("operative_text") or "")) == 1
assert k_q in s2
print("AGREEMENT PROVEN : (k) is in the source (quoted) and in exactly one hunk")
