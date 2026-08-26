# F3 FIXTURE MANIFEST — AUTHOR REVIEW PACKAGE

**Why this exists.** The ceremony halted at **C2.5**. `SC-4(k2)` — now registered text in the applied
`PREREG.md` — makes this file **an object the gate consumes**, and requires that it be enumerated in
the declaration's SC-8(a) freeze and **not carry a `DRAFT` status at the tag**. It carries one.

**The status has not been altered by automated tooling, and no such alteration was requested.** A field reading *"author
review required"*, flipped without an author review, would be a false statement about a gate input
inside the signed object. **Nothing below changes the file.** This package exists so the review can
happen, not to substitute for it.

**There is no "disclose and proceed" route.** A registration whose reconciliation reads an unfrozen
draft has no freeze.

---

## THE FILE

| | |
|---|---|
| path | `evidence/fixture_spike/f3/fixture_manifest_DRAFT.json` |
| sha256 | `f871b2c773fd4edae7ad068a95da554dd594ecafcb0a1a3ef7f6ef5ce2e26ec5` |
| bytes | 26,576 |
| *(the bytes moved when the classification basis was restated; no classification changed)* | |
| `manifest_status` | **`DRAFT - author review required`** ← the blocking field |

**It is F3, not T4, and the declaration says so in terms:** *"Why F3 governs and not T4."*
`t4/fixture_manifest_35col_DRAFT.json` declares itself `derived_from` the F3 manifest and is a
35-column **projection**, not a classification. **The registered text disambiguates; there is no
ambiguity to halt on.**

## WHAT SC-4(k2) ACTUALLY READS FROM IT

Not the file at large — **one list**: *"the fixture manifest's list of columns classed as leaking
sources — **the named list**, not the count."* The limb also states the count is **not** a gate
quantity and enters **no** denominator.

**So the review that matters is a review of these 25 names, and of the basis on which they are so
classed.** Everything else in the file is context.

## THE SMALLEST SET OF FACTS TO CHECK

**1. The classification basis** — one sentence, and everything below depends on it:

> Classes describe the **PRE-LAG** construction semantics — what each column reads relative to the
> label base `mid(t)` **BEFORE** the universal `shift(1)` at `phase7_l2_sim.py` line 276.

**Is pre-lag the right frame for a leakage ground truth?** If it is, the list follows. If it is not,
the list is wrong in a way no downstream check would catch.

**2. The 25 LEAK-SOURCE names, in their two flavors.**

*`label_base_price` (7) — reads the same mid the label is built from:*
`mid_return_1s` · `mid_return_5s` · `mid_return_10s` · `mid_return_30s` · `tick_direction` ·
`vwap_distance` · `weighted_mid`

*`contemporaneous_state_flow` (18) — reads state at `t` that the label's forward window also sees:*
`trade_volume_1s` · `trade_count_1s` · `dollar_volume_1s` · `net_delta_1s` · `net_delta_5s` ·
`net_delta_10s` · `net_delta_30s` · `net_delta_60s` · `buy_volume_10s` · `sell_volume_10s` ·
`large_trade_count_10s` · `bid_size_1` · `ask_size_1` · `total_bid_depth` · `total_ask_depth` ·
`spread_ticks` · `book_slope_bid` · `book_slope_ask`

**3. The two borderline calls the file flags itself.** Both carry a `note`, and both are judgement,
not derivation:

- a column *"Reads raw book columns at t directly (`bid_size_1`, `bid_size_5`); classified
  **LEAK-SOURCE** per the 45-set DAG, not DESCENDANT."*
- a column *"Not in the 45-set; new classification. Pure function of two contemporaneous leak
  sources — **inherits, does not independently leak**."*

**4. The counts, only as a cross-check on the names:** 35 columns = **25 LEAK-SOURCE** + 6 DESCENDANT
+ 4 CLEAN; `independently_leaking_sources: 25`; 19 columns not fed to Phase 7.

## WHAT CONFIRMING THIS COMMITS YOU TO

The 25 names become **a gate input**: SC-4(k2) requires every unit the manifest so classes that the
derivation does not class REQUIRED to be **named individually**, with the registered predicate that
produced its class. A later revision of this list would be **a change to a gate input outside the
class C route** — which is exactly why the limb forbids a `DRAFT` status at the tag.

## THE TWO THINGS THAT MUST HAPPEN, IN ORDER

1. **[AUTHOR]** review the 25 names and the pre-lag basis; then the `manifest_status` field ceases to
   say review is required. **This step is the author's and is not delegable to tooling.**
2. **[THEN]** the file is added to `AVAILABILITY_DECLARATION.md` §D.1 item 3's *"Specifically and
   exhaustively"* list. That list currently names the ground-truth map, the cohort predicate, the
   reference AUC trio, criterion 1's column enumeration, §C.4's declared exclusions, the fixture
   identity and pc2 exclusion, and the `floor(t-1)+1s` boundary — **and no fixture manifest.** A
   declaration edit, which is permitted; the declaration is revisable.

**Both, or C2.5 halts again — correctly.**
