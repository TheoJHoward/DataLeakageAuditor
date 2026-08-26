# A3 — THE GENERAL COUNT-LITERAL CLASS. SWEEP RESULT. **NOTHING FIXED.**

**A3.1's shape:** prose asserting a COUNT of a thing ENUMERATED elsewhere, with nothing tying the
two together. The hash set was one instance; `COMMIT_PLAN.md`'s "Three invocations" was another,
and it surfaced only because §15 changed the enumeration underneath it.

**Scope (A3.3):** the six-file set + manifest-carrying prose — `PREREG.md`, `DESIGN.md`,
`HISTORY.md`, `AVAILABILITY_DECLARATION.md`, `README.md`, `PRACTICES.md`,
`PRIOR_ART_VERIFICATION.md`, `DEVIATIONS.md`, `evidence/ceremony/*.md`. F1 holds.

---

## METHOD, AND ITS ADMITTED FAILURE MODE

A first pass matched "count word + set noun" and returned **162 candidates**, almost all noise
(`6 RULE` is a tier label; `2.6 A probe's…` is a section number).

A second pass reported a hit only where an enumeration was **found and measured**, so each hit is
checkable: **29 checkable sites, 4 agreeing, 25 disagreeing.**

**Then I hand-checked the 25, and the automation was wrong.** It pairs a count with *whatever list
follows*, not with the count's own enumeration. Every disagreement I verified was a pairing
artifact:

| site | claim | actual enumeration | verdict |
|---|---|---|---|
| `PREREG.md:332` | "**6 RULE**" | inline: L1.1, L1.2, L1.3, L1.4a, L3.1b, L3.2-with-groups = **6** | **AGREE** |
| `DESIGN.md:488` | "the four criteria" | `PREREG.md` §6.2 ll.459–462 = **4** | **AGREE** |
| `HISTORY.md:343` | "adds **eleven**, for twenty-one" | 13 `v**` entries − 2 marked *not a firing* = **11**; 10+11 = **21** | **AGREE** |
| `CEREMONY_COMMANDS.md:31` | "One of **four items**" | §0 table = **4** data rows | **AGREE** |
| `CEREMONY_COMMANDS.md:35` | "all **five criteria**" | `PREREG.md` §10.1 = **5** numbered criteria | **AGREE** |
| `CEREMONY_COMMANDS.md:46` | "the **two items** carried forward" | of the 4, two are unsatisfied (cross-tool, licence) = **2** | **AGREE** |
| `AVAILABILITY_DECLARATION.md:2825` | "**FOUR CATEGORIES**" | CATEGORY 1–4 present = **4** | **AGREE** |
| `AVAILABILITY_DECLARATION.md:2592`, `:2595`, `:2364`, `:3234` | "the **six** `mbo_*` classes" | `n1/declared_map.csv`: 6 scored `mbo_*` (`mbo_all_rows` is the 24-row diagnostic, correctly excluded) | **AGREE** |
| `AVAILABILITY_DECLARATION.md:3244` | "**four** `trades_*` classes" | `declared_map.csv` = **4** | **AGREE** |
| `AVAILABILITY_DECLARATION.md:2275`, `:3127` | "all **10** declared/event classes" | 6 `mbo_*` + 4 `trades_*` = **10**; 10 × 96 = 960, + 24 diagnostic = **984** ✔ | **AGREE** |
| `AVAILABILITY_DECLARATION.md:3721` | "these **three entries**" | §D.3 (i)(ii)(iii) = **3** | **AGREE** |

**Not individually hand-verified:** the remaining flagged sites in `PREREG.md` (`:449`, `:521`,
`:1038`) and `HISTORY.md:219`, `AVAILABILITY_DECLARATION.md:3071`. Their pattern matches the same
pairing artifact, but I am recording them as **unverified rather than clean** — an unverified site
is not a passing site (H-L15).

---

## THE FINDING

**No further live instance of the general class was found in the shipping corpus.** Two instances
existed and both are now fixed: the hash set (R67 §10/§16) and `COMMIT_PLAN.md`'s "Three
invocations" (R67 §15).

**`HISTORY.md:343` is the model this class should be written to**, and it was already there:

> "…adds **eleven**, for twenty-one. **Two entries are marked *not a firing*:** v19 and v23 …
> **A verifier counting entries rather than firings will get twenty-three; the reconciliation is
> here.**"

It states the count, points at the enumeration, **and pre-empts the most likely wrong recount.**
That is what a count that cannot be derived mechanically should look like.

`AVAILABILITY_DECLARATION.md` §C.3 does the same thing structurally — *"Each is derived from its own
source, enumerated by name, and counted. Every count below was verified this pass against
`f3\\fixture_manifest_DRAFT.json`…"*

---

## P2 CALLS (R66 §1.1) — and they all land the same way

**P2 asks whether a reader relying on the site reaches a wrong conclusion about what a gate tests,
a threshold or denominator, a pass/fail condition, or what an amendment changed.**

| site class | P2 | disposition |
|---|---|---|
| all 11 hand-verified sites above | **fails P2** — they are all **correct**, so no reader is misled | **no action** |
| the 5 unverified sites | **fails P2 pending** — 3 of 5 are in `PREREG.md`, which is registered and **cannot be edited** regardless | **POST-TAG ERRATA**; verify then |
| the class as a whole | **fails P2** — no gate reads any of these counts | **POST-TAG ERRATA** |

**A count is load-bearing when a gate executes against it.** The hash-set literals qualified because
C2/C2f/C1c run against the set at tag time. **A prose count of invocations, categories or classes is
read by a human, not by a gate.** None of the sites above is executed.

**So the default disposition A3.4 states in advance is the correct one on the evidence, and I am
not arguing against it:** **POST-TAG ERRATA.** I found nothing that would justify an exception, and
I want to be explicit that this conclusion did not depend on the list turning out short — it
depends on no gate reading any of these counts.

**One caveat worth stating rather than burying.** The five unverified sites are unverified because
I ran out of the round, not because I judged them low-risk. If any turns out to be *wrong* (not
merely unpaired), the P2 call on that one site should be remade — a wrong count in `HISTORY.md`
ships inside the hash set even though no gate reads it.

---

## H-L19, RECORDED

**A rule restated as a literal does not merely go stale — it FORKS.** One hash set carried five
different values across registered text, a hashed declaration and the ceremony package, each
locally plausible, because no site derived from the operation. **A count not computed from the
thing it counts is not a description; it is an independent claim, and independent claims drift
apart.** The remedy is never a corrected numeral: it is one authority plus a detector that fails
when a restatement disagrees — or, where the count cannot be mechanised, `HISTORY.md:343`'s form:
state the enumeration and pre-empt the wrong recount.

**Corollary (H-L19a): line-keyed references are the same defect.** Three citations were 169 lines
stale; writing §D.3 then drifted two detector exemptions by 64 lines **within the same round**.
Cite anchors; where a line key is unavoidable, pin it to content so drift is loud. The detector's
pins caught their own drift twice this round, which is the only reason it was not silent.
