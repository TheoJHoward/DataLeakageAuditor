#!/usr/bin/env python3
"""DELTA R57/W2a - re-scope every C6 citation to what the re-verification supports.

GATES THE TAG: K6_RESULTS.md ships inside the killgate tree, which R48/Q1(a) admitted to
the Phase 0 record and X4 item 7a puts on the staging list.

Three sites, found by identifier-and-numeral search after a prose literal gave a false
clean: lines 22, 109, 260.

WHAT THE RE-VERIFICATION SUPPORTS. Of the five tools declared eligible on C6, exactly ONE
produced an informative negative. The other four could not, for reasons that are defects
of the harness or of the tools' reach - and every one of those defects leans toward the
conclusion this project wants, which is why the count may not stand unqualified.
"""
import pathlib

KG = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                  "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                  "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/killgate/k6")
p = KG / "K6_RESULTS.md"
t = p.read_text(encoding="utf-8")

SUBS = []

# --- site 1: the summary headline (line 22) ----------------------------------
SUBS.append((
    "**And the load-bearing negative result is now measured rather than asserted: on C6 \u2014 the\n"
    "one-bar-of-reach case \u2014 five eligible tools produced zero hits.** Four ran and were silent or\n"
    "false-alarmed; one crashed.",

    "**And the load-bearing negative result is measured rather than asserted \u2014 at the strength the\n"
    "evidence actually supports, which is narrower than this file first claimed. On C6, the\n"
    "one-bar-of-reach case, ONE in-kind tool was measured and missed.** *(Re-scoped 21 August 2026,\n"
    "R57/W2a, after independent re-verification by a party that did not produce this run. The\n"
    "sentence here previously read \"five eligible tools produced zero hits\", which is arithmetically\n"
    "true and invites the reading that five independent detectors examined C6 and failed. One did.)*\n"
    "\n"
    "Of the five declared eligible: **`leak-detect`** is the only informative miss \u2014 a demonstrably\n"
    "live probe that fires on C5 both sides and on C2 contaminated. **`deepchecks`** could not\n"
    "register a hit by construction: its only T6-mapped check tests train/test **date** overlap,\n"
    "which C6 holds identical on both sides. **`Leakly`** fired on **0 of 8** cell-sides and no\n"
    "positive control was ever established for it. **`temporalcv`**'s recorded evidence is unsound \u2014\n"
    "of its three T6-mapped gates, `gate_temporal_boundary` is **never called** and\n"
    "`gate_suspicious_improvement` is wired with **inverted polarity** and cannot fire.\n"
    "**`leakage-buster`** crashed on NaN because its adapter alone omits `.dropna()`, and C6 is the\n"
    "**only** case in the set containing NaN \u2014 a harness defect landing on exactly the flagship case.\n"
    "\n"
    "**Every one of these defects leans the same way: toward the conclusion this project wants.**\n"
    "The harness fixes and the re-run are tracked separately as W2b; until they land, **no form of\n"
    "the five-tool claim may be cited.**"))

# --- site 2: the section heading (line 109) ----------------------------------
SUBS.append((
    "### 3.1 C6 \u2014 the flagship. Five eligible tools, zero hits.",
    "### 3.1 C6 \u2014 the flagship. One in-kind tool measured and missed; three could not register a hit; one crashed on a harness defect."))

# --- site 3: the conclusion (line 260) ---------------------------------------
SUBS.append((
    "on the case built to test exactly that, five eligible tools returned zero hits.",
    "on the case built to test exactly that, **the one in-kind tool able to register a hit did not**.\n"
    "Three further tools were nominally eligible but structurally unable to register one, and a fifth\n"
    "abstained on a harness-caused crash \u2014 so **this case does not carry the weight of five\n"
    "independent negatives**, and is not to be cited as though it did (R57/W2a)."))

for old, new in SUBS:
    n = t.count(old)
    assert n == 1, "match count %d for %.60s" % (n, old.replace("\n", " "))
    t = t.replace(old, new, 1)

p.write_text(t, encoding="utf-8")
print("K6_RESULTS.md: %d C6 citations re-scoped" % len(SUBS))
