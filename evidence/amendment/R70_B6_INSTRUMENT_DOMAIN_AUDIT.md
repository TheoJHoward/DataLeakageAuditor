# B6 — INSTRUMENT-DOMAIN AUDIT

**The GAP line is the deliverable (B6.2).** Where a gap is "none", how that was established is
stated; no instrument asserts completeness.

---

## D1 — count literals for the v30a hash set

- **CLAIMED CLASS.** Every count literal in the shipping corpus referring to the tag-message hash
  set equals `len($FILES)`.
- **ACTUAL DOMAIN.** Lines matching a tag-message/hash-set context, from which a *number phrase*
  attached within two words of a hash-set noun is parsed. Numerals 0–99,999 with any comma
  grouping; English words 0–999 (hundreds, "and", tens-unit compounds); ordinals to *twelfth*;
  `both`. Markdown emphasis stripped; **table rows included**. Bare `lines` counts only in the
  construction "tag message … N lines".
- **GAP — what it CANNOT see.** Informal quantifiers (`a dozen`, `half a dozen`, `a couple of`);
  Roman numerals; the parenthetical-duplicate form `six (6) hashes`; a count whose noun is more
  than two words away; a count with no hash-set noun at all; ranges (`6-8 hashes` reads as 6).
  Values above 99,999 in numeral form. **Unparsed phrases are REPORTED, not skipped** — the
  instrument fails loudly rather than silently passing on anything it matched but could not read.
- **BOUNDARY TEST.** Property test, **0–200 × 10 surface forms = 2,010 cases: 2,010 correct, 0
  wrong, 0 missed.** Beyond the edge: 201, 999, 1,000, 9,999, 10,000 all CORRECT. `a dozen`,
  `half a dozen`, `a couple of`, `VI`, `six (6)`, noun-absent and noun-distant all MISSED, as listed
  in the gap.

> **This instrument reported PASS for its entire life before R70 while detecting no numerals at
> all.** `6 hashes`, `42 hashes`, `1,000 hashes` were invisible, and `twenty-five hashes` resolved
> to **20** — a wrong value, which is worse than a miss because it can accidentally equal the
> authority. Its 8/8 and 19/19 batteries passed because every mutation was authored from inside its
> vocabulary. **B5.3 is the rule that follows.**

## D2 — path enumerations that purport to BE the hash set

- **CLAIMED CLASS.** Any enumeration of the hashed paths equals `$FILES`, order-sensitive for the
  tag-message body.
- **ACTUAL DOMAIN.** Lines carrying ≥3 of the six basenames, judged over a five-line window
  (idx−2 … idx+2). Plus a structural parse of the `<64 hex>  <path>` block for the tag body.
- **GAP.** An enumeration spread over **more than five lines**; one carrying **≤2** of the six; one
  written with paths spelled differently (relative prefixes, backslashes); an enumeration inside a
  fenced block the window splits. `git add` lines are deliberately excluded and owned by D3.
- **BOUNDARY TEST.** Per-exemption mutation on all 5 D2 exemptions: **5/5 fired.** Tag-body
  reorder: fired. Enumeration losing a member: fired. Window edge not separately probed — **stated
  as an open gap, not as coverage.**

## D3 / D4 — the staging plan covers the hash set

- **CLAIMED CLASS.** D3: §4's aggregate `git add` set ⊇ `$FILES`. D4: the pre-commit block *derives*
  `$FILES` from its authority and names every member.
- **ACTUAL DOMAIN.** D3 parses lines matching `^git add `. D4 greps for the literal derivation
  command and for each member's path as a substring.
- **GAP.** D3 cannot see staging performed any other way — `git add -A`, a shell variable, a
  wildcard, or an add inside a loop. D4's "names every member" is substring presence, which a
  mention in prose satisfies as readily as a real EXPECT entry.
- **BOUNDARY TEST.** M4 (drop a hashed file from the add set): fired. M5a (remove the derivation):
  fired. M5b (a member never named): fired.

## D5 / D6 — exemptions

- **CLAIMED CLASS.** A site may carry a known historical value; anything else fails.
- **ACTUAL DOMAIN.** Keyed by **path + line**, pinned to a substring that must be on that line, and
  since R70 scoped to an explicit **allowed value set** (counts) or **ordered tuple**
  (enumerations).
- **GAP.** Line keys drift on every insertion above them — observed **five times in three rounds**.
  Drift now fails loudly and the message names the destination line, so it is a maintenance cost,
  not a silent hole. An exemption whose pinned text appears on two lines is reported ambiguous
  rather than resolved.
- **BOUNDARY TEST.** **19/19 per-exemption mutations fired**, each writing a value the exemption
  does not whitelist. Before R68/R70 the same mutations were **silent** on all 8 D1 sites and both
  D7 line-scoped sites.

## D7 — declaration hash/size values

- **CLAIMED CLASS.** Every recorded declaration hash or byte/line size in the shipping corpus
  matches the file.
- **ACTUAL DOMAIN.** Lines naming `AVAILABILITY_DECLARATION.md` **by filename**, in the six-file
  set + every `evidence/**/*.md` + root manifest-carrying prose, **table rows included**. Plus a
  structural parse of the f4 pointer's current block.
- **GAP — explicitly excluded, with the reason.** `DECLARATION_POINTER.md`'s **prose** is out of
  population: it is a change ledger recording every past transition by from-hash and to-hash, so
  scanning it flags 24 historical values that are correct as history. **Its one live value is the
  structured current block, which IS checked.** Also invisible: a declaration hash on a line that
  says only "the declaration" without the filename; truncated hashes under 8 hex.
- **BOUNDARY TEST.** 5/5 negative tests fired, including two that were **SILENT before exemptions
  became value-scoped**. The widening happened twice: R68 install, R68 rescope.

## D8 — line-pinned citations

- **CLAIMED CLASS.** Six registered citations whose targets have no heading still resolve to
  expected content.
- **ACTUAL DOMAIN.** Exactly those six pairs. **Nothing else.**
- **GAP — large and stated.** 395 line citations exist in the shipping corpus; D8 covers **6**. The
  other 389 are covered by classification, not by assertion: 117 into locked `PREREG.md` (cannot
  drift), 158 archive/source (113 carrying a quoted content pin), 49 live (38 pinned), and **71
  UNATTRIBUTED — a defect in the classifier, reported as such and not as coverage.**
- **BOUNDARY TEST.** Insert a line above `### H-34`: fired on 3 of 6 registrations, with
  `HISTORY.md:219` reporting that it now reads *lesson 12's* text — the plausible-but-wrong
  resolution the instrument exists to catch.

## The §A.11 conformance walk

- **CLAIMED CLASS.** Every registered §6.2 element is walked and given a verdict; none is left
  "outstanding".
- **ACTUAL DOMAIN.** 23 lines of §6.2's 443–481 span, enumerated by line number in the walk table.
- **GAP.** **Four non-blank lines are not walked: 443, 455, 466, 478.** Three are justified — 443 is
  the section heading, 455 and 466 are historical parentheticals describing superseded versions.
  **478 is normative prose and is the real gap** ("This is a rebalance, not a tightening. The two
  gates are incomparable…"), and it is the site R66 §2.1 exists to fix.
- **BOUNDARY TEST.** Line-by-line set difference over 443–481 with the walk's ranges expanded.
  *A first pass, which did not expand range rows like `470-476`, reported six gaps and was wrong;
  472 and 474 are covered by that range. Recorded because an instrument audit that miscounts is
  the thing this audit is about.*

## The manifest check (`sha256sum -c MANIFEST.sha256`)

- **CLAIMED CLASS.** The evidence tree is unmodified since the manifest was written.
- **ACTUAL DOMAIN.** Exactly the paths the manifest lists. It verifies listed→disk; **it cannot
  see disk→listed.**
- **GAP — CLOSED at R71/§37, and this line records what remains AFTER the fix, not before.**
  `sha256sum -c` itself is still one-directional and always will be; the reverse direction is now
  asserted by two instruments outside it. **D9 (`manifest_coverage`)** enumerates every file under
  the manifest's claimed scope and fails if any lacks a line; **C2d-1** does the same against the
  INDEX at tag time, which is the set the commit actually carries. *What remains:* D9 reads the
  working tree, so between D9's run and `git add` a file could still appear — which is precisely
  why C2d-1 exists and runs at ceremony time. Neither can see a file added **after** C2d-1 and
  before `git commit`; C2g's clean-tree assertion is the backstop there.
- **BOUNDARY TEST.** Before: set comparison, 248 listed / 248 on disk — the gap was closed *that
  day, by coincidence of contents*, not by any instrument. After: a scratch file was written into
  `evidence/`, **D9 FIRED** naming it as "would ship inside the signed commit unattested", and the
  file was removed. The property is now checked, not observed.

## The sweeps still relied upon

| sweep | claimed | actual domain | gap | boundary test |
|---|---|---|---|---|
| **A3 count-class** | prose counts of enumerated sets, shipping corpus | 6-file set + ceremony `*.md`; count word adjacent to a set noun; **skipped lines beginning with `\|`** | **table rows were out of population** — three stale declaration values lived there and were found a round later by accident | re-run after widening found them; the exclusion is now recorded in H-L20 |
| **B3 citations** | every line citation, shipping corpus | every line of 14 files, paragraph-attributed, **no exclusions** | **71 of 395 UNATTRIBUTED** — the classifier cannot always tie a number to a target file | reported as a method defect; re-run once (window→paragraph) cut it from 142 |
| **K1 description** | every passage describing an amended object | ten amendments, agent-driven read | not mechanically bounded; no population proof. **R82/E1 — the weakness now has a NAMED MECHANISM:** K1's step-1 enumerator `_K1_enumerate.py` carries a literal BACKSPACE in its `MARK` regex, so the marker split it guards never runs. Measured against the current source: **37 blocks emitted where 40 are correct** — 2 runs collapse (ssf 663: 2→1; ssf 789: 3→1) and **3 marker sites appear in no catalogue entry at all** (§8.2 line 915, §11 item 3, §0.2.1 line 97). Not a MISS but a **MISCOUNT plus a MISATTRIBUTION**: each collapsed run keeps ONE sha12 anchor and ONE `first` field showing only its first marker, so several sites are carried under one anchor. **The failure is silent by construction** — the `marker split: N run(s) -> M block(s)` progress line only prints when the split fires, so a split that never fires prints nothing. | **none.** See E1's containment note below |

**E1 CONTAINMENT — the defect does not reach a cited number.** `_K1_enumerate.py` is **superseded**.
The cited population artifact `_K1_population_FROZEN.json` carries the `idx/lines/kind` schema, which
`_K1_enumerate.py` does not emit; it is written by **`_K1_enumerate2.py`**, which has **0 control
bytes** and **no marker split at all** — multi-site runs are expanded by hand in `BLOCK_MANIFEST.md`
(*"Six of the 33 are multi-site runs … giving 42 entries"*). `_K1_enumerate.py`'s own output,
`_K1_population.json`, **is cited in no shipping document.** So neither E1.2's floor framing nor
E1.3's figure correction applies: **D-STALE's two figures — the sweep's finding and the
uncorrected remainder — come from the agent-driven description sweep, not from this script,
and neither is touched by this defect.** They are referred to by role rather than restated,
because a figure this finding does not bear on should not be repeated in its record (E1.3). Restating them
here would be restating a number this finding does not bear on.

**Corpus-wide check, stronger than E3.1 asked for.** All **230** `.py` files in the shipping tree
were scanned byte-exact: **exactly one** carries a control character — `_K1_enumerate.py`, byte 6097.
**No regex in any other script, cited or not, contains a control byte.** D12 now holds that line.

**Separate and unresolved, found while measuring this and NOT caused by it.**
`_K1_population_FROZEN.json` is **byte-identical** to the live `_K1_population.json` (sha256
`c430a4d4…`), which is not what "frozen" asserts; it holds **36** entries of which **30** begin
inside lines 89–1576, while `BLOCK_MANIFEST.md` describes it as **33 blocks**; and **0 of its 36
sha12 anchors match the current `SCHEMA_SET_FINAL.md`**. The ranges point at an older source. Whether
this matters depends on whether `BLOCK_MANIFEST.md` is superseded by `SCHEMA_RECORDS.json` and the
R80 generator — **that is an author question, not mine**, and it is recorded here rather than
resolved.


---

## B5.3, EXTENDED AT R81/C3 — THE KNOWN-POSITIVE PRECONDITION

**B5.3 already said** a detector's mutations must include values drawn from OUTSIDE its accepted
domain. **C3 adds the precondition that makes that testable on a SWEEP:**

> **A sweep's clean result is not reported until the sweep has been run against at least one KNOWN
> POSITIVE and has FIRED on it.**

Filed here, with B5.3, rather than as a new lesson: it is the same rule — an instrument authored from
inside its own vocabulary passes vacuously — applied to sweeps instead of to detectors. It applies
**retroactively to any sweep whose result is still relied on pre-tag**.

**Why it earns its place.** The §88 external-text sweep returned **16 of 16 clean, twice**, while the
instance that prompted its existence (`Y3 §6.3`) sat inside its own population: first because it
matched filenames only, then because a heredoc wrote a literal backspace byte into the regex. Neither
was found by inspection. **Both were found by pointing the sweep at the known instance.**

**It recurred at R81 and the rule caught it.** The C2 resolvability check's first version used a
`NOT_TARGET` pattern to classify boundary references away from real targets. A `\b` written through a
non-raw Python triple-quoted string became **a literal backspace byte (0x08)** — the identical defect,
in a different file, three rounds later. There it produced a false CLEAN; here a false POSITIVE, which
is why it was survivable. **The fix was not a better pattern.** C2.1 says the vocabulary is unbounded,
so the classifier was removed outright and replaced by an explicit recorded-read table: every line a
field names but no record covers must carry the field's own words plus a determination, and a read
that fires on nothing is REPORTED (D7's rule, applied to reads).

## C3.3 — SWEEPS WHOSE CLEAN RESULT IS RELIED ON PRE-TAG, AND WHETHER THEY HAVE A KNOWN POSITIVE

Listed at R81 per C3.3. **Not re-run** — C3.3 asks which those are, and says not to re-run them yet.

| sweep | relied-on result | known positive |
|---|---|---|
| **§88** external-text | 3 hits; no further external operative text | **YES** — added at R81/C1; fired on SC-12 → Y3 |
| **C2** target resolvability | 16/16, 0 unresolved | **YES** — `--self-test`, fires on the R79 defect |
| **block reachability** (R81) | 2 findings | **YES** — `--self-test` |
| **§53.2** untraceable lines = 0 | yes | **NONE** |
| **§53.3** clauses missing = 0 | yes | **NONE** |
| **§57.3(b)** 21/21 and 15/15 | yes | **NONE** |
| **§57.3(c)** anchors exactly once 21/21 | yes | partial — §53.5 boundary test 2 |
| **§77.1** copied-anchor 10/10 | yes | §53.5 boundary test 2 |
| **§82** independent extraction 21/21 | yes | §53.5 boundary test 1 (digest corruption) |
| **§56/§62** script triage | yes | **NONE** — and it has already failed once, missing 161 scripts |

**Four have no known positive at all**, and **three of those four are the checks that were blind to
`PREREG.md` line 1022** (§53.2, §53.3, §57.3(b)) — see `APPROVAL_PACKAGE.md` §"⛔ HALT — R81/C2".
That is not a coincidence: all three reason forward from the record set, so a block the record set
never claimed cannot make any of them fire, and no mutation authored from inside their domain would
ever have revealed it.

---

## D2 (R81) — THE ESCAPING RULE, FILED AS TOOLING DISCIPLINE

> **File content is never written through a shell heredoc or a non-raw string literal.**
> **Use the Write tool, or `pathlib.write_text`/`write_bytes` from a script whose own content came**
> **from Write.**

Filed here with **B5.3** and **C3** rather than as a new lesson class, because the pattern is the
same one: **the instrument was narrower than its claim, and the gap stayed invisible until something
fired.** B5.3 is about a detector's vocabulary; C3 is about a sweep's known positive; D2 is about the
channel the instrument itself is written through. In all three the failure is silent by construction.

**The mechanism.** A `\b` intended as a regex word boundary, passed through a shell heredoc or a
non-raw Python string, becomes a literal BACKSPACE (0x08). The regex still compiles. It simply can
never match. The same applies to `\f` (FORM FEED), `\a` (BEL), `\v`, `\t` and `\n` in Windows
paths and prose. **A control byte renders as nothing** in terminal, editor, diff and code review
alike, so no amount of reading finds it.

**Seven instances, and the rule is being written because the fifth, sixth and seventh were produced
by the act of documenting the first four.**

| # | where | what happened | how it surfaced |
|---|---|---|---|
| 1 | §88 sweep, v1 | matched filenames only (`\S+\.md`) | **FALSE CLEAN 16/16** with `Y3 §6.3` inside its own population |
| 2 | §88 sweep, v2 | heredoc wrote `\b` as BACKSPACE; three alternatives dead | **FALSE CLEAN 16/16 again** — caught only by C1's known-positive test |
| 3 | heredoc `\\n` collapsing | multi-line string mangled | build noise |
| 4 | `check_registration.py`, twice | multi-line string broke the file | syntax error |
| 5 | R81/C2 `NOT_TARGET` | `\b` → BACKSPACE in a non-raw triple-quoted string | **false POSITIVE** — SC-1/SC-2 reported unresolved; survivable only by luck of direction |
| 6 | `APPROVAL_PACKAGE.md` §88 note | the prose *describing instance 2* contained the bug | **D12** |
| 7 | this file, the C3 section | the prose *describing instance 5* contained the bug | **D12** |

Instances 6 and 7 are the argument. Both were written **in the same session that diagnosed instances
1, 2 and 5**, by an author who had just finished explaining the mechanism, into sentences whose
subject *was* the mechanism. Rediscovery does not generalise; a rule applied at the point of writing
does.

**Two further instances predate the phase and are recorded, not fixed** (R13 — evidence artifacts are
never adjusted): `_K1_enumerate.py`'s `MARK` regex, where the BACKSPACE disables the marker split it
guards so the enumeration **under-splits**; and `_snapshots/PRE_R9_HASHES.txt`, where a Windows path
`fixture_spike\f4\availability_...` became FORM FEED and BEL. Both are dated records. Both are
carried as **value-scoped D12 exemptions with their reasons stated**, not waived.

**The instrument (D1.3).** `D12` in `tools/check_registration.py` scans the six-file set plus every
manifest entry, byte-exact, for anything outside TAB/LF/CR and the printable ranges. Negative test:
four probes — BACKSPACE, VERTICAL TAB (a control **outside** the incident vocabulary, per B5.3),
U+200B ZERO WIDTH SPACE (a different code path, the Unicode-category branch), and a TAB/LF/CR-only
file that **must not fire**. **4 of 4 correct**, manifest restored byte-exact, probe removed.
The fourth probe is not decoration: without it, a detector that returns a finding unconditionally
would pass the other three.

---

## F1 (R85) — FIX THE CONTENT, NOT THE EXEMPTION

> **When a detector fires on newly authored content, the FIRST response is to change the content.**
> **An exemption is the last resort, not the first.**

Filed here with B5.3, C3 and D2 as tooling discipline. The reasoning is the same in every one of
them: an instrument that is narrowed to fit the work stops being a test of the work.

**The instance that is its evidence (R84).** `CLAIM_ENUMERATION.md` was written as a table whose
rows paired a source filename with a figure drawn from it — the declaration's name in
one cell and, three cells later, a byte count quoted from one of its lines. **D7 fired**, reporting that the
file stated a byte size for the declaration that the declaration does not have. D7 was right to fire, and it was
right for a reason beyond its own rule: **a row juxtaposing a filename with a number asserts, to a
human reader exactly as much as to a detector, that the file IS that size** — when what the catalogue
records is that a LINE of that file CONTAINS that value. An exemption would have silenced the
detector and left the misreading in place for every human.

**The content changed instead.** The source file became a section heading and the file column was
dropped, so no row juxtaposes a filename with a figure. D7 went quiet because the defect it named was
gone, **and the artifact is clearer than the version that provoked it** — the distinction between
*carrying* a value and *being* one is now structural rather than something a reader must infer.

**The general form.** A detector firing on new content is evidence about the content first and about
the detector second. Exempting inverts that. The exemption is correct only where the content cannot
change — a dated record under R13, a frozen artifact — **and then the reason is what is recorded,
not the silence.**

---

## THE PATTERN, AND WHY IT IS A CLASS (B6.3)

**Ten instances now, and every single one in the direction that HIDES findings:**

1. §A.11's walk skipped line 478.
2. Four early sweeps excluded the active scratchpad root.
3. A3's count sweep excluded table rows.
4. D7 was widened twice (install, then rescope).
5. D1's vocabulary ceiling stopped at *eight*.
6. **D1 detected no numerals at all** — the largest, and it reported PASS throughout.
7. D1 mis-parsed compounds, yielding wrong values rather than misses.
8. D5/D6 exemptions were line-scoped, licensing any future error on an exempted line.
9. V1 was a print with no assertion, never once executed.
10. C2.5 was a condition with no command.

**Not one was found by reviewing the instrument. Every one was found by running it against
something outside its domain, or by accident.** The direction is not random: a narrow instrument
reports PASS, and PASS is what an author is hoping to see, so nothing prompts a second look.

**H-L21 (filed): an instrument's PASS is a statement about its domain, not about the world.** Until
its domain is measured, a PASS means "nothing in the part I look at", and the part it looks at is
usually smaller than its name. The measurement is not a review — reviewing an instrument uses the
same assumptions that built it, which is why nine of ten were found by accident rather than by
reading. **The measurement is a boundary test: run it at the edge of its domain and just outside,
and record what it cannot see.** An instrument whose gap is "none" must say how that was
established.

---

## GAPS THAT GO TO §12 (B6.4)

Gaps that **cannot** be closed within this ceremony, and are therefore disclosed:

1. **The manifest cannot see an unlisted file.** Closed today by set comparison (248/248); the
   structural gap remains and is checked only at ceremony time by V4.
2. **D8 covers 6 of 395 citations.** The other 389 rest on classification, and 71 are unattributed.
3. **K1's description sweep has no measured population.** Its output is cited as evidence, not
   relied on as coverage.
4. **D1 cannot read informal quantifiers, Roman numerals, or `six (6)` forms**, and reads a range as
   its first value.
5. **D3 cannot see staging done by any means other than a literal `git add` line.**

**A verification apparatus that claims more than it delivers is the exact defect this project
audits in other people's pipelines.** These are stated so that the registration's own instruments
are held to the standard the registration applies to its subject.
