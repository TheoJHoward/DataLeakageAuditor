# COMMIT ACCOUNTING — every commit between `prereg-v30` and the amendment commit

**What this is (R97/§158.2).** The ceremony no longer asserts a pinned `HEAD` value. It **derives**
the commit list between `prereg-v30` and `HEAD` and requires **every commit in it to be accounted
for here**, by hash, by what it did, and by why it belongs in the tagged tree.

**An unaccounted commit is a HALT. A new accounted commit is not.** That is the whole point: a
pinned literal breaks on legitimate work and tells you nothing; this reports the work and demands a
reason for it.

**Gate:** `C5b` in `CEREMONY_COMMANDS.md` §2. It matches on the **7-character short hash** in the
`account:` lines below.

---

## Base

`prereg-v30` → commit **`fe0d5a5708cfe1f817bd50e12a2cd02c2b4456ac`**. A tag never moves, so this is
the one value in the check that is safe to state.

## The accounted commits

- `account: 5842857` — **OpenTimestamps receipt for registration commit.** Commits the `.ots`
  receipt for the v30 registration commit. Belongs in the tagged tree because `PREREG.md` §11's
  integrity chain requires the external timestamp receipt to be committed, and a commit cannot
  contain the receipt for its own hash — so it lands in a follow-up commit, which is this one.

- `account: 0ee26c4` — **OpenTimestamps receipt upgraded: Bitcoin attestations at blocks 961654 and
  961656.** Replaces the pending receipt with the upgraded one carrying Bitcoin attestations.
  Belongs for the same reason: it is the completion of v30's timestamp obligation, and the amended
  tree must not drop v30's own integrity record.

- `account: ffa6d94` — **Track the v30a availability declaration and prior-art verification.**
  Brings `AVAILABILITY_DECLARATION.md` and `PRIOR_ART_VERIFICATION.md` into the tree. Belongs
  because the declaration is one of the **six files the v30a tag message hashes**, and a tag whose
  hash set names a file that is not in the tree is not a lock.

- `account: 80401d0` — **Kill-gate sign-off (H-34, prior art) with four factual corrections, plus
  review lessons H-L12 and H-L13.** One file, `HISTORY.md`, **+33 −0**, parent `ffa6d94` — verified
  from the commit at R97/§157.2, not from a report. Belongs because **H-34 IS the sign-off the tag
  depends on**: under the author's recorded routing of 25 August 2026 (branch (b)), the §9.2
  cross-tool comparison and the licence check gate **Phase 1 entry** and not the amendment tag, and
  H-34's verdict is what discharges the tag's side of §10.1. **A tag based on `ffa6d94` would
  exclude the record its own routing depends on.**

- `account: 0acab4e` — **Pre-registration v30a: §6.2 reference AUC, contamination-class locus,
  sliced CI variant, and criterion 3 — class C amendment (PREREG §0.2.1).** The amendment commit
  itself: the applied `PREREG.md`, the declaration carrying the F3 manifest's sign-off, the README's
  v30a hash block, and the evidence tree. Belongs because it **is** the thing the `prereg-v30a` tag
  is cut over.

- `account: 945433f` — **Ceremony: C2g's working-tree assertion becomes a derivation; Phase 1
  brief.** C2g's assertion was a hardcoded list of three untracked paths and it went stale the moment
  `LICENSE` and `tools/control_char_scan.py` entered the tree — both recorded, neither in the list.
  It now **derives**: every untracked path must be a ceremony artifact, on D10's ephemeral list, or
  recorded in `DEFERRED_ITEMS.md`, and it names the path and all three tests when it fails. Also
  carries `evidence/session/PHASE1_BRIEF.md`. Belongs because the tag is cut over a tree whose own
  verification step must not fail on recorded, accounted-for files — **a gate that cannot pass on a
  correct tree is not a gate**, and this is the second time a pinned expectation stopped this
  ceremony (H-L24).

  *A commit cannot account for its own hash, so the accounting for `945433f` lands in the commit
  after it — the same shape as the OpenTimestamps receipt, which cannot be inside the commit it
  attests.*

- `account: b3ed6f6` — **Pre-registration v30a … class C amendment (PREREG §0.2.1).** The ceremony
  commit produced by the R113 re-run: identical hashed content to `0acab4e`, carrying in addition
  the accounting for `0acab4e` and `945433f` and the updated evidence manifest. Belongs because it
  is the tree the re-run verified end to end — C2g green on both legs, all six hashes byte-identical
  to `v30a.hashes.txt`.

- `account: 4bae848` — **Ceremony: C5b takes a baseline; commits made by the ceremony are exempt
  from accounting.** C5b required every commit between `prereg-v30` and HEAD to be accounted, which
  could not terminate once the ceremony itself commits. It now records HEAD at ceremony start as a
  **baseline**: commits up to it are inherited and must be accounted; commits after it are the
  ceremony's own. Its failure message was also rewritten — it said *"Do NOT widen this check"*,
  which would have warned the next reader off a correct fix, and now states the baseline rule and
  says the fix is the accounting, not the check. Belongs because the tag is cut over a tree whose
  own first gate must be able to terminate.

---

## The baseline rule, and why a commit is never asked to account for itself

**C5b takes a BASELINE**: HEAD at ceremony start, recorded once per run in `v30a.baseline.txt`.
Every commit from `prereg-v30` up to and including the baseline is **inherited** and must carry an
`account:` line here. **Commits after the baseline are the ceremony's own, and the ceremony is their
account.**

Without that rule the check could not terminate. The accounting lives *inside* the commit, so a
commit can never account for its own hash — the same reason the OpenTimestamps receipt needs a
follow-up commit — and accounting each new commit merely creates another unaccounted one. **An
inherited unaccounted commit still halts**, which is the point, and C5b's known-positive removes a
real accounting line to prove it.

---

## Why the accounting is by short hash

The gate greps for the 7-character short hash. That is deliberate: it is stable under abbreviation
growth, it is what `git log --oneline` prints, and it forces the accounting to name a **specific
object** rather than a description that could drift onto a different commit.

## What to do when a new commit appears

Add an `account:` line. Do not edit the gate, do not widen it, and do not remove the check — the
check firing on a new commit is it working. If the commit does **not** belong in the tagged tree,
that is the finding, and it is why the gate is a HALT rather than a warning.
