# f4 — POINTER, not a copy

**Written:** 2026-08-12. Replaces `f4\availability_declaration_DRAFT.md`, which was a full
byte-duplicate of the declaration and has been deleted from this tree.

## The normative copy

**The one normative copy of the availability declaration is the repository-root file
`AVAILABILITY_DECLARATION.md`.** There is no second copy anywhere under `evidence\`, and none
may be created. This directory holds this pointer and nothing else.

    path:   AVAILABILITY_DECLARATION.md          (repository root; one level above evidence\)
    sha256: d26d8d5e8885639f03c70e526cc6b3c0aa68ab1f78b53b8ab4868a291f278275
    bytes:  329950
    as of:  2026-08-24, at the writing of this hash block (R67/§14.3(c): the three §D.3
            interpretation entries for the registered hash-set language; supersedes the
            2026-08-21 block, which supersedes the 2026-08-20 v30a scrub block below)

That hash is also the `../AVAILABILITY_DECLARATION.md` line of `evidence\MANIFEST.sha256`, and
the two are generated in the same pass. `sha256sum -c MANIFEST.sha256`, run from inside
`evidence\`, verifies the declaration through that line. **If the recorded hash and the file
disagree, the file wins and the record is stale** — a pointer records where authority lives,
it does not confer it.

**2026-08-26 (v30a closeout) — the current bytes.** The declaration moved from `10b65a00…` / 309,001 bytes to `d26d8d5e…` / 329,950 bytes / 4332 lines, on the §D.2 hash-enumeration rewrite, §D.5's named open obligations, §D.6's five deployed disclosures, §D.1's repository path for the pinned producing code, and §146.2's frame extension to the tag message. **Rewritten in the same pass that moved the declaration, per R15.** Values derived with `sha256sum` and `wc`, never transcribed.

**2026-08-26 (author sign-off) — the current bytes.** The declaration moved from `059fe270…` to `10b65a00…` / 309,001 bytes / 4027 lines when §D.1 recorded the F3 manifest's sign-off and re-pinned its bytes. **Rewritten in the same pass, per R15.**

**2026-08-25 (R99) — the current bytes.** The declaration moved from `ea46404d…` / 307,917 bytes to `059fe270…` / 308,491 bytes / 4019 lines, when §D.1's exhaustive freeze list gained the F3 fixture manifest, pinned by path and by SHA-256. **Rewritten in the same pass that moved the declaration, per R15.** Values derived with `sha256sum` and `wc`, never transcribed.

**2026-08-25 (R99) — the current bytes.** The declaration moved from `24c8a627…` / 305,634 bytes to `ea46404d…` / 307,917 bytes / 4012 lines, when §D.1's exhaustive freeze list gained the F3 fixture manifest, pinned by path and by SHA-256. **Rewritten in the same pass that moved the declaration, per R15.** Values derived with `sha256sum` and `wc`, never transcribed.

**2026-08-25 (R95) — the current bytes.** The declaration moved from `4c07c76f…` / 303,643 bytes / 3,982... to `24c8a627…` / 305,634 bytes / 3982 lines, when it gained the §146.2 line-reference frame and the §148.1 walk frame. **Rewritten in the same pass that moved the declaration, per R15** — a pointer hash carried forward from an earlier sync is prohibited. Values derived with `sha256sum` and `wc`, never transcribed.

**2026-08-21 (R48) — the current bytes.** The declaration moved again, from `ddbf7f2d…48d6` / 287,480 bytes / 3,796 lines to `723566d9…8dc2` / 296102 bytes / 3,854 lines, on three corrections: §A.5's statement that no cross-tool comparison had been run (false when written — one ran on 14 Aug 2026 and does not satisfy §9.2), §A.1 item 2's model-family claim (false against its own cited source), and a new §A.1 item 4 registering **ex ante** that the post-fix trio has no originating counterpart. The manifest line and this hash block were rewritten **in the same pass**, which is what R15 requires and what failing to do produced the drift recorded below.

**Provenance of the current bytes — HISTORICAL RECORD, NOT A PROCEDURE.** *(Rewritten
2026-08-13 after an independent verification found this paragraph asserting, in the present
tense, the very operation the R18 INVARIANT below forbids. The operative sentence it used to
carry — "when the two differ, the repository-root file is refreshed from the build copy … never
the reverse" — is DELETED, not softened: under R18 there is no build copy for it to refer to,
and that sentence is a verbatim statement of the procedure that destroyed §A.6.0 once already,
recorded below.)*

What happened, in the past tense: on 2026-08-13 the repository-root copy was refreshed from a
then-live build copy under the transient scratchpad, byte-compared after writing (`cmp` exit 0,
sha256 equal on both sides). That was the last such refresh. It is recorded because the byte
provenance of the file matters, not because it describes anything that may be done again.

**The current rule is the R18 INVARIANT below: the repository-root file is edited in place,
there is no build copy, and nothing is ever copied over the root.** Where this historical
paragraph and the invariant appear to differ, the invariant governs and this paragraph is
history.

**2026-08-20 — the v30a declaration scrub, recorded under the invariant.** The repository-root
file was **edited in place**, by content-matched substitution with a match-count assert on every
hunk: one prerequisite hunk at §A.6.0, then the seventy-one hunks of the v30a scrub — seventy-two
in all, each asserted to match exactly once, none applied by line number, none forced. **Nothing
was copied over the root**, and the applier refuses to write if any assert fails. The file moved
from `f0829bd3…3310` / 277,411 bytes / 3,684 lines to `ddbf7f2d…48d6` / 287,480 bytes / 3,796
lines. The intermediate state after the prerequisite was checked against the scrub's own declared
base (`1290186e…1c30`, 3,695 lines) before the scrub hunks were applied, so both legs are pinned
rather than only the endpoint. **Both frozen regions were verified byte-identical across the
pass**: the T2 addendum block (6,229 bytes) and the decision-log tail (4,595 bytes). The hash
block above and the `../AVAILABILITY_DECLARATION.md` line of `MANIFEST.sha256` were rewritten in
this same pass, as R15 requires.

*(Recorded late, and the lateness is the point: the hash block above carried `f0829bd3…` for one
round after the scrub landed. R15 prohibits a hash carried forward from an earlier sync, and this
pointer is the artifact that prohibition is about. The rule held for the manifest line, which was
rewritten with the declaration, and failed here — one half of a "rewritten in the same pass,
always" pair is not the pair. Both halves are now rewritten together, and a check that the pointer
and the manifest agree belongs in the pre-ceremony verification rather than in a reader's memory.)*

## Why a pointer and not a copy — R14

Working resolution **R14 (single normative copy)**: the repository-root
`AVAILABILITY_DECLARATION.md` is the ONE normative copy; the evidence tree carries a pointer
plus a recorded hash, never a duplicate file.

**The lesson this repeats.** `HISTORY.md` records v23 as an author-initiated restructure taken
on the parallel review's diagnosis — *"the measurement layer's generator named as duplicated
authority plus collapsed axes."* Duplicated authority was the defect: two artifacts entitled to
answer the same question, with nothing in the structure deciding which one governs. The fix was
not to synchronise them more carefully. It was to leave exactly one.

**The recurrence, measured.** Before this pass, `f4\availability_declaration_DRAFT.md` and the
repository-root `AVAILABILITY_DECLARATION.md` were byte-identical at
`e95063f4503180bd10fd2f83d028ab047962cb4251a73180ed0c26b5ff6ae076` (176209 bytes) — and both
were **stale**. The live draft had moved to `d1f43f51…` (215256 bytes) in the R11-batch pass,
which rewrote the header's Fixture paragraph and added Part II §0, §13(i), §13(j) and the §C.3
scope rewrite. Two copies agreeing with each other and disagreeing with the source is the exact
failure mode duplication produces: the agreement reads as corroboration, and
`sha256sum -c MANIFEST.sha256` would have returned **OK on both lines** while the declaration
under verification was a version behind. A near-miss, not a miss — nothing was tagged on those
bytes — but it is the v23 defect recurring in a new layer, which is why the structural fix is
applied here rather than a reminder to keep the copies in sync.

**The hashes recorded above are current, not historical.** `d1f43f51…` (215256 bytes) appears in
the paragraph above only as the state at the moment R14 was applied; it is **not** the current
declaration. The R18 five-defect correction pass of 2026-08-12 — 14 anchored edits, ledger at
`fixture_spike\finalfix\R18_five_defect_ledger.txt` — moved the draft to `f4abf851…`
(224596 bytes, 3059 lines), and the repository-root file was restaged from it in the same pass
that rewrote this pointer's hash block and the `../AVAILABILITY_DECLARATION.md` line of
`MANIFEST.sha256`. That is R15 operating as intended: a recorded hash is computed at write time
from the bytes then on disk, never carried forward from an earlier pass.

**A further pass followed R18, and this pointer recorded its state until the 2026-08-13 restage
below.** The confirming verification of the R18 pass found two residual defects — §A.10 item 2
still admitted a false-positive reading onto the UNSCORED class, and §13(j) item 4 quoted a peak
without naming its metric — both fixed by the orchestrator on 2026-08-12 in two anchored edits.
That moved the declaration to `18d08e0e…` (225675 bytes, 3072 lines), which was the hash block
at the top of this file and the `../AVAILABILITY_DECLARATION.md` line of `MANIFEST.sha256` until
the 2026-08-13 restage recorded below. Both frozen regions were re-verified byte-identical to
`_snapshots\PRE_R9_HASHES.txt` after those edits (T2 block `d4dd09b9…`/6170 B; decision-log tail
`059bbb1d…`/5744 B).

**Correction recorded in place, per the rule that a record is amended openly or not at all.**
While updating this pointer the orchestrator replaced every occurrence of the old byte count
mechanically, which briefly rewrote the historical sentence above to attribute 225675 bytes to
`f4abf851…`. That was wrong — `f4abf851…` is 224596 bytes — and the sentence has been restored.
No hash was altered by that slip, and no other statement in this file was affected.

**2026-08-13 — R14/R15 restage, and the repair of an R14 miss.** On entry to this pass the
repository-root declaration was `32c7c415…` (233302 bytes, mtime 2026-08-13 07:27) while **both**
R14 records — this hash block and the `../AVAILABILITY_DECLARATION.md` line of `MANIFEST.sha256`
— still read `18d08e0e…` (225675 bytes). The declaration had been changed in a pass that rewrote
neither record, so the manifest's declaration line could not have verified against the bytes on
disk. That is the R14 two-record rule missed rather than near-missed, and it is recorded here
rather than quietly corrected. The repair: the repository-root file was restaged from the live
build copy, which had itself moved on to `e4dd1e52…` (266848 bytes, 3566 lines); `cmp` returned
exit 0 and both sides hash equal; this hash block and the manifest line were then rewritten from
those bytes, computed at write time, in this same pass. The intermediate `32c7c415…` state was
never a recorded state and is named here only so the gap in the record is legible.

**Two further changes in the same pass, neither of which touches this pointer's subject.** (1)
The evidence tree gained 26 files — `fixture_spike\s13\` (18), and the three build directories
that sit beside `fixture_spike\` in the transient scratchpad rather than inside it:
`ceremony\` (4), `author_review\` (1), `errata\` (3) — each copied byte-identical under the
standing exclusion rules (nothing over 20 MiB, no `.pkl`, no `__pycache__`). (2) `MANIFEST.sha256`
gained a **second** `../` line, for the repository-root `PRIOR_ART_VERIFICATION.md`
(`b97a2804…`, 3610 bytes), which the ceremony commits and which no manifest line previously
covered. Neither change creates a second copy of the declaration, and the build-source
`f4\availability_declaration_DRAFT.md` remains outside this tree.

**2026-08-13, later the same day — the `32c7c415…` gap RESOLVED, and what it contained recovered.**
The paragraph above named `32c7c415…` (233302 bytes) as an unrecorded intermediate state and
restaged over it from the build copy. That restage was correct in form but it discarded content:
`32c7c415…` was **larger than the build copy it was overwritten from** (233302 vs 225675 bytes),
so roughly 7.6 KB existed only in the repository-root file. No copy of those bytes survived
anywhere on disk — the file is untracked, so git held no history of it, and a filesystem-wide
search for a 233302-byte file returned nothing.

The content was recovered from the session transcript that produced it
(`33e8c843-30fa-4bfb-aa9f-814c77bdb2e6.jsonl`, line 20988): a single `Edit` replacing a
326-character anchor with 7939 characters — **§A.6.0, the DERIVATION RULE** for the three gate
classes, which states the rule that *yields* the enumeration (REQUIRED iff the construction
carries the wall-clock `ts_floor` join and is not degenerate-constant; OUT OF JURISDICTION iff it
reads only same-row book/clock values, availability-legal at the boundary under R1; UNSCORED iff
degenerate-constant or unconstructible under T4) so that the enumeration is derivable rather than
asserted. Its loss would have been substantive, not cosmetic: without it the three lists are
assertions a reader must take on trust.

The recovered edit was re-applied to the live build copy against the same anchor (match count 1,
verified unique), the repository-root file was restaged from it, and this hash block and the
`MANIFEST.sha256` lines were rewritten from those bytes in the same pass. Current state:
`456f5568…`, 274475 bytes, 3651 lines; §A.6.0 present exactly once; both frozen regions unchanged
(T2 block `d4dd09b9…`/6170 B, decision-log tail `059bbb1d…`/5744 B); `sha256sum -c` exit 0.

**Two method consequences, recorded because the near-miss was structural rather than careless.**
(1) A restage that copies build → root is only safe when the root is not ahead of the build copy;
the direction must be checked, not assumed, and a root larger than its source is a stop condition.
(2) The R14 single-copy rule removed the *duplicate-authority* failure but introduced a
*direction* failure in its place: with one normative copy fed from a transient source, an edit
made directly to the normative copy is invisible to the next sync and is destroyed by it. Both
are candidates for the ceremony record and for the HISTORY lesson list alongside H-L12/H-L13.
Also recorded: this pointer's hash block was updated by targeted replacement of the two record
lines only — the blanket byte-count replacement that corrupted a historical sentence earlier in
this file was not repeated.

**2026-08-13 — R18/R19 implemented. The loss class is now closed structurally, not procedurally.**

The recovery recorded above detected the failure. Detection was not enough: the same restage
would have destroyed the same content again on the next pass. Two changes make it unreachable.

**R18 — there is no build copy.** The transient build copy
`fixture_spike\f4\availability_declaration_DRAFT.md` has been retired to
`fixture_spike\_retired\availability_declaration_DRAFT.RETIRED-2026-08-13.md` — a name chosen so
it cannot be mistaken for a source — after byte-equality with the repository-root file was
confirmed (`456f5568…`, 274475 bytes, identical on both sides at the moment of retirement). The
repository-root `AVAILABILITY_DECLARATION.md` is now the ONLY live copy.

> **INVARIANT.** The repository-root `AVAILABILITY_DECLARATION.md` is edited **in place**. No
> process copies any file over it, and no build copy of it exists to copy from. Synchronisation
> runs in ONE direction only — root → evidence records (this pointer's hash block and the
> `../AVAILABILITY_DECLARATION.md` line of `MANIFEST.sha256`) — never into the root. A step that
> would write the root by copy is a defect in the procedure, not an operation to perform: halt
> and report instead. **Root-ahead-of-source cannot arise, because there is no source.**

**R19 — the declaration is under version control.** `AVAILABILITY_DECLARATION.md` and
`PRIOR_ART_VERIFICATION.md` were committed locally (commit `ffa6d94`, no push, no tag) BEFORE the
ceremony, so the declaration now has git history. Had it been tracked when the overwrite occurred,
recovery would have been `git show` rather than a search of session transcripts.

**The two lessons, recorded in open form (candidates for the H-L list alongside H-L12/H-L13).**

1. **Authority without direction is not a single-source rule.** R14 named one normative copy and
   removed duplicate authority — the v23 defect — but left the *direction* of synchronisation
   unstated. With one normative copy fed from a transient source, an edit made directly to the
   normative copy is invisible to the next sync and is destroyed by it. Naming which artifact
   governs is only half the rule; the other half is naming which way bytes may move.
2. **An authoritative file outside version control has no history, and recovery then depends on
   incidental transcripts.** The declaration was the most-reviewed artifact in the project and the
   only one not tracked. Its recovery succeeded because a session transcript happened to retain
   the edit — an artifact never intended as a backup, retained for unrelated reasons. That is luck
   standing in for a mechanism.

**What the rule forbids, concretely.**

1. No second copy of the declaration under `evidence\` — not as a draft, not as a snapshot of
   the current text, not under another name.
2. Anything under `evidence\` that needs the declaration **cites** it by path and by the hash
   recorded here and in `MANIFEST.sha256`; it does not reproduce it.
3. The one permitted exception is a **frozen historical snapshot**, which must be named for the
   state it froze and must never be a candidate for "the current declaration".
   `fixture_spike\_snapshots\availability_declaration_PRE_R9.md` is such a snapshot: it is a
   record of the pre-R9 text, is not maintained, and is not this file's subject.
4. When the declaration changes, exactly two records are rewritten in the same pass: this
   pointer's hash block and the `../AVAILABILITY_DECLARATION.md` line of `MANIFEST.sha256`. A
   hash carried forward from an earlier pass is prohibited — the same prohibition working
   resolution **R15** places on the six tag-time hashes.

## Scope

This pointer is a build-record artifact. It states nothing normative about the availability
model, the information boundary, the declared ground-truth map, or any gate class. Every such
statement lives in `AVAILABILITY_DECLARATION.md`, and `PREREG.md` remains the sole normative
source for measurement semantics (`PREREG.md` §0.1: *"`PREREG.md` is the sole normative source
for measurement semantics"*).
