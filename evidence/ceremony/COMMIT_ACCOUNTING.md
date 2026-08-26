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

---

## Why the accounting is by short hash

The gate greps for the 7-character short hash. That is deliberate: it is stable under abbreviation
growth, it is what `git log --oneline` prints, and it forces the accounting to name a **specific
object** rather than a description that could drift onto a different commit.

## What to do when a new commit appears

Add an `account:` line. Do not edit the gate, do not widen it, and do not remove the check — the
check firing on a new commit is it working. If the commit does **not** belong in the tagged tree,
that is the finding, and it is why the gate is a HALT rather than a warning.
