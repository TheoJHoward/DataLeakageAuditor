# ITEM M3 — Zero-tick / magnitude-filter evidence

**Claim under test:** "phase5_fixed removed the magnitude filter; zero-tick rows excluded from
evaluation only."

**Verdict: CODE-VERIFIED (both halves), with one precision caveat — see §7.**

Method: static read only. No execution, no detector code, no development-corpus contact.
Archive treated as read-only.

Files examined:

- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\phase5\phase5_fixed.py`
  (56,467 bytes, mtime 2026-04-07 10:08)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\phase5\phase5_ml.py`
  (37,064 bytes, mtime 2026-04-06 19:24)

---

## 1. HALF ONE — magnitude filter removed (label prep)

`phase5_fixed.py`, lines 972-975 — verbatim:

```
   972	        # FIX 1: Keep ALL rows (no magnitude filter), just drop NaN labels
   973	        valid = feat_df.dropna(subset=[fwd_col])
   974	        # Note: sentinel rows have NaN fwd_col, so they're dropped here for
   975	        # tree models but kept implicitly in sequence builder via NaN features
```

Line 973 is the sole row-selection step applied to `feat_df` before the month split. It is a
`dropna` on the label column and nothing else — no `.abs()`, no threshold comparison.
The immediately following split (lines 978-980) consumes `valid` unfiltered:

```
   978	        train_df_h = valid[valid["month"].isin(months_train)]
   979	        val_df_h   = valid[valid["month"].isin(months_val)]
   980	        test_df_h  = valid[valid["month"].isin(months_test)]
```

Corroborating instrumentation at lines 988-994 exists only because zero-change rows survive:

```
   988	        # FIX 1: Print zero-change fraction
   989	        n_zero = (valid[fwd_col] == 0).sum()
   990	        n_total = len(valid)
   991	        zero_frac = n_zero / n_total if n_total > 0 else 0
```

**Negative check:** a grep of `phase5_fixed.py` for `MIN_MOVE|magnitude|abs\(.*fwd|fwd_move.*>=|>= *2`
returns no magnitude-threshold code anywhere in the file. The only two `magnitude` hits are the
comment on line 972 and the change-table string on line 1103 (§2). The filter is absent, not
relocated.

## 2. HALF ONE — self-description in the change table

`phase5_fixed.py`, `print_change_table()`, lines 1102-1112. The two load-bearing rows, verbatim:

```
  1103	        ("Magnitude filter",     "|fwd_move|>=2 ticks",       "Removed — all seconds used"),
```

```
  1110	        ("Zero-change seconds",  "Removed by mag filter",      "Kept in training, excluded from AUC"),
```

Line 1103 states the removal. Line 1110 states the replacement disposition — train-yes,
AUC-no — which is exactly the second half of the claim, asserted by the script about itself.

## 3. HALF TWO — training labels are built over ALL rows, including zero-tick

`phase5_fixed.py`, lines 630-638 — verbatim:

```
   630	    # FIX 1: Use ALL seconds. Label: 1 if fwd_move > 0, 0 if fwd_move <= 0
   631	    # Sentinel rows with NaN fwd_col get label NaN (will be discarded in sequences)
   632	    fwd_tr = train_df[fwd_col].values.astype(np.float64)
   633	    fwd_val_arr = val_df[fwd_col].values.astype(np.float64)
   634	    fwd_te_arr = test_df[fwd_col].values.astype(np.float64)
   635	
   636	    y_tr_raw  = np.where(np.isnan(fwd_tr), np.nan, (fwd_tr > 0).astype(np.float32))
   637	    y_val_raw = np.where(np.isnan(fwd_val_arr), np.nan, (fwd_val_arr > 0).astype(np.float32))
   638	    y_te_raw  = np.where(np.isnan(fwd_te_arr), np.nan, (fwd_te_arr > 0).astype(np.float32))
```

Line 636 is the decisive one. The predicate is `fwd > 0` — a strict inequality with no
zero-exclusion branch. A zero-tick row is therefore **not dropped**; it is assigned label `0`
and pooled with the genuine down-moves. The only NaN branch is for sentinel rows (`np.isnan`),
not for zero magnitude. This is what makes the phrase "excluded from evaluation **only**"
literally true: zero-tick rows are present, labelled, and trained on.

Training consumes these arrays unmasked. Tree/linear path, lines 741-745:

```
   741	        # FIX 1: train on ALL, eval on non-zero only
   742	        X_train = X_tr_raw.copy()
   743	        y_train = y_tr_raw.copy()
   744	        X_test_arr = X_te_raw.copy()
   745	        y_test_arr = y_te_raw.copy()
```

No `eval_mask` appears on any `.fit()` call (e.g. line 767-768 `model.fit(X_train, y_train, ...)`).

## 4. HALF TWO — the eval_mask, tree/linear variant (line 747)

`phase5_fixed.py`, line 747 — verbatim:

```
   747	        eval_mask_te = (fwd_te_arr != 0) & (~np.isnan(fwd_te_arr))
```

Defined inside the `else:` (non-DL) branch opened at line 739. Note it is built from
`fwd_te_arr` — the **test** array only — and is constructed *after* `X_train`/`y_train` are
already fixed at lines 742-743. It cannot reach training.

Point of application, lines 807-811 — verbatim:

```
   807	        # Compute AUC on non-zero only (FIX 1)
   808	        if eval_mask_te.sum() > 10:
   809	            test_auc = roc_auc_score(y_test_arr[eval_mask_te], test_pred[eval_mask_te])
   810	        else:
   811	            test_auc = roc_auc_score(y_test_arr, test_pred)
```

The mask's entire lifetime is the subscript on line 809. Same pattern for validation AUC at
lines 816-818:

```
   816	            eval_mask_v = (fwd_val_arr != 0) & (~np.isnan(fwd_val_arr))
   817	            if eval_mask_v.sum() > 10:
   818	                best_val_auc = roc_auc_score(y_val_arr[eval_mask_v], vp[eval_mask_v])
```

(also at lines 796-798 for the LogReg sweep).

## 5. HALF TWO — the eval_mask, sequence/DL variant (line 678)

`phase5_fixed.py`, lines 677-681 — verbatim:

```
   677	        fwd_at_labels_te = get_label_fwd(X_te, y_te_raw, fwd_te_arr)
   678	        eval_mask_te = (fwd_at_labels_te != 0) & (~np.isnan(fwd_at_labels_te))
   679	
   680	        fwd_at_labels_val = get_label_fwd(X_val, y_val_raw, fwd_val_arr)
   681	        eval_mask_val = (fwd_at_labels_val != 0) & (~np.isnan(fwd_at_labels_val))
```

Line 678 is the same `!= 0` predicate as line 747, but indexed against sequence **label
positions** rather than raw rows. The helper that produces the aligned fwd values,
lines 663-675, walks the same stride-`SEQ_LEN` blocks and applies the same NaN-discard rule the
sequence builder uses, so the mask lines up element-for-element with `ys_te`:

```
   663	        def get_label_fwd(X_arr, y_arr, fwd_arr):
   664	            n = len(X_arr)
   665	            n_possible = (n - SEQ_LEN) // SEQ_LEN
   666	            fwd_at_labels = []
   667	            for j in range(n_possible):
   668	                start = j * SEQ_LEN
   669	                label_idx = start + SEQ_LEN
   670	                if label_idx >= n:
   671	                    break
   672	                seq_block = X_arr[start:start+SEQ_LEN]
   673	                if not np.isnan(seq_block).any() and not np.isnan(y_arr[label_idx]):
   674	                    fwd_at_labels.append(fwd_arr[label_idx])
   675	            return np.array(fwd_at_labels) if fwd_at_labels else np.zeros(0)
```

Crucially, the DL training sequences are built at lines 657-659 **before** the mask exists, and
are passed to the trainer unmasked:

```
   657	        Xs_tr,  ys_tr,  meta_tr  = build_sequences_fixed(X_tr,  y_tr_raw)
   658	        Xs_val, ys_val, meta_val = build_sequences_fixed(X_val, y_val_raw)
   659	        Xs_te,  ys_te,  meta_te  = build_sequences_fixed(X_te,  y_te_raw)
```

Point of application, lines 715-719 — verbatim:

```
   715	        # FIX 1: AUC on non-zero-change only
   716	        if eval_mask_te.sum() > 10:
   717	            test_auc = roc_auc_score(ys_te[eval_mask_te], test_pred[eval_mask_te])
   718	        else:
   719	            test_auc = roc_auc_score(ys_te, test_pred)
```

The mask is additionally forwarded to the shuffle-test control (line 727) so the null
distribution is scored on the identical subset — lines 453-458:

```
   453	            # Apply same eval mask as real run
   454	            if ys_test_eval_mask is not None:
   455	                tp = test_pred[ys_test_eval_mask]
   456	                yt = ys_test[ys_test_eval_mask]
```

That is still evaluation, not training. **Complete list of `eval_mask` occurrences in
`phase5_fixed.py`:** lines 438, 454-456, 472, 510-512, 678, 681, 716-717, 727, 747, 796-798,
808-809, 816-818, 825. Every one is either a definition, a parameter pass-through, or a
subscript feeding `roc_auc_score`. **None is on a `.fit()`, a loss, or a sampler.**

## 6. CONTRAST — `phase5_ml.py`'s filter (line 679)

`phase5_ml.py`, lines 677-684 — verbatim:

```
   677	        # Apply magnitude filter
   678	        valid = feat_df.dropna(subset=[ret_col])
   679	        valid = valid[valid[ret_col].abs() >= 2.0].copy()
   680	        valid["target"] = (valid[ret_col] > 0).astype(int)
   681	
   682	        train = valid[valid["month"].isin(TRAIN_MONTHS)]
   683	        val = valid[valid["month"].isin(VAL_MONTHS)]
   684	        test = valid[valid["month"].isin(TEST_MONTHS)]
```

Structural contrast, and it is the whole point:

- Line 679 sits **above** the train/val/test split on lines 682-684. The filter is therefore
  applied to the corpus *once*, upstream of everything, so the surviving rows define both the
  training set and the evaluation set.
- `phase5_ml.py` contains **no `eval_mask` of any kind** (grep: zero hits). Its eight
  `roc_auc_score` calls — lines 462, 490, 528, 529, 549, 568, 578, 595 — are all unmasked,
  because there is nothing left to mask out.
- Compare line 973 of `phase5_fixed.py` (`dropna` only, filter gone) against line 679 here
  (`dropna` **plus** `.abs() >= 2.0`). Line 678 of `phase5_ml.py` and line 973 of
  `phase5_fixed.py` are the same statement; line 679 is precisely the statement that was deleted.
- Both files build the label with the same `> 0` predicate (`phase5_ml.py` line 680,
  `phase5_fixed.py` line 636). The label rule did not change. Only the population it is applied
  to changed.

## 7. CAVEAT — the two exclusions are NOT complements

Worth recording because it bears on any comparison of AUCs across the two scripts:

- `phase5_ml.py` line 679 excludes `|fwd| < 2`, i.e. it drops **-1, 0, and +1** tick rows.
- `phase5_fixed.py` lines 678/747 exclude `fwd == 0`, i.e. they drop **only 0** tick rows.

So `phase5_fixed`'s evaluation set is strictly larger than a like-for-like recovery of
`phase5_ml`'s: the ±1-tick rows, previously absent everywhere, are now **in both training and
evaluation**. The claim's phrase "zero-tick rows excluded from evaluation only" describes
`phase5_fixed`'s own behaviour accurately, but it does not imply the two scripts' AUCs are
computed over comparable populations. They are not.

Secondary asymmetry, `phase5_fixed.py` lines 721-722:

```
   721	        # Use training's best val AUC (computed during training on all samples)
   722	        val_auc_eval = best_val_auc
```

The DL branch's reported validation AUC is **unmasked** (zero-tick rows included), whereas the
tree/linear branch's validation AUC **is** masked (lines 816-818). Test AUC is masked on both
branches. This affects val-AUC comparability between architecture families only; it does not
touch the claim, which concerns test evaluation.

---

## 8. VERDICT

| Half of claim | Status | Exact citation |
|---|---|---|
| "phase5_fixed removed the magnitude filter" | **VERIFIED** | `phase5_fixed.py:972-973` — comment "FIX 1: Keep ALL rows (no magnitude filter)" + `valid = feat_df.dropna(subset=[fwd_col])`, the only row selection, no threshold. Corroborated by change table `phase5_fixed.py:1103` and by absence of any magnitude predicate file-wide. Contrast: the deleted statement survives at `phase5_ml.py:679`. |
| "zero-tick rows excluded from evaluation only" | **VERIFIED** | Included in training: `phase5_fixed.py:636` `(fwd_tr > 0)` labels zero-tick as 0, no drop; unmasked `.fit()` at 742-743/767. Excluded at eval: `phase5_fixed.py:747` (tree) and `:678` (sequence), both `(fwd != 0) & ~isnan`, applied solely at `roc_auc_score` (`:809`, `:717`). Self-described at `:1110` "Kept in training, excluded from AUC". |

Caveat on scope, not on truth: §7 — `!= 0` (fixed) and `|x| >= 2` (ml) exclude different
populations, so the removal was not a straight swap of one exclusion for another.
