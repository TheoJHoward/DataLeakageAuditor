#!/usr/bin/env python3
"""A4(a), A4(b), A4(d) — the declaration edits, applied by anchor.

Anchored on heading text, never on line numbers: line numbers move as soon as
the first edit lands, and re-pinning by arithmetic is the defect H-L24 records.

Written with the Write tool per D2.1.
"""
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
DECL = REPO / "AVAILABILITY_DECLARATION.md"

s = DECL.read_text(encoding="utf-8")
orig_len = len(s)

# ---------------------------------------------------------------- A4(a) -----
D2_START = "### D.2 — The v30a tag message carries SIX hashes"
D3_START = "### D.3 — Interpretation rule for decision-log entries"
i, j = s.index(D2_START), s.index(D3_START)

NEW_D2 = """### D.2 — The v30a tag message's hash enumeration

**The enumeration is derived from `PREREG.md` §11 item 8, and from nothing else.** Item 8 is the
v30a clause that defines the set; it is cited here by anchor rather than by line, because this file
is living and a line reference into it drifts.

**Item 8's three limbs, and what each contributes:**

1. **"every registered document and every registration tool — the registration and its checking
   tools as item 1 names them."** §11 item 1 names nine paths. Eight are files; the ninth,
   `tests/registration/`, is a directory, and a directory name does not pin content — item 8's
   closing sentence speaks of a registered **file**, so the directory is enumerated as the files it
   contains.
2. **"every document an amendment registers under §0.2.1 (the availability declaration included)."**
   That is this file.
3. **"every file SC-8(f) requires hashed."** SC-8(f) reaches every file the freeze ranges over.
   Two of those are separate committed files rather than elements inside this one: the F3 fixture
   manifest, which SC-4(k2) reads and §D.1 pins, and the declared ground-truth map, which is the
   scoring key.

**DECLARED: the `prereg-v30a` tag message carries TWENTY SHA-256 lines.** The count is read from the
enumeration and is not an independent assertion about it; the enumeration is produced by the
ceremony's C2 step, whose output `v30a.hashes.txt` is the single authority for any `prereg-v30a`
hash value.

| limb | paths |
|---|---|
| 1 — item 1, named individually | `PREREG.md`, `DESIGN.md`, `HISTORY.md`, `DEVIATIONS.md`, `PARKING_LOT.md`, `VALIDATED_CONFIG.toml`, `tools/check_registration.py`, `protocol/runtime_reference.py` |
| 1 — `tests/registration/`, expanded | `EXPECTED_OUTPUTS.md`, `conftest.py`, `generate_expected_outputs.py`, `test_checker.py`, `test_expected_outputs.py`, `test_invariants.py`, `test_traces.py`, `traces.py` |
| 2 — §0.2.1 | `AVAILABILITY_DECLARATION.md` |
| 3 — SC-8(f) | `evidence/fixture_spike/f3/fixture_manifest_DRAFT.json`, `evidence/fixture_spike/n1/declared_map.csv` |
| §D.1's pinned producing code | `evidence/fixture_spike/f3/phase7_l2_sim.py` |

**WHY THE EARLIER SIX IS SUPERSEDED, recorded rather than quietly replaced.** This section previously
declared SIX and derived that number from two sources: working resolution R7, which records the
executed `prereg-v30` five, and `PREREG.md` §0.2.1 line 97's "both file hashes in the tag message."
**Item 8 names both of those in terms and supersedes them as the set:** *"where an earlier clause
names the hashed files or their number — item 3's three names, §0.2.1 line 97's 'both' — it records
the set at the time of its writing, stands as that record, and is superseded as the set by this
item."* The earlier derivation rested on the very clause item 8 retires, and it did not cite item 8.
Both earlier statements stand as the record of what was true when they were written; neither states
the set now.

**PRIOR_ART_VERIFICATION.md is not named by item 1, is not registered under §0.2.1, and is not
within the range SC-8(f) ranges over; it is outside the enumeration by rule.**

That file was the declined seventh candidate, closed as SIX at `COMMIT_PLAN.md` §6. **Growing the
set reopens that closure, so it is decided again here rather than inherited:** the earlier decision
turned on a judgement about what belonged, and this one turns on the rule item 8 states. The
outcome is the same and the ground is different, which is why it is restated rather than cited.

**Why the declaration is in the set at all.** This file carries the scoring key and the declared
elements the gate consumes. A tag that hashes the specification but not the declaration the
specification is evaluated under is an integrity chain with a hole exactly where the amendment
lives, and **an amendment weaker than the thing it amends is not one** (§0.2.1 line 97).

**Lock-time obligations arising elsewhere in this file — BOTH DISCHARGED, recorded so the change is
auditable rather than silent:**

- **(i) "Add the contamination availability class as a named field to the governing manifest"
  (§A.3) — DISCHARGED by amendment, not by doing it.** The recording locus is amended to this
  declaration, which the tag hashes; the manifest is an evidence artifact and is not edited
  (§A.3, working resolution R13). There is no residual manifest edit due before the tag.
- **(ii) "Produce or formally defer the CI sliced variant" (§A.4) — DISCHARGED by amendment.**
  The element is moved off the Phase 0 acceptance fixture and re-registered as a Phase 1 CI
  obligation with its scoring rule declared ex ante. It is not due at lock; it is due at the
  first CI run that exercises the padded slicer, and it is frozen by §D.1 item 5.

**No lock-time obligation remains outstanding in this file.** Obligations carried FORWARD rather
than discharged are named at §D.5, so a later reader does not mistake "nothing due at lock" for
"nothing due".

"""

s = s[:i] + NEW_D2 + s[j:]

# ------------------------------------------------------- A4(b) and A4(d) ----
E_START = "## §E. Gate protocol input surface"
k = s.index(E_START)

NEW_D5_D6 = """### D.5 — Named open obligations

**Recorded under SC-9(c); neither is waived.** SC-9(c) holds that a locked obligation is discharged
only by being met or by being amended, and may not be discharged by a working resolution or by being
carried forward silently. These two are carried forward, and this section is what makes that
carrying explicit rather than silent.

**SC-2(e) is not engaged.** SC-2(e) governs moving an element between phases. Neither element moved:
both remain Phase 0 elements gated by §10.1. What a working resolution fixed was the **due event**,
not the phase.

**(i) §9.2 cross-tool comparison — Phase 0 element, gated by §10.1.**

- **DUE:** before any Phase 1 result is published. Not a condition on Phase 1 work commencing —
  §10.0 step 0 is the only such condition.
- **DISCHARGE:** each named comparator has been run against the acceptance fixture with its own
  positive control (W2b) and its findings recorded per tool. A comparator that cannot run is
  recorded could-not-run with the reason and counts as covered-with-exclusion, never as a pass.
  **Zero comparators run is not a pass** (SC-11a).

**(ii) Licence check — Phase 0 element, gated by §10.1.**

- **DUE:** before any third-party code enters the shipped distribution, and in any case before
  Phase 1 ship.
- **DISCHARGE:** every dependency in the shipped distribution has its licence recorded, and no
  copyleft licence appears in the vendored set. `deepchecks` is AGPL-3.0 and is named.
  Interoperation by optional import or separate process is not vendoring; the distinction is
  recorded with the determination.

**The shape of both entries is §D.2(ii)'s:** a named due event plus a discharge rule, with the rule
**cited rather than restated** where a registered clause already states it.

---

### D.6 — Disclosures at the tag

**What this section is.** Five disclosures accrued during the amendment. Each was written as it
should appear and none had been deployed into a registered file, so each existed only in a drafting
record. **A disclosure that lives only in a drafting record discloses nothing to a reader of the
tag**, and this file freezes at the tag. They are landed here for that reason.

**One of them was already load-bearing while absent.** §A's conformance walk states that `PREREG.md`
line 478 "is handled instead by **specific disclosure at D-STALE**, by line and by quotation" — a
registered pointer into a disclosure that did not exist. The pointer now resolves.

---

**D-KEY — the attestation boundary.**

> **What the ceremony verifies about the signing key, and what it does not.** Step C1b verifies
> three things and halts if any disagrees: the signature is good (`[GNUPG:] GOODSIG`); the primary
> key fingerprint gpg reports for the signature (`[GNUPG:] VALIDSIG`, last field) equals the
> fingerprint the signed tag message asserts; and both equal the fingerprint declared at §D.4, which
> is inside the tag's hash enumeration and therefore covered by the OpenTimestamps receipt over the
> commit.
>
> **All three legs are internal to this repository.** Together they establish that the tag was
> signed by the key this registration names, and that the naming was fixed before the timestamp.
> **They do not establish who holds that key.** Key-to-person binding cannot be established by any
> repository-local check: an actor able to rewrite the tag could rewrite all three legs together.
>
> **That binding rests on publication outside this repository.** The only external location this
> repository names is the GitHub remote `https://github.com/TheoJHoward/DataLeakageAuditor.git`.
> **No keyserver is referenced anywhere in the repository.** If the public key is published, the only
> location consistent with the repository's own contents is the author's GitHub account settings —
> **which is mutable, carries no date a reader can see, and can be removed or replaced without
> leaving a record.** For a pre-registration, whose whole value is that a claim was fixed at a
> knowable time, that is a weak external anchor, and it is disclosed as such rather than left to be
> discovered.
>
> **What shipping the key material fixes, and what it does not.** `prereg-signing-key.asc` at the
> repository root is the ASCII-armored public key, so the tagged tree carries the key material
> itself and a reader in ten years can verify the signature without a keyserver that may no longer
> exist. **This closes the availability problem, not the binding problem** — a key shipped inside
> the repository it signs proves internal consistency only, exactly as above. The uid on the shipped
> key reads `Theo Johann Howard <theojhoward1@gmail.com>`; it is recorded here because the key
> material ships and the uid ships with it.
>
> **A remedy available and NOT taken, stated so the choice is visible:** publishing the key to
> `keys.openpgp.org` and citing that URL in the README would give a dated, third-party, append-only
> anchor. It is an author action requiring control of the key and the email address; no ceremony
> step can perform it.

---

**D-ADVISORY — the five deferred advisory steps.**

> **Five ceremony steps emit output for a human to compare and assert nothing.** They are `C5`
> (2 items), `C2b` (6), `C3c` (3), `C3d` (2) and `V2` (2). Each is honest advisory — it claims no
> verdict — but a reader should know that at these five points the ceremony's correctness rested on
> a person reading output, not on an exit status. The ten steps whose printed verdict contradicted
> their exit status were converted and each carries a fired negative test; **these five were
> deferred, and this line is the record that they were deferred rather than overlooked.**

---

**D-STALE — the stale-description class, stated as a FLOOR.**

> **A class of stale descriptions is disclosed rather than fixed, and its extent is not known.**
>
> After the R9, R11, Y1, R1, R2, R16, SC-13 and Z1 amendments, a sweep was run for passages that
> still describe the amended objects as they were before. **The sweep found approximately
> seventy-six distinct sites and returned zero of ten amendments clean.** Of those, the
> ship-critical subset was fixed. **What is disclosed here is a different quantity from what the
> sweep found, and the two must not be read as one:** the sweep's finding is the seventy-six above;
> what remains uncorrected is **approximately thirteen sites in four classes** — the declared map's
> class set (Y1), what counts as a violation at equal timestamps (R1), a per-side criterion
> enumeration that omits criterion 1, and SC-13's description.
>
> **The number seventy-six is a FLOOR, not an extent.** The sweep's population was never measured.
> It was an agent-driven read over ten amendments, not a mechanically bounded scan, and no proof
> exists that it covered every passage describing every amended object. **The true size of this
> class is unknown and may be larger than the sweep found.** Nothing here should be read as bounding
> the class by seventy-six, or by thirteen.
>
> **The instrument's own limits, quoted verbatim rather than paraphrased:** its actual domain was
> *"ten amendments, agent-driven read"*; its gap was *"not mechanically bounded; no population
> proof"*; and its boundary test was *"none — this is the weakest instrument in the set, and its
> output is cited as evidence rather than relied on as coverage."*
>
> **WHICH INSTRUMENT PRODUCED THESE FIGURES — stated so the two are never conflated.** Both figures
> above are the **agent-driven description sweep's**. **Neither comes from any script.** In
> particular neither comes from `_K1_enumerate.py`, the K1 step-1 population enumerator, which
> shares the K1 label and nothing else: it enumerates blockquote runs in `SCHEMA_SET_FINAL.md` for
> the block manifest and has never counted a stale description. `_K1_enumerate.py` carries a defect
> — a literal BACKSPACE in its `MARK` regex, so the marker split it guards never runs — and **that
> defect does not touch these figures or anything else cited anywhere**: the script is superseded by
> `_K1_enumerate2.py`, and its own output is cited in no document. A later reader finding the K1
> defect should not go looking for its effect here, because there is none.
>
> **ONE STALE SENTENCE, NAMED BY LINE, NOT LEFT TO THE CLASS.** The class above is disclosed as a
> floor. **This sentence is disclosed individually, because it is known to be false and it was left
> in the registered text deliberately.**
>
> **Where:** `PREREG.md` **line 478 as registered at `prereg-v30`; line 948 in the amended file.**
>
> **Verbatim:** *"**This is a rebalance, not a tightening.** The two gates are incomparable: a
> fixture detected only at `dtype_promoted` with nothing on clean or corrected fails the old and
> passes the new; a fixture detected at PROVEN throughout but with one REVIEW finding on a clean
> source passes the old and fails the new. The trade is deliberate — drop the irrelevant requirement
> that acceptance detections be proofs, add the relevant requirement that **nothing shipped appears
> on clean or corrected material**."*
>
> **Why it is now false.** Its closing clause states criterion 3's purpose as a pure silence test on
> the corrected side. **SC-3 retired that premise.** Under the amendment the corrected side is
> scored against the declared ground-truth map: findings the map predicts are **required**, and a
> tool silent where the map declares a violation **fails**. The sentence describes a gate the
> registration no longer has.
>
> **The operative text is correct and is not affected.** The criterion itself — `PREREG.md` line 461
> as registered — **was replaced by SC-3**, and the replacement is what the gate reads. The applied
> text registers that *"the criteria of §6.2 as amended are the whole gate"*; line 948 is not a
> criterion, sits in §6.2's framing prose, is inside no clause block, and **no tool in the
> repository reads it** — verified by search, not assumed. **It is rationale, not operative.**
>
> **Why it was not amended.** Re-amending rationale prose would open a second approval cycle over a
> sentence that binds nothing, and line 97's rule — *"An amendment weaker than the thing it amends
> is not one"* — is not engaged, because **nothing is weakened by leaving it**: the operative
> criterion is strictly harder than the one this sentence describes. **The trade is accuracy of
> rationale against the cost of the tag, and it was taken knowingly.**
>
> **It was known false at tag time and left in place. That is the disclosure.** A reader who takes
> this sentence as a statement of what criterion 3 requires will be wrong, and should read SC-3.
>
> **Why the class was not measured before the tag.** Measuring the population means enumerating
> every passage in every corpus that describes every amended object, and judging each against what
> the object now is. That is larger than the amendment it would qualify, and it was ruled out of
> scope rather than attempted and abandoned. **The consequence is stated rather than mitigated: a
> reader relying on any description in these documents of an object amended by R9, R11, Y1, R1, R2,
> R16, SC-13 or Z1 should verify it against the registered text, because this registration does not
> warrant that such descriptions were all found.**

---

**D-INSTRUMENT — gaps in the verification apparatus itself.**

> **The checks that verify this ceremony have measured domains, and the gaps are disclosed.** Five
> remain open at the tag:
>
> 1. **`sha256sum -c` is one-directional.** It verifies listed→disk and cannot see a file on disk
>    that no manifest line covers. Two instruments outside it now assert the reverse direction (a
>    registration-checker scan of the tree, and a ceremony step against the index), but neither can
>    see a file added between the last check and `git commit`; the clean-tree assertion after commit
>    is the backstop.
> 2. **The line-citation check covers 6 of 395 citations.** The other 389 rest on classification,
>    and **71 of them could not be attributed to a target file at all** — a defect in the
>    classifier, recorded as such and not as coverage.
> 3. **The stale-description sweep has no measured population** (see D-STALE).
> 4. **The hash-count check cannot read informal quantifiers, Roman numerals, or the `six (6)`
>    form, and reads a range as its first value.**
> 5. **The staging check cannot see staging performed by any means other than a literal `git add`
>    line** — a wildcard, a variable or a loop is invisible to it.
>
> **These are published because a verification apparatus that claims more than it delivers is the
> defect this project exists to detect in other people's pipelines**, and a pre-registration that
> exempted its own instruments from that standard would be making the claim it warns against.

---

**D-ARCHIVE — the external-input dependency.**

> **The fixture's inputs are not in this repository, and this is disclosed rather than resolved.**
>
> **The classifications were produced by `phase7_l2_sim.py`, committed in this repository and hashed
> in the tag message. The inputs it consumed are external to the repository, so a repository-only
> reader can audit the derivation but cannot re-execute it.**
>
> **THE FIGURES FOR THIS DISCLOSURE LIVE IN ONE ARTIFACT, AND THIS DISCLOSURE DOES NOT RESTATE
> THEM.** That artifact is `evidence/LARGE_ARTIFACTS_RECORD.md`, attested by its line in
> `evidence/MANIFEST.sha256`. Every per-file size, every count, and the archive's own total are
> there, measured and sourced. **A figure quoted in two places is a figure that will eventually
> disagree with itself.**
>
> **What is missing.** The producers read market data from a local archive outside the repository.
> The producing code is committed; the inputs are not. A reader holding this repository and nothing
> else **cannot regenerate the fixture from source** — they can verify every committed hash, re-run
> every check, and read every result, but the bytes the fixture was built from are not theirs to
> re-read. The position is: **(a) producing code in the repository — YES; (b) inputs in the
> repository — NO; (c) pipeline deterministic — YES, demonstrated twice over.**
>
> **MAGNITUDE.** The archive runs to **several hundred gigabytes**. What the producers actually read
> — traced through their own source rather than estimated — is **a few hundred megabytes across a
> bounded, enumerated set of files: a small fraction of one percent of the archive.** The inputs are
> **ZC 2025-01 and 2025-08 only**. The gap between what the archive holds and what the fixture needs
> is **roughly four orders of magnitude**, and that gap is the disclosable fact: the dependency
> looked like an archive-sized problem and is not one.
>
> **A NEGATIVE RESULT, REPORTED AS A POSITIVE FINDING.** The question *"what else does the fixture
> read?"* was put to the producers' own source, and the answer is **NONE**. The archive's other
> large trees — `processed/`, `pc2_transfer/`, `raw_data/`, each of them hundreds of gigabytes — are
> read by none of the producers. **The dependency is bounded, and it is bounded by reading the code
> rather than by asserting a scope.** A NONE that was looked for and not found is evidence; a NONE
> that was assumed is not — which is why the method is stated beside the result.
>
> **A second measured fact, disclosed because it changes what "durable" means.** The archive is
> **not synced to any cloud location, and neither is anything else**: the sync engine's database and
> the account file were both last written nearly three years before the tag. **Every copy of every
> artifact this registration depends on is on one machine, on one disk.**
>
> **Why the disclosure is not deleted now that the producing code ships.** Deleting it would claim a
> self-sufficiency the repository does not have. Bringing the file in closes the code half only.

---

"""

s = s[:k] + NEW_D5_D6 + s[k:]

DECL.write_text(s, encoding="utf-8", newline="\n")
print("A4(a)/(b)/(d): declaration rewritten, %d -> %d bytes (+%d)"
      % (orig_len, len(s), len(s) - orig_len))
for probe in ("### D.2 — The v30a tag message's hash enumeration",
              "### D.5 — Named open obligations",
              "### D.6 — Disclosures at the tag",
              "PRIOR_ART_VERIFICATION.md is not named by item 1",
              "**D-KEY", "**D-ADVISORY", "**D-STALE", "**D-INSTRUMENT", "**D-ARCHIVE"):
    if probe not in s:
        sys.exit("HALT: %r did not land" % probe)
print("all anchors present")
