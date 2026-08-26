# Z1 / Z2 / Z5 — THE THREE RECORDS, DRAFTED

**STAGING ONLY. Nothing applied.** `HISTORY.md` was read, not edited; it stands at
`c597f653469f42df867321c0db81fb55e3ec66e5194909db3f3daa1e9088f0a0`, 313 lines. These entries land
at the ceremony, with `HISTORY.md`'s other open items, so the file takes one hashed state rather
than several unhashed ones (the reasoning `errata/HISTORY_L5_R26_FIRING_STAGED.md` §4.2 gives, which
applies unchanged).

**What changed from the staged draft.** `errata/HISTORY_L5_R26_FIRING_STAGED.md` §3.1 variant A was
written when the 13 August decision was understood as a **firing** of §10.2's criterion 5 whose
consequence was **deferral of the release**. Both halves are now withdrawn by the author:

- **"stop" in line 1042 attaches to the WORK, as registered.** The sentence's own "and resume after
  1 November" is the resumption. Reading it as deferral of the release alone *softens* a registered
  consequence, and the declaration's §D.3 forbids resolving locked text toward the weaker reading
  (declaration lines 3478–3482: "A decision-log interpretation of locked text may resolve ONLY toward
  the STRONGER reading. Any interpretation that weakens a locked obligation … is a class C amendment
  and may not be recorded as a working resolution."). The stronger reading is taken; no amendment is
  made; the criterion keeps its registered text and its registered consequence.
- **The 13 August decision is a FORECAST, not a firing.** Criterion 5 is date-gated — "A date, not a
  phase number" — and a date-gated criterion cannot be evaluated before its date. What the author
  determined on 13 August is that the 15 October condition will not be met. That determination
  releases schedule pressure on the amendment work. It alters no registered consequence, and it does
  not consume the criterion: criterion 5 still evaluates on 15 October, on its own terms.

**Consequence for the amendment.** SC-14 is withdrawn. No clause amends §10.1's criterion 5 or
§10.2's criterion 5. The v30a diff loses one hunk and gains none.

---

## 1. Z5 — the ledger entry, variant A reframed

**Numbering.** `HISTORY.md`'s highest main-series entry today is **H-34** (`grep -oE '^### H-[0-9]+'`
→ H-30 … H-34; `grep -c 'H-35'` → 0). **H-35 is claimed by the amendment entry** (`ceremony/H34_DRAFT.md`
§1, `ceremony/COMMIT_PLAN.md` §3, `ceremony/CEREMONY_COMMANDS.md` A4), so this entry is **H-36
provisionally**. If the amendment entry does not land, this one takes **H-35**. Assign at landing, as
the IDs always have been.

**Date.** Recorded 20 August 2026 — the day recorded, not the day worked, the convention H-L12 fixed
(`HISTORY.md` l.218). If the ceremony lands on a later day, the operator sets that day instead; the
decision date, 13 August 2026, does not move.

**Insertion point.** Unchanged from the staged file §4: immediately before `### H-B addendum — firings
v18 through v30` (occurs exactly once), after H-35 if H-35 has landed, otherwise after H-34's closing
`---` and its two blank lines. Assert the anchor's match count is 1 before and after the edit (H-L11).

```markdown
### H-36 — from `PREREG.md` §10.2 (kill criterion 5, ship-by date)

*(Recorded 20 August 2026 — dated by the day recorded, not the day worked, the convention H-L12 set — for the author's decision of 13 August 2026, which is a FORECAST and not a firing. §10.2's criterion 5 — "Not installable by a stranger by 15 October → stop and resume after 1 November" — is date-gated, "A date, not a phase number", and a date-gated criterion cannot be evaluated before its date. What the author determined, nine weeks ahead of it, is that the condition will not be met: the tool will not be installable by a stranger by 15 October. The reason is the amendment's growth — a fixture replacement under §6.2 became a schema registration, `PREREG.md` taking the generic clauses and the declaration supplying the data, plus a separate replacement for §10.2's criterion 2, which §10.2 requires committed before any development-corpus contact. Registering those against a ship-by date would mean registering crisis-drafted rules. What the forecast changes is schedule pressure, and nothing else: the criterion keeps its registered text and its registered consequence, and it evaluates on 15 October on its own terms. Its "stop" attaches to the work, as registered, and the sentence's own "and resume after 1 November" is the resumption — a narrower reading, releasing only the ship-by date, would soften a locked obligation, which §D.3 of the declaration forbids resolving toward. September stays blocked for Concept A and the 1 November application is untouched. No criterion of §10.2 has fired; this is not a firing of §0.2's stopping rule either, so H-B's enumeration does not move.)*
```

**Word count: 249** (backticks and asterisks stripped). Longer than variant A's 201 because the
forecast/firing distinction and the §D.3 ground are both load-bearing and neither can be dropped
without leaving the entry ambiguous about what happened. A 150-word compression is available on
request; it loses the §D.3 sentence.

**Every clause traces to a source.**

| Clause | Source |
|---|---|
| "dated by the day recorded, not the day worked" | `HISTORY.md` l.218 (H-L12), quoted |
| the criterion, verbatim | `PREREG.md` l.1042 |
| "A date, not a phase number" | `PREREG.md` l.1042, quoted |
| "nine weeks ahead" | 13 Aug → 15 Oct 2026 = 18 + 30 + 15 = 63 days = 9 weeks exactly |
| the amendment's growth; crisis-drafted rules | the author's decision of 13 August 2026, in substance |
| "which §10.2 requires committed before any development-corpus contact" | `PREREG.md` l.1031, l.1033 |
| "§D.3 … forbids resolving toward" | `AVAILABILITY_DECLARATION.md` lines 3478–3482, in substance |
| September blocked; 1 November untouched | the author's decision of 13 August 2026 |
| H-B's enumeration does not move | `HISTORY.md` l.230; register determination in the staged file §1 |

**No chat-only identifier appears in the entry.** It says "the author's decision of 13 August 2026"
rather than naming the working resolution, for the reason the staged file gives at §0.1: an entry
that names a resolution recorded only in a planning transcript cites something a reader cannot reach.

---

## 2. Z2 — the twin-criterion-5 registration defect

**Record it, do not fix it in v30a.** No renumbering. The entry below is a ledger note in the same
main series; it takes the next free ID after H-36 — **H-37 provisionally**, assigned at landing.

```markdown
### H-37 — from `PREREG.md` §10.1 and §10.2 (two criteria numbered 5)

*(Recorded 20 August 2026. `PREREG.md` numbers a criterion 5 twice: §10.1's fifth kill-gate condition, "Has had a release or commit within the previous 12 months" (l.1024), and §10.2's fifth kill/pause criterion, "Not installable by a stranger by 15 October" (l.1042). The two share no subject, no trigger and no consequence, and the documents around them already cite both — H-34 cites §10.1's, H-36 cites §10.2's. A bare "criterion 5" is therefore ambiguous everywhere in this repository, and the ambiguity is live rather than theoretical: a v30a clause was drafted against §10.1's criterion 5 when §10.2's was meant, and would have amended the collective outcome of the prior-art kill gate — converting "stop building and contribute upstream" into a deferral — had the scope question not been asked before it landed. The defect is the numbering, not either criterion: §10.2's list runs 2, 3, 4, 5 with no item 1, so its numerals were never independent of §10.1's. **Recorded as a registration defect for a future amendment; v30a does not renumber**, because renumbering a registered criterion is itself a class C change and would invalidate every citation of both numbers written to date. The working rule until then: never write bare "criterion 5" — write "§10.1's criterion 5" or "§10.2's criterion 5".)*
```

**Why a ledger note and not a `PARKING_LOT.md` or `DEVIATIONS.md` entry.**
`PARKING_LOT.md` is constrained by `PREREG.md` §11 item 1 to the single §13.9 entry, and
`check_parking_lot` enforces that over every line — a second entry is a checker failure, not a
record. `DEVIATIONS.md` cannot carry it either: a class C object may not be recorded there
(`PREREG.md` l.1033, "No `DEVIATIONS.md`-only criterion"), and the checker's own scope comment says
a rule-shaped line in `DEVIATIONS.md` is by construction a class C change in the one place §0.2.1
forbids. The main series is where errata against a locked clause live — "what a version said and
what it cost" — which is exactly this.

---

## 3. Z1 — what is NOT recorded, stated so the absence is deliberate

- **No `PREREG.md` amendment.** SC-14 is withdrawn; neither criterion 5 is amended, marked, or
  re-read. The registered text of both stands byte-exact and operative.
- **No `DEVIATIONS.md` entry.** The staged file raised one as a possibility under the reading where
  the author narrows a registered consequence. Z1 takes the other reading — the registered
  consequence is not narrowed — so there is no departure to record. `DEVIATIONS.md` stays 0 bytes
  until D-001 lands at the ceremony.
- **No ledger-count movement.** H-B's twenty-one firings, thirteen listed entries and twenty-three
  entries counted are untouched: a forecast is not a firing of §10.2's criterion 5, and it is not a
  firing of §0.2's stopping rule.
- **No withdrawal of H-34.** H-34 signs off §10.1's five-criterion prior-art gate, a different
  object, and its citation of `PRIOR_ART_VERIFICATION.md` (`b97a2804…e733bb`) was independently
  re-verified this pass against the file on disk. Nothing about the criterion-5 work touches it.

---

*Drafted at DELTA R33. Three entries, all staged. Landing is a ceremony step: H-36 and H-37 ride the
same `HISTORY.md` open as H-35 and D-001, so the file takes one hashed state.*
