# §10 — R23 GROUND TRUTH, ESTABLISHED BEFORE ANY LITERAL WAS TOUCHED

**Nothing was fixed. §10.1 held: the count was derived from the operation, never read off the
literals.**

---

## §10.2 — THE ENUMERATION, AND THE TRUE COUNT

Derived from the two sources §10.2 names, independently, then cross-checked.

**Source 1 — the tag message's own content** (`CEREMONY_COMMANDS.md` §3.5, the format block
written to `tagmsg.txt` at tag time). Six `<64 hex>  <path>` lines, enumerated by path.

**Source 2 — R15's single-operation hashing step** (§3.4, C2):
`for f in $FILES; do printf '%s  %s\n' "$(git show ":$f" | sha256sum | cut -d' ' -f1)" "$f"; done | tee v30a.hashes.txt`,
where `$FILES` is set once at §3.2 l.180.

**The two sources agree, path for path and in order:**

| # | path | in v30? |
|---|---|---|
| 1 | `PREREG.md` | yes |
| 2 | `DESIGN.md` | yes |
| 3 | `HISTORY.md` | yes |
| 4 | `tools/check_registration.py` | yes |
| 5 | `protocol/runtime_reference.py` | yes |
| 6 | `AVAILABILITY_DECLARATION.md` | **no — new at v30a** |

**TRUE COUNT: 6.**

Chained shut by three further gates that each read the same list: **C2e** (independent reader,
working tree vs index), **C2f** (`tagmsg.txt`'s hash lines equal `v30a.hashes.txt`), **C1c** (the
*signed object*'s hash lines equal `v30a.hashes.txt`). Nothing in the chain reads a numeral.

**The operative object is the LIST, not the number.** Every gate in the ceremony — C2a, C2b, C2c,
C2, C2e, C2f, C1c — iterates `$FILES`. The numeral "six" is a word-count of that list, restated in
prose. That is the whole R23 defect in one sentence, and it is why §10.4's detector is the right
shape.

**Verified against the executed precedent, read from the repository this pass:**
`git cat-file tag prereg-v30 | grep -cE '^[0-9a-f]{64}  '` returns **5**, paths 1–5 above, in that
order. `README.md` ll.31–35 mirrors the same five. The v30a six is the v30 five as a verbatim
prefix plus the declaration appended last, exactly as §3.2 states.

---

## §10.3 — DO THE LITERALS AGREE? **NO. HALT.**

**39 count-literal sites carry FIVE distinct asserted values.** This is not one decided value
restated stalely; it is four separate specifications of the hashed set, two of them live.

| value | asserted where | status |
|---|---|---|
| **TWO** | `PREREG.md:97` (§0.2.1) — *"signed tag, **both** file hashes in the tag message"* | **REGISTERED TEXT.** Uneditable. R7 rules it "a stale count predating `HISTORY.md` and the tooling files joining the block" |
| **THREE** | `PREREG.md:1050` (§11 item 3) — *"SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md` as committed in the tag message and the README"* | **REGISTERED TEXT.** Uneditable. An **enumeration by path**, not a count |
| **FIVE** | `AVAILABILITY_DECLARATION.md:3833` (R7) — *"**R7. hash-count:** the v30a tag message carries ALL FIVE hashes, matching the prereg-v30 tag as executed."* | in the hashed declaration, in a block headed *"Verbatim from the delta"* |
| **SIX** | §D.2 (`:3589`, `:3602`, `:3624`), `:993`, `:3811`; `CEREMONY_COMMANDS.md` x13; `COMMIT_PLAN.md` x5; `DEVIATIONS_DRAFT.md` x3 | what the ceremony is written for |
| **SEVEN** | `COMMIT_PLAN.md:346`, `:357`, `:428` (blocker item 8, **AUTHOR / decision**); `CEREMONY_COMMANDS.md:191` | **OPEN AUTHOR DECISION, undecided** |

**Sites that say "five" about the *v30* tag are correct and are not counted as disagreement**
(decl `:3591`, `:3610`, `:3811`; `CC:185`, `:227`; `CP:100`, `:365`, `:387`; `DD:290`). Those
describe the executed precedent accurately. **The disagreement is the five values above.**

### The disagreement is not cosmetic — the two registered values conflict with the executed act

`PREREG.md:1050` names **three paths**. The **executed `prereg-v30` tag carries five**, including
`tools/check_registration.py` and `protocol/runtime_reference.py`, which §11 item 3 does not name.
So either §11 item 3 is a **floor** (a superset satisfies it) or it is an **enumeration** (the v30
ceremony already exceeded its own registered specification). **The registered text does not say
which**, and `PREREG.md:97`'s "both" cannot be reconciled with either reading.

### G2 TRIP — this is a Class C question, not a description fix

§9.2's test is met literally. To correct `AVAILABILITY_DECLARATION.md:3833` I would have to decide
**what R7 means**:

- §D.2 reads R7 as ruling on the **inheritance** — that all five v30 hashes carry forward (against
  §0.2.1's "both"), leaving room for a sixth. Under that reading R7 is true and needs no fix.
- R7's own text labels itself **`hash-count:`** and predicates *"the v30a tag message carries ALL
  FIVE hashes"* — a statement about the message's total. Under that reading R7 is false of the
  message §3.5 specifies, and §D.2 contradicts a ruling it cites as its own basis.

Choosing between those is deciding what the amendment means. Writing either correction requires
the sentence *"R7 probably intended..."*. **§9.2 says stop there and not write the sentence.**

Compounding it: R7 sits under the header *"Decision log — working resolutions (DELTA R2,
2026-08-10; **PROVISIONAL until the prereg-v30a tag is signed**) ... Verbatim from the delta"*.
It is a verbatim transcript of an author instruction. Editing it falsifies "verbatim"; leaving it
ships a hashed document that contradicts its own §D.2. **Neither is mine to choose.**

**Both guards fire on the same site: §10.3's disagreement branch and §9.1's G2.**

---

## COLLATERAL DEFECTS FOUND WHILE ESTABLISHING GROUND TRUTH

Reported, not fixed. Each verified from disk this pass.

**(a) BLOCKING AT CEREMONY TIME — the staging plan omits two of the six.**
`COMMIT_PLAN.md` §4's three `git add` invocations are
`PREREG.md DEVIATIONS.md HISTORY.md DESIGN.md README.md` / `AVAILABILITY_DECLARATION.md` /
`evidence`. **`tools/check_registration.py` and `protocol/runtime_reference.py` appear in none of
them**, and V1's EXPECT list omits both. `git status --porcelain` **this pass** reports
` M tools/check_registration.py` — a hashed file, modified, that the plan never stages. At ceremony
time **C2b halts** ("modified in the working tree but not staged") and **V2 halts** ("Any remaining
` M ` line is a hashed file edited after staging — STOP"). §3.3 describes this exact trap as "the
check the whole operation turns on".

**This is directly in §10.4's path: adding the detector to `tools/check_registration.py` modifies a
hashed file the staging plan does not stage.**

**(b) The delegation target does not exist.** `CEREMONY_COMMANDS.md:188` — *"The six/seven question
is open and is `COMMIT_PLAN.md` §3.3's, not this file's."* `COMMIT_PLAN.md` has **no §3.3**; §3 is
the H-34 ID collision. The question lives at **§6**, which says so itself (*"carried forward from
§3.3, restated"*). A shipping file routes the one open author decision to a section that was
renumbered away.

**(c) Three stale line citations, all off by exactly +169.** `§D.2 (l.3420)` at
`CEREMONY_COMMANDS.md:183`, `COMMIT_PLAN.md:356` and `DEVIATIONS_DRAFT.md:290` — §D.2 is at
**3589**. `R7 ... (l.3664)` at `COMMIT_PLAN.md:386` — R7 is at **3833**. 3589−3420 = 3833−3664 =
**169**: the declaration grew 169 lines above both anchors and no citation was re-derived. Same
shape as H-L17.

**(d) A circular instruction in §3.5.** *"`README.md`'s new v30a block is filled from
`v30a.hashes.txt` the same way, and is staged and committed **before** C2 runs."* `v30a.hashes.txt`
is **C2's output** (§3.4: "the only place any `prereg-v30a` hash value is produced"). README cannot
be filled from it before it exists. §11 item 3 puts the block "in the tag message **and the
README**", so this is the second locus of the same six — and its fill order is unexecutable as
written.

---

## §14.2 — THE LABEL SURVEY, AND WHY R7 STANDS

**Ruled by survey, not by intent. The G2 was real; the question proved determinable.**

**The distinction the survey turns on: a LABEL names the question; a PREDICATE answers it.** R7's
predicate is *"the v30a tag message carries ALL FIVE hashes"*, and the clause *"matching the
prereg-v30 tag as executed"* fixes "FIVE" to the v30 five. **Any set containing those five
satisfies it**, so it is TRUE of the six. The totality reading comes only from the label
`hash-count:`.

**Every labelled entry in the decision log, surveyed:**

| entry | label | does the label assert anything the body does not? |
|---|---|---|
| R1 | `ties` | no — names the question; body: default `available` stands |
| R2 | `boundary` | no — body: the measured floor(t−1)+1s boundary |
| R3 | `35-column` | no — body: documented-unverifiable assumption |
| R4 | `as-built defects (buy classifier, uint32 wrap)` | **closest case** — carries a *referent* (which defects), not a predicate. The body supplies the disposition |
| R5 | `weighted_mid` | no |
| R6 | `weighted_mid flavor` | no — differs from R5's label only to disambiguate topic |
| R7 | `hash-count` | **no** — a noun phrase naming the question; it does not say "the count is five" |
| R8 | `H-entry` | no |

**Verdict: labels are consistently topic tags. §14.2(b) fires. R7 STANDS UNAMENDED, §D.2's
inheritance reading is the literal reading, there is no contradiction, and nothing is edited.**

**The decisive structural evidence is not in the labelled entries at all.** Half the block carries
**no labels**: R9, R11, R12 and R13 are recorded as bare `**R9.**`, `**R11.**`, and put their
referents in the body. **If labels were normative, dropping them would drop content.** Their absence
is only intelligible if the label is an optional convenience tag.

**Independent corroboration, found rather than constructed:** §D.3's rule paragraph — written
before this survey and not derived from it — already describes R7 as *"reading 'both' as the
executed five, not as a licence to publish two"*. That is the inheritance reading, recorded in the
declaration months earlier.

**The verbatim block was not edited under any branch.** R7 is a transcript of an author delta;
editing it would falsify the word "verbatim" that introduces it.

---

## WHAT THE DEFECT ACTUALLY WAS

**Not one literal was arithmetically wrong once SIX was ruled.** Every "six" site was already
correct; the "five" sites are all correct statements about the *v30* tag; the registered "two" and
"three" are satisfied (see §D.3 (i) and (ii)). **The defect was structural, not arithmetic:** the
set was asserted independently in ~39 places instead of derived once, and independent assertions
drift apart — which is how one set came to carry five different values.

**H-L19.** A rule restated as a literal does not merely go stale — it **forks**. A count that is not
computed from the thing it counts is not a description; it is an independent claim, and independent
claims drift apart. The remedy is never a corrected numeral; it is a single authority plus a
detector that fails when a restatement disagrees with it.

---

## VERDICT (superseded — recorded as the state at the R67 halt)

**§10.3 HALT (literals disagree, five values) + §9.1 G2 TRIP (correction requires deciding what a
recorded ruling means).** *Resolved by §14: SIX ruled, R7 resolved by survey.*

Per R66 §0.4, nothing past this executes. **§10.4's detector is not written** — §10.4 says the
detector must "verify the fix", and there is no fix to verify until the author fixes the count.
**§10.5 is not reached.** §11.2–§11.7 are not started.

**No literal was edited. No count was adjusted toward the literals. `PREREG.md` untouched.**
