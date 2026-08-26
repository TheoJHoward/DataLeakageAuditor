# DEFERRED ITEMS — recorded with their substance, before execution

**Why this file exists (R87/§111).** §56.5 holds that a ruling is not settled until it is in the
repository. Deltas are chat text, and a section that is DEFERRED rather than executed lives only
there. **A ledger line naming a section number is a pointer into a transient location.** §39, §72.2
and §64/D11 survived eleven rounds as the single line *"Post-tag: §39 (+§72.2) into `DESIGN.md`;
§64's D11 sweep"*, and a corpus-wide search for any of those three labels returned exactly one hit —
that line itself. Nobody reading the record could say what they were.

**The standing rule this file implements (§111.2):** a delta section that defers work **lands as a
repository item WITH ITS SUBSTANCE at the moment it is deferred**, not when it is executed.

**Recording is not doing.** Every item below is post-tag. Nothing here is executed by being written
down, and nothing here gates the `prereg-v30a` tag.

---

## §39 — the auditor publishes its detection domain (DESIGN.md, Phase 1 requirement)

To be added to `DESIGN.md` **in `DESIGN.md`'s own voice**, as a Phase 1 requirement:

> The auditor publishes its **detection domain** and what it **cannot see**. A silent pass is
> reported **together with the domain that produced it** — a pass is a statement about what was
> looked for, and a reader given the verdict without the domain cannot tell a clean result from an
> unexamined one. Its test suite draws cases from **OUTSIDE** the detection domain, not only from
> inside it.

**Empirical basis:** H-L21 and its instances — an instrument's PASS is a statement about its DOMAIN,
not about the world, and every instance in this project's own apparatus was found by testing from
outside the vocabulary the instrument was authored in.

## §139 — the usability requirement (Phase 1, pairs with §39)

To be added to `DESIGN.md` **in `DESIGN.md`'s own voice**, as a Phase 1 requirement:

> The **availability declaration is the tool's adoption surface**. A tool requiring a hand-authored
> per-column specification will not be used. The auditor **infers availability where inference is
> sound** — schema, timestamp columns, declared event anchors — and **asks the user only where the
> answer is genuinely ambiguous**. **Every inferred value is reported as inferred, with what it was
> inferred from**, so a user can see it and override it.

**Author's framing, 25 August 2026:** *"the goal is easy to use but useful."*

**Why it pairs with §39 (§139.2).** §39 says **publish what the tool cannot see**; §139 says **do not
make the user do work the tool can do**. Same principle from two ends: the burden the tool declines to
carry lands on the user, and a burden the user will not carry means the tool goes unused and detects
nothing. Neither half is a caveat — both are checks the tool ships.

## §72.2 — a documented lesson is not a control (folded into §39, same voice)

> A documented lesson is **not a control**. The auditor **ships the check, not the caveat**. Where it
> knows a failure mode, it **asserts against it**; where it cannot assert, it **publishes the gap**.

## §180.4 — bring `phase7_l2_sim.py` into the repository (post-tag, RECOMMENDED)

**The file:** `phase7_l2_sim.py`, sha256 `c659d3ac167a13afb52651d4521ecc9fd5c8fabd59fd2d712eb4afa5b4669665`, **949 lines, 41,745 bytes (~41 KB)**, currently
resident only in the archive at `results\pc2_all_phases\_scripts\scripts\`.

**Why it is post-tag.** Bringing it in **changes what ships**, and its absence makes
**nothing in the signed object false** — §D.1 pins its bytes, and D-ARCHIVE discloses that a
repository-only reader cannot re-derive the classifications. Disclosed truthfully is not the
same as unavailable, and §71.3's line falls between them.

**RECOMMENDED, and the recommendation is the point.** At ~41 KB it is smaller than several
files already in the evidence tree. Committing it would make the F3 manifest's 35
classifications **independently verifiable from the repository alone**, which converts a
disclosed external dependency into no dependency at all. The verification performed at R101
would then be reproducible by any reader rather than by anyone holding the archive.

## §173 — THE FOURTH DIRECTION: untracked, unattested, unlisted (post-tag)

**The gap.** Four directions exist between the working tree, the manifest and the commit. Three are
checked and one is not:

| direction | check |
|---|---|
| disk → listed (every evidence file has a manifest line) | **D9** |
| listed → in the commit (every attested path is tracked or staged) | **D16** |
| work root → repo-or-ephemeral | **D10** |
| **repo tree → accounted for** | **NOTHING** |

**D10 does not cover it.** Its domain is the *work root* compared against the repo tree; a file that
lives in the repo tree is outside the question it asks. So a file can sit in the repository working
directory, be untracked, be attested by nothing, appear on no list, and **no instrument in the
apparatus will name it.**

**Why it is POST-TAG and not ship-critical (§71.3).** An unaccounted untracked file makes **nothing
in the signed object false**. The signed tree contains what it contains; the manifest attests what it
attests; D16 guarantees no attestation points outside the commit. An untracked extra on disk is
invisible to the tag rather than contradicted by it. It is a completeness gap in the apparatus, not a
falsehood in the registration — which is exactly the §71.3 line.

**THE SPEC, for whoever builds it.**

> Enumerate every untracked file under the repository root. Each must be **one** of:
> **(a)** in `COMMIT_PLAN.md` §4's staging set, **(b)** manifest-attested, or **(c)** on D10's
> ephemeral list with a reason. Anything in none of the three is reported. Population and exclusions
> stated per §30.1.

**A known positive is available today, before the check exists:** `LICENSE` is untracked, in no
staging set, attested by nothing, and on no list. It fires. `tools/control_char_scan.py` **was** a
second instance until R100/§172 declared it ephemeral — so the check would have caught two, and one
has since been closed by the route the check would demand.

**How it was found.** Not by an instrument. It surfaced at R98 when the three untracked files were
listed by hand for §165, and the question *"what checks this?"* had no answer. That is the shape of
every gap in this apparatus: a direction nobody thought to walk.

## §168.3 — LICENSE (post-tag, author's choice)

The repository has an untracked `LICENSE` at its root. **Nothing attests it** — no manifest line, no
staging-set entry — so it is not ship-critical and D16 does not ask after it.

**But a public research repository with no committed licence is a real gap** for anyone who wants to
use the tool, and it does not sit on its own: it interacts with the **Phase 6 wrap decision** and
with the **`deepchecks` AGPL-3.0 question recorded in H-34**, where a copyleft dependency's terms
bear on what the wrapper may be. **Choice of licence is the author's**, and it is recorded here so it
is not lost the way §39 and D11 nearly were.

## §64 / D11 — executed-procedure claims must resolve to an artifact

Every claim in the ceremony package and in `AVAILABILITY_DECLARATION.md` that a procedure **was
EXECUTED** — *"ran on D"*, *"was run"*, *"was verified"* — must resolve to an artifact in the
evidence tree.

- Sweep with its **population and exclusions stated per §30.1**.
- Any assertion that **cannot be made to resolve** goes into the **§12 disclosure**, naming what was
  claimed and what evidence exists for it.

**Why it is post-tag, recorded at R77:** deferred at §73.2 because **no such assertion appears in the
tag message**. That **NONE result is the reason for the deferral**, and it is a positive finding, not
an absence of checking — the tag message carries hashes, a key fingerprint and prose about
timestamping, and asserts no executed procedure whose evidence a reader would have to locate.

---

## STATUS

| item | status | recorded |
|---|---|---|
| §39 | post-tag, **not executed** | R87 |
| §72.2 | post-tag, **not executed**, folds into §39 | R87 |
| §64 / D11 | post-tag, **not executed** | R87 |
| §139 usability | **Phase 1**, **not executed**, pairs with §39 | R93 |
| §168.3 LICENSE | **post-tag**, **not executed**, author's choice | R99 |
| §173 fourth direction | **post-tag**, **not executed**; spec recorded, known positive available | R100 |
| §180.4 phase7_l2_sim.py | **post-tag**, **not executed**, **RECOMMENDED** — ~41 KB makes the manifest independently verifiable | R102 |
