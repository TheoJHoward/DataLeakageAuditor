#!/usr/bin/env python3
"""R49 ADDENDUM S1-S3 - constraints on SC-4(k), applied to the draft in flight.

S1  Two mechanisms, neither sufficient alone. The FLOOR handles the degenerate case;
    the RECONCILIATION handles the gradual one. N >= 1 is satisfied by scoring a single
    column, so the floor must read as the terminal backstop it is - not as the
    protection. The clause now says which does which.
S2  State the verifiability limit honestly. The map ships with the tag; the FIXTURE does
    not. A third party can read a published reconciliation and cannot check its
    classifications against the data. An overstated obligation is the same defect class
    as an overstated availability claim.
S3  Adversarial test on (k) itself: a declarer satisfies it by classing 24 of 25 OUT OF
    JURISDICTION on thin grounds. "Quality of ground" is unregisterable vagueness; the
    achievable bar is PROVENANCE - every ground names the artifact and location behind it,
    so a ground with nothing behind it becomes visible rather than plausible.

Source and hunk edited from ONE string. S4's N2 procedure runs after.
"""
import json
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

OLD_HEAD = "**(k) THE REQUIRED LIST IS NON-EMPTY, AND THE DENOMINATOR IS RECONCILED AGAINST THE MANIFEST.**"
OLD_TAIL = "would surface is **fourteen units**."

NEW = """**(k) TWO MECHANISMS AGAINST A COLLAPSING SCORED POPULATION, AND NEITHER IS SUFFICIENT ALONE.**
There are two ways criterion 1 stops meaning anything, and they need different instruments. The
population can go **empty** \u2014 the degenerate case, caught by the floor at (k1). Or it can be
**narrowed unit by unit** until what survives is not worth scoring \u2014 the gradual case, caught by the
reconciliation at (k2). **(k1) alone is satisfied by scoring a single column.** It is written below
as the terminal backstop it is; **the operative protection is (k2)**, and a reader who takes the
backstop for the mechanism has mistaken which failure this clause exists to stop.

**(k1) THE FLOOR \u2014 THE TERMINAL BACKSTOP.** The declared scored set and the REQUIRED list are
enumerated by name **before any detector runs** and are **non-empty on every declared side**. **If
either is empty on any declared side, criterion 1 is not discharged and the outcome is STOP** \u2014
lifted only by supplementing the declaration with declared, enumerated units for that side and
re-freezing under \u00a711's integrity chain; never by scoring criterion 1 on the remaining side, never by
suppressing the empty side's gate, and never by a `DEVIATIONS.md` entry or a working resolution.
**Non-emptiness is the whole of this limb, and deliberately so:** any minimum above zero would be a
threshold chosen from the distribution this fixture already exhibits, which \u00a77.0 forbids. A floor
that cannot be set without looking at the data is not set. **This limb therefore catches only the
degenerate case; it is not the protection and must not be cited as one.**

**(k2) THE RECONCILIATION \u2014 THE OPERATIVE MECHANISM.** The REQUIRED list is published alongside a
**per-unit reconciliation against the fixture manifest's list of columns classed as leaking
sources** \u2014 the **named list**, not the count. **Every unit the manifest so classes that this
derivation does not class REQUIRED is named**, with **the registered predicate of (b) that produced
its class** and the declared facts on which it satisfies that predicate. A difference stated as a
count, a total, or a summary of where the differences "mostly" sit does not satisfy this limb; the
unit is named or it is not reconciled.

**(k2)(i) EVERY GROUND NAMES THE ARTIFACT AND LOCATION THAT SUPPORTS IT.** For each such unit the
declaration cites **the artifact and the location within it** \u2014 file, and row, line, or field \u2014 on
which the declared facts rest. **The quality of a ground is not something this registration can
require**, and pretending otherwise would be vagueness dressed as a constraint; **provenance is.** A
ground with an artifact behind it can be looked up and disagreed with. **A ground with nothing
behind it becomes visible as such**, which is the whole of what this limb can achieve and is worth
more than a bar no reader could apply.

**The list is a publication input, and the count remains not a gate number.** Reading the list under
this limb neither makes the manifest's leaking-source **count** a gate quantity nor admits it to any
denominator \u2014 (k3) governs, and \u00a76.2 line 446's manifest requirement is unamended. **Because the
gate now reads that list, the manifest is an object the gate consumes: the declaration enumerates it
in the SC-8(a) freeze, and its recorded status is not `DRAFT` at the tag.** A list that invites its
own later revision cannot decide a gate outcome; an author review that silently made a complete
reconciliation incomplete would be a change to a gate input outside the class C route.

**(k3) A DISCLOSURE, NOT A CLASSIFICATION \u2014 AND THE LIMIT OF WHAT A READER CAN CHECK.** **A
reconciliation published under this limb is a disclosure, not a classification entering a criterion,
denominator, or count** (a). It derives nothing, changes no class, and no quantity appearing in it is
N. That sentence is load-bearing: without it (a) forbids the very comparison that makes the
denominator auditable, and the limb would contradict the clause it sits in.

**What a third party can and cannot do with it, stated plainly rather than implied.** The declared
map and this reconciliation are published with the registration; **the acceptance fixture is not,
and no clause requires it to be.** So a reader can check the reconciliation for **completeness**
(every manifest-classed leaking source accounted for), for **internal consistency** (each ground
citing a registered predicate), and for **provenance** (each ground naming an artifact and
location) \u2014 and **cannot** independently verify a classification against the fixture's data. **This
limb is therefore a disclosure obligation with limited external verifiability, and it is registered
as one.** Claiming it delivers an audit a reader cannot perform would be the same defect as an
overstated availability claim.

**(k4) WHAT MAKES THIS LIMB FAIL.** This limb fails where the REQUIRED list is empty on a declared
side; **or where the reconciliation is absent**; or where any difference in it is unnamed, is named
without the registered predicate that produced its class, **or is named with a ground that cites no
artifact and location (k2)(i)**. **This is a live gate item, not a check that only fires on
corruption: it can fail on an artifact that is behaving correctly, and on the fixture as declared at
the date of this amendment it is UNSATISFIED.** The declaration publishes a per-unit
cross-tabulation of the construction-SOURCE cut against the gate cut, which is a different pair of
partitions; it publishes no per-unit reconciliation against the manifest's leaking-source list. The
difference the limb would surface is **fourteen units**."""

ssf = D / "SCHEMA_SET_FINAL.md"
s = ssf.read_text(encoding="utf-8")
i = s.index("> " + OLD_HEAD)
j = s.index("> " + OLD_TAIL) + len("> " + OLD_TAIL)
old_q = s[i:j]
old_plain = "\n".join(x[2:] if x.startswith("> ") else x[1:] if x == ">" else x
                      for x in old_q.split("\n"))
new_q = "\n".join(("> " + x).rstrip() for x in NEW.split("\n"))
ssf.write_text(s[:i] + new_q + s[j:], encoding="utf-8")
print("SCHEMA_SET_FINAL.md: SC-4(k) revised  (%d -> %d lines)"
      % (len(old_q.split("\n")), len(new_q.split("\n"))))

hp = D / "_X5_hunks_v2.json"
d = json.loads(hp.read_text(encoding="utf-8"))
n = 0
for h in d["hunks"]:
    op = h.get("operative_text") or ""
    if OLD_HEAD in op:
        a = op.index(OLD_HEAD)
        b = op.index(OLD_TAIL) + len(OLD_TAIL)
        h["operative_text"] = op[:a] + NEW + op[b:]
        h["what_changes"] = (h.get("what_changes") or "").rstrip() + (
            "  **R49 addendum S1\u2013S3**: (k) now names which mechanism handles which failure \u2014 the "
            "floor is the **terminal backstop** for the degenerate case, the reconciliation is the "
            "**operative protection** against gradual narrowing, because N\u2009\u2265\u20091 is satisfied by "
            "scoring one column. **(k2)(i)** adds the only bar that is registerable: every ground "
            "**names the artifact and location** behind it \u2014 quality of ground is not something a "
            "registration can require, provenance is. **(k3)** now states the verifiability limit "
            "outright: the map ships and the fixture does not, so a reader can check completeness, "
            "internal consistency and provenance, and cannot verify a classification against the "
            "data. It is a disclosure obligation with limited external verifiability and says so.")
        n += 1
assert n == 1, "hunk match %d" % n
json.dump(d, open(hp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("SC-4 hunk        : operative text and what_changes updated")

s2 = ssf.read_text(encoding="utf-8")
d2 = json.loads(hp.read_text(encoding="utf-8"))
assert sum(1 for h in d2["hunks"] if NEW in (h.get("operative_text") or "")) == 1
assert new_q in s2 and old_plain not in s2
print("AGREEMENT PROVEN : revised (k) in source (quoted) and in exactly one hunk; old text gone")
