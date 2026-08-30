# Track B lessons

The review register in `HISTORY.md` closed at lesson 45 and is not reopened per
round. Track B's lessons accumulate here, plain and dated, for a considered
append later.

Each entry records what happened and what it costs to get wrong. Nothing here
creates, amends or narrows a rule; these are observations, not instructions.

---

## TB-01 — *(28 August 2026)* A merge can resurrect a defect that was deliberately removed

`phase1`'s copy of the checker carried the line-pinned citation form that R163 §3
ruled against and main had converted to an anchor. "Main wins" was the correct
resolution, and it was correct for a reason stronger than recency: importing the
older side would have undone a ruling.

The ruling had already been demonstrated by then, not merely argued. The anchored
citation moved three times as the register grew — 281, then 313, then 315 — and
resolved at each. The pinned form would have been stale by 36 lines at the first
of those and would have needed re-pinning at every append after.

**Every reconciliation with an older branch is a chance to reinstate something
that was removed on purpose, and the conflicts are only where that shows up
loudly.** The quiet cases are the files that merge cleanly because only one side
touched them. What made this one safe was checking, for each conflicted file,
whether the older side's unique content was superseded text or genuine work —
and the answer differed per file, so the question had to be asked per file.

Measured, for that merge: zero lines unique to `phase1` in the review register;
two in the checker, both the ruled-against form; four in the README, all pre-tag
hash values; thirty in the session record, a pre-tag snapshot; fifty-three in the
availability declaration, including a citation to a clause that does not exist.
Six files, six times the older side lost, and each time for a stated reason.

---

## TB-02 — *(28 August 2026)* An invariant can be asserted, cited, and unenforced

`src/leakaudit`'s docstring stated that the package "never accepts, imports, or
constructs `CaseLabels`" — the SC-7(c) separation every acceptance number
depends on — and cited `leakaudit.trace.assert_key_free` as stating it
executably. That module did not exist, and the string occurred nowhere else in
the repository.

The assertion was **true**: a complete AST enumeration over nine modules and
1,984 lines found no import, no bare `import protocol` (which would make the key
reachable by attribute), no dynamic import machinery at all, and the only three
textual occurrences inside docstrings. So nothing was ever wrong with the tool.
**A correct invariant with no check is still an unverified assertion**, and the
citation pointing at an absent file made it a false statement in the code
carrying the claim.

Two things this round is worth remembering for:

**The natural repair for the natural check is an exemption.** A text matcher
looking for `CaseLabels` flags the very docstrings that state the invariant, and
the obvious fix is to exempt them — which is the move this project spent a whole
close-out learning to refuse. Parsing removes the temptation rather than
resisting it: a docstring is a string constant, so it simply is not a reference,
and there is nothing to exempt. **Choose the instrument that has no false
positives to forgive.**

**The check that existed was shaped like a check and could not fail.** A text
scan in the probe suite tried to strip docstrings by splitting on triple quotes,
and its assertion carried `or True`. Its two live assertions caught
`import CaseLabels` and `CaseLabels(` but not `import protocol...`, the
attribute route. It is now a delegation to the parser.

**A fix can be correct and still have a second-order cost.** Repointing the
fixture path into `evidence/` made Python write `__pycache__` there, and the
evidence tree is attested file by file, so two unattested files appeared and the
gate went to two findings. Measured, not anticipated. The import now suppresses
bytecode for its own scope. **When a fix moves work into an attested tree, ask
what the work leaves behind.**

---

## Open items — recorded, not acted on

- **Whether SC-7(c) belongs in the registration gate.** A pytest-only check is
  weaker than a gate check: the gate is what the registration binds, and a suite
  can be skipped where the gate cannot. Adding it changes a registered instrument
  and would surface in the delta-of-findings comparison against the frozen
  checker. Deferred to the D2 subsystem — discriminator, window, relative-root
  defect — which touches that instrument anyway, so the two changes are ruled and
  disclosed together rather than separately. Raised R175 §6.
