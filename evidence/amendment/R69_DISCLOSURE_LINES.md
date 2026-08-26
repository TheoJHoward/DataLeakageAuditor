# §12 DISCLOSURE LINES ACCRUED — to land with R66 §4

Each is written as it should appear. R66 §4.2 holds: **nothing here characterises a remainder as
harmless.**

---

## D-KEY (R69/B2.5) — the attestation boundary

> **What the ceremony verifies about the signing key, and what it does not.** Step C1b verifies
> three things and halts if any disagrees: the signature is good (`[GNUPG:] GOODSIG`); the primary
> key fingerprint gpg reports for the signature (`[GNUPG:] VALIDSIG`, last field) equals the
> fingerprint the signed tag message asserts; and both equal the fingerprint declared at
> `AVAILABILITY_DECLARATION.md` §D.4, which is inside the six-file hash set and therefore covered by
> the OpenTimestamps receipt over the commit.
>
> **All three legs are internal to this repository.** Together they establish that the tag was
> signed by the key this registration names, and that the naming was fixed before the timestamp.
> **They do not establish who holds that key.** Key-to-person binding cannot be established by any
> repository-local check: an actor able to rewrite the tag could rewrite all three legs together.
>
> **That binding rests on publication outside this repository.** As at 24 August 2026 the only
> external location this repository names is the GitHub remote
> `https://github.com/TheoJHoward/DataLeakageAuditor.git`. **No keyserver is referenced anywhere in
> the repository, and no key file was tracked before R69.** If the public key is published, the
> only location consistent with the repository's own contents is the author's GitHub account
> settings — **which is mutable, carries no date a reader can see, and can be removed or replaced
> without leaving a record.** For a pre-registration, whose whole value is that a claim was fixed at
> a knowable time, that is a weak external anchor, and it is disclosed as such rather than left to
> be discovered.
>
> **What R69 added, and what it does not fix.** `prereg-signing-key.asc` at the repository root is
> the ASCII-armored public key, so the tagged tree now carries the key material itself and a reader
> in ten years can verify the signature without a keyserver that may no longer exist. It is
> deliberately **not** added to the six-file hash list (§14.1(b): that list is a citation device and
> the commit tree already fixes every tracked file; SIX is not reopened). **This closes the
> availability problem, not the binding problem** — a key shipped inside the repository it signs
> proves internal consistency only, exactly as above.
>
> **The uid on the shipped key reads `Theo Johann Howard <theojhoward1@gmail.com>`.** It is recorded
> here because the key material now ships and the uid ships with it.

**Remedy available and NOT taken in this round, stated so the choice is visible:** publishing the
key to `keys.openpgp.org` and citing that URL in the README would give a dated, third-party,
append-only anchor. It is an author action requiring control of the key and the email address; it
is not something this ceremony can perform.

---

## D-ADVISORY (R68/§27.3) — the five deferred advisory steps

> **Five ceremony steps emit output for a human to compare and assert nothing.** They are
> `C5` (2 items), `C2b` (6), `C3c` (3), `C3d` (2) and `V2` (2). Each is honest advisory — it claims
> no verdict — but a reader should know that at these five points the ceremony's correctness rested
> on a person reading output, not on an exit status. The ten steps whose printed verdict contradicted
> their exit status were converted at R68 and each carries a fired negative test; these five were
> deferred, and this line is the record that they were deferred rather than overlooked.

---

## D-STALE (R71/§38) — the stale-description class, stated as a FLOOR

> **A class of stale descriptions is disclosed rather than fixed, and its extent is not known.**
>
> After the R9, R11, Y1, R1, R2, R16, SC-13 and Z1 amendments, a sweep was run for passages that
> still describe the amended objects as they were before. **The sweep found approximately seventy-six
> distinct sites and returned zero of ten amendments clean.** Of those, the ship-critical subset was
> fixed. **What is disclosed here is a different quantity from what the sweep found, and the two must
> not be read as one:** the sweep's finding is the seventy-six above; what remains uncorrected is
> **approximately thirteen sites in four classes** — the declared map's class set (Y1), what
> counts as a violation at equal timestamps (R1), a per-side criterion enumeration that omits
> criterion 1, and SC-13's description — are **disclosed here and not corrected**.
>
> **The number seventy-six is a FLOOR, not an extent.** The sweep's population was never measured.
> It was an agent-driven read over ten amendments, not a mechanically bounded scan, and no proof
> exists that it covered every passage describing every amended object. **The true size of this
> class is unknown and may be larger than the sweep found.** Nothing in this disclosure should be
> read as bounding the class by seventy-six, or by thirteen.
>
> **The instrument's own limits, quoted verbatim from the R70 instrument-domain audit rather than
> paraphrased:** its actual domain was *"ten amendments, agent-driven read"*; its gap was *"not
> mechanically bounded; no population proof"*; and its boundary test was *"none — this is the
> weakest instrument in the set, and its output is cited as evidence rather than relied on as
> coverage."*
>
> **WHICH INSTRUMENT PRODUCED THESE FIGURES — stated so the two are never conflated (R83/§94.4).**
> Both figures above are the **agent-driven description sweep's**. **Neither comes from any
> script.** In particular neither comes from `_K1_enumerate.py`, the K1 *step-1 population
> enumerator*, which shares the K1 label and nothing else: it enumerates blockquote runs in
> `SCHEMA_SET_FINAL.md` for the block manifest and has never counted a stale description.
> `_K1_enumerate.py` carries a defect — a literal BACKSPACE in its `MARK` regex, so the marker
> split it guards never runs (R82/D1, R83/E1) — and **that defect does not touch these figures
> or anything else cited anywhere**: the script is superseded by `_K1_enumerate2.py`, and its
> own output `_K1_population.json` is cited in no document. A later reader finding the K1 defect
> should not go looking for its effect here, because there is none.
>
> **ONE STALE SENTENCE, NAMED BY LINE, NOT LEFT TO THE CLASS (R95/§147.3).** The class above is
> disclosed as a floor. **This sentence is disclosed individually, because it is known to be false
> and it was left in the registered text deliberately.**
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
> the corrected side. **SC-3 retired that premise.** Under the amendment the corrected side is scored
> against the declared ground-truth map: findings the map predicts are **required**, and a tool
> silent where the map declares a violation **fails**. The sentence describes a gate the registration
> no longer has.
>
> **The operative text is correct and is not affected.** The criterion itself — `PREREG.md`
> line 461 as registered — **was replaced by SC-3**, and the replacement is what the gate reads.
> Applied `PREREG.md` line 111 registers that *"**the criteria of §6.2 as amended are the whole
> gate**"*; line 948 is not a criterion, sits in §6.2's framing prose, is inside no clause block, and
> **no tool in the repository reads it** — verified by search at R95, not assumed. **It is rationale,
> not operative.**
>
> **Why it was not amended.** R66 §2.1 existed to fix it and was never executed. Re-amending
> rationale prose would open a second approval cycle over a sentence that binds nothing, and
> `PREREG.md` line 97's rule — *"An amendment weaker than the thing it amends is not one"* — is not
> engaged, because **nothing is weakened by leaving it**: the operative criterion is strictly harder
> than the one this sentence describes. **The trade is accuracy of rationale against the cost of the
> tag, and it was taken knowingly.**
>
> **It was known false at tag time and left in place. That is the disclosure.** A reader who takes
> this sentence as a statement of what criterion 3 requires will be wrong, and should read SC-3.
>
> **Why it was not measured before the tag.** Measuring the population means enumerating every
> passage in every corpus that describes every amended object, and judging each against what the
> object now is. That is larger than the amendment it would qualify, and it was ruled out of scope
> for this ceremony rather than attempted and abandoned. **The consequence is stated rather than
> mitigated: a reader relying on any description in these documents of an object amended by R9, R11,
> Y1, R1, R2, R16, SC-13 or Z1 should verify it against the registered text, because this
> registration does not warrant that such descriptions were all found.**
>
> The sweep's raw output is retained in the ceremony record and is cited, not summarised, so that a
> later reader can measure what this one did not.

---

## D-ARCHIVE (R77/§69.2, written R83/§78, restructured R84/§99) — the external-input dependency

> **The fixture's inputs are not in this repository, and this is disclosed rather than resolved.**
>
> **THE FIGURES FOR THIS DISCLOSURE LIVE IN ONE ARTIFACT, AND THIS DISCLOSURE DOES NOT RESTATE THEM.**
> That artifact is **`evidence/LARGE_ARTIFACTS_RECORD.md`**, sha256
> **`7a9204692286119214ea9d49177e7ab3d436036dd8fcae418999242defce02d4`**,
> attested by its line in `evidence/MANIFEST.sha256`. Every per-file size, every count, and the
> archive's own total are there, measured and sourced. **A figure quoted in two places is a figure
> that will eventually disagree with itself**, and this disclosure had that defect from the day it
> was written until this restructure.
>
> **What is missing.** The three producers read market data from a local archive outside the
> repository. The producing code IS committed (R76); the inputs are not. A reader holding this
> repository and nothing else **cannot regenerate the fixture from source** — they can verify every
> committed hash, re-run every check, and read every result, but the bytes the fixture was built from
> are not theirs to re-read. §62.3 states the position: **(a) producing code in the repository —
> YES; (b) inputs in the repository — NO; (c) pipeline deterministic — YES, demonstrated twice over.**
>
> **MAGNITUDE.** The archive runs to **several hundred gigabytes**. What the three producers actually
> read — traced through their own source rather than estimated — is **a few hundred megabytes across
> a bounded, enumerated set of files: a small fraction of one percent of the archive.** The inputs are
> **ZC 2025-01 and 2025-08 only**. The gap between what the archive holds and what the fixture needs
> is **roughly four orders of magnitude**, and that gap is the disclosable fact: the dependency
> looked like an archive-sized problem and is not one.
>
> **A NEGATIVE RESULT, REPORTED AS A POSITIVE FINDING.** The question *"what else does the fixture
> read?"* was put to the producers' own source, and the answer is **NONE**. The archive's other large
> trees — `processed/`, `pc2_transfer/`, `raw_data/`, **each of them hundreds of gigabytes** — are
> read by none of the three producers. `phase5_ml_fixture.py` sets `LOCAL_DATA = C:\MBO_data`, which
> does not exist, so `get_data_dir` falls back to `processed/`. **The dependency is bounded, and it
> is bounded by reading the code rather than by asserting a scope.** A NONE that was looked for and
> not found is evidence; a NONE that was assumed is not — which is why the method is stated here
> beside the result, and why the result is not left to be inferred from the absence of a finding.
>
> **A second measured fact, disclosed because it changes what "durable" means.** The archive is **not
> synced to OneDrive, and neither is anything else**: the sync engine's database and the account file
> were both last written **5 September 2023**, nearly three years ago. **Every copy of every artifact
> this registration depends on is on one machine, on one disk.**
>
> **What is NOT disclosed here is a recommendation.** §70.2 held that no backup strategy be proposed
> until the footprint was measured. It is measured; the factual position is stated with nothing
> attached. **What to do about it is the author's call, and this disclosure takes no position.**
>
> **THE FROZEN F3 MANIFEST'S 35 CLASSIFICATIONS REST ENTIRELY ON `phase7_l2_sim.py`, WHICH IS
> OUTSIDE THE SIGNED TREE.** Every column cites it as its construction source; the label
> definition and the universal `shift(1)` that fixes the pre-lag frame are in it. It is pinned
> in §D.1 by sha256 alongside the manifest, and it lives in the archive's
> `results\pc2_all_phases\_scripts` reference. **A reader with the repository alone cannot
> re-derive the 35 classifications.** That is the concrete form of this disclosure: not that
> some inputs are external, but that a *gate input's meaning* is.
>
> **This does not gate the tag** (R77/§69.3). It is disclosed because a reader entitled to know
> whether they can reproduce the fixture should learn it here rather than by attempting it.

---

## D-INSTRUMENT (R71/§38, B6.4) — gaps in the verification apparatus itself

> **The checks that verify this ceremony have measured domains, and the gaps are disclosed.** Five
> remain open at the tag:
>
> 1. **`sha256sum -c` is one-directional.** It verifies listed→disk and cannot see a file on disk
>    that no manifest line covers. Two instruments outside it now assert the reverse direction (a
>    registration-checker scan of the tree, and a ceremony step against the index), but neither can
>    see a file added between the last check and `git commit`; the clean-tree assertion after commit
>    is the backstop.
> 2. **The line-citation check covers 6 of 395 citations.** The other 389 rest on classification,
>    and **71 of them could not be attributed to a target file at all** — a defect in the classifier,
>    recorded as such and not as coverage.
> 3. **The stale-description sweep has no measured population** (see D-STALE).
> 4. **The hash-count check cannot read informal quantifiers, Roman numerals, or the `six (6)` form,
>    and reads a range as its first value.**
> 5. **The staging check cannot see staging performed by any means other than a literal `git add`
>    line** — a wildcard, a variable or a loop is invisible to it.
>
> **These are published because a verification apparatus that claims more than it delivers is the
> defect this project exists to detect in other people's pipelines**, and a pre-registration that
> exempted its own instruments from that standard would be making the claim it warns against.
